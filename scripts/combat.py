#!/usr/bin/env python3
"""
combat.py — a generic 5e initiative & resource tracker (REPL).

Knows nothing about any campaign: every combatant is data you load or add.

Run:
    python scripts/combat.py                 # resume autosave, or start empty
    python scripts/combat.py fight.json      # load an encounter (fresh)

Encounter file = a JSON list of combatants, e.g.:
    [
      {"name": "Big Bad", "init": 14, "side": "enemy",
       "hp": 300, "lr": 3, "la": 3, "recharge": {"Roar": "5-6"}},
      {"name": "Aria",  "init": 18, "side": "pc"},
      {"name": "Bran",  "init": 11, "side": "pc"}
    ]

PCs need only name/init/side: HP isn't tracked, just up/down (down turns are
skipped). Enemies track hp, lr (legendary resistance), la (legendary actions),
recharge abilities and conditions. Everything else has sane defaults.

Type `help` inside for commands.
"""

import sys
import os
import json
import copy
import random

try:
    import readline  # noqa: F401 — gives input() up/down history + line editing
except ImportError:
    pass  # not present on some platforms; REPL still works, just no history

# ---- ANSI (degrades fine if your terminal ignores it) ----------------------
BOLD = "\033[1m"
DIM = "\033[2m"
RST = "\033[0m"
CUR = "\033[96m"   # current turn (cyan)
ENEMY = "\033[95m"   # enemies (magenta/purple)


# ---- combatant construction -------------------------------------------------
def parse_recharge(spec):
    """'5-6' or '6' -> {'lo':5,'hi':6,'ready':True}. d6 assumed."""
    spec = str(spec).strip()
    if "-" in spec:
        lo, hi = spec.split("-", 1)
        lo, hi = int(lo), int(hi)
    else:
        lo = hi = int(spec)
    return {"lo": lo, "hi": hi, "ready": True}


def make_combatant(d):
    """Normalise a raw dict (from a file or `add`) into our runtime shape."""
    side = d.get("side", "enemy").lower()
    is_pc = side == "pc"
    # PCs: HP untracked by design. For others, current/max are tracked
    # separately so a resumed state keeps both (don't clobber max with current).
    hp = None if is_pc else d.get("hp")
    maxhp = None if is_pc else d.get("maxhp", hp)
    maxlr = int(d.get("maxlr", d.get("lr", 0)))
    lr = int(d.get("lr", maxlr))
    maxla = int(d.get("maxla", d.get("la", 0)))
    la = int(d.get("la", maxla))
    recharge = {}
    for name, spec in (d.get("recharge") or {}).items():
        if isinstance(spec, dict):                 # already-normalised (saved state)
            recharge[name] = {"lo": spec["lo"], "hi": spec["hi"],
                              "ready": spec.get("ready", True)}
        else:                                      # authored "5-6" / "6"
            recharge[name] = parse_recharge(spec)
    return {
        "name": d["name"],
        "init": int(d.get("init", 0)),
        "side": "pc" if is_pc else "enemy",
        "down": bool(d.get("down", False)),
        "hp": hp,
        "maxhp": maxhp,
        "lr": lr, "maxlr": maxlr,
        "la": la, "maxla": maxla,
        "reaction": None if is_pc else bool(d.get("reaction", True)),
        "recharge": recharge,
        "conds": dict(d.get("conds", {})),  # {tag: rounds_left or None}
    }


# ---- state -----------------------------------------------------------------
class State:
    def __init__(self):
        self.round = 1
        self.turn = 0          # index into self.order()
        self.combatants = []
        self.undo_stack = []
        self.state_path = None   # where autosave writes; set at boot
        self.source_path = None  # the encounter file, for `reset`; set at boot

    # combatants sorted high->low init, stable on insertion order for ties
    def order(self):
        return sorted(self.combatants, key=lambda c: -c["init"])

    def to_dict(self):
        return {"round": self.round, "turn": self.turn,
                "combatants": self.combatants}

    @classmethod
    def from_dict(cls, d):
        s = cls()
        s.round = d.get("round", 1)
        s.turn = d.get("turn", 0)
        s.combatants = [make_combatant(c) for c in d.get("combatants", [])]
        return s

    # ---- undo / autosave ----
    def snapshot(self):
        self.undo_stack.append(copy.deepcopy(
            {"round": self.round, "turn": self.turn,
             "combatants": self.combatants}))
        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            print("nothing to undo")
            return
        snap = self.undo_stack.pop()
        self.round = snap["round"]
        self.turn = snap["turn"]
        self.combatants = snap["combatants"]

    def autosave(self):
        if not self.state_path:
            return
        try:
            with open(self.state_path, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
        except OSError as e:
            print(f"(autosave failed: {e})")

    # ---- lookup ----
    def find(self, needle):
        """Case-insensitive: exact name, else unique prefix match."""
        needle = needle.strip().lower()
        exact = [c for c in self.combatants if c["name"].lower() == needle]
        if exact:
            return exact[0]
        hits = [c for c in self.combatants if c["name"].lower().startswith(needle)]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            print(f"no combatant matches '{needle}'")
        else:
            print(f"'{needle}' is ambiguous: " +
                  ", ".join(c["name"] for c in hits))
        return None

    def current(self):
        order = self.order()
        if not order:
            return None
        self.turn %= len(order)
        return order[self.turn]


# ---- turn engine -----------------------------------------------------------
def start_of_turn(state, c):
    """Start of a creature's turn: refresh LA + reaction, roll recharges."""
    if c["maxla"] and c["la"] != c["maxla"]:
        c["la"] = c["maxla"]
    if c.get("reaction") is False:           # reaction refreshes on its turn
        c["reaction"] = True
    for name, r in c["recharge"].items():
        if not r["ready"]:
            roll = random.randint(1, 6)
            if r["lo"] <= roll <= r["hi"]:
                r["ready"] = True
                print(f"  {c['name']}: {name} recharged (rolled {roll})")
            else:
                print(f"  {c['name']}: {name} not ready (rolled {roll})")


def end_of_turn(state, c):
    """End of a creature's turn: tick its timed conditions (so a '1' set
    before its turn lasts THROUGH that turn, then clears — i.e. 'until the
    end of its next turn'). Sticky conditions (no number) never tick."""
    expired = []
    for tag, left in list(c["conds"].items()):
        if left is None:
            continue
        left -= 1
        if left <= 0:
            expired.append(tag)
            del c["conds"][tag]
        else:
            c["conds"][tag] = left
    if expired:
        print(f"  {c['name']}: {', '.join(expired)} ended")


def advance(state):
    order = state.order()
    if not order:
        print("no combatants")
        return
    if all(c["down"] for c in order):
        print("everyone is down — nothing to advance to")
        return
    end_of_turn(state, order[state.turn % len(order)])  # end the current turn
    for _ in range(len(order) + 1):
        state.turn += 1
        if state.turn >= len(order):
            state.turn = 0
            state.round += 1
            print(f"{BOLD}=== Round {state.round} ==={RST}")
        c = order[state.turn]
        if not c["down"]:
            start_of_turn(state, c)
            return


# ---- rendering -------------------------------------------------------------
def pips(remaining, total):
    return "●" * remaining + "○" * (total - remaining)


def render(state):
    order = state.order()
    print()
    print(f"{BOLD}Round {state.round}{RST}  " + "─" * 40)
    if not order:
        print("  (no combatants — `add` or `load <file>`)")
        print()
        return
    cur = order[state.turn % len(order)]
    for c in order:
        marker = "►" if c is cur else " "
        name = c["name"]
        bits = []
        if c["side"] == "pc":
            bits.append("down" if c["down"] else "")
        else:
            if c["hp"] is not None:
                bits.append(f"{max(c['hp'],0)}/{c['maxhp']}")
            if c["down"]:
                bits.append("DEAD")
            if c["maxlr"]:
                bits.append("LR " + pips(c["lr"], c["maxlr"]))
            if c["maxla"]:
                bits.append("LA " + pips(c["la"], c["maxla"]))
            if c.get("reaction") is not None:
                bits.append("RX " + ("●" if c["reaction"] else "○"))
            for rn, r in c["recharge"].items():
                bits.append(f"{rn}[{'ready' if r['ready'] else '··'}]")
        for tag, left in c["conds"].items():
            bits.append(tag if left is None else f"{tag}:{left}")
        line = f"{marker} {c['init']:>3}  {name:<14} " + "  ".join(b for b in bits if b)
        if c["down"]:
            line = f"{DIM}{line}{RST}"
        elif c["side"] == "enemy":
            line = f"{(BOLD + ENEMY) if c is cur else ENEMY}{line}{RST}"
        elif c is cur:
            line = f"{CUR}{BOLD}{line}{RST}"
        print(line)
    print()


# ---- dice ------------------------------------------------------------------
def roll_dice(expr):
    expr = expr.replace(" ", "").lower()
    mod = 0
    for sign in ("+", "-"):
        if sign in expr[1:]:
            i = expr.index(sign, 1)
            mod = int(expr[i:])
            expr = expr[:i]
            break
    if "d" in expr:
        n, _, faces = expr.partition("d")
        n = int(n) if n else 1
        faces = int(faces)
        rolls = [random.randint(1, faces) for _ in range(n)]
        total = sum(rolls) + mod
        detail = "+".join(map(str, rolls)) + (f"{mod:+d}" if mod else "")
        return total, detail
    return int(expr) + mod, ""


# ---- commands --------------------------------------------------------------
def cmd_add(state):
    try:
        name = input("  name: ").strip()
        if not name:
            return
        init = int(input("  init: ").strip() or 0)
        side = (input("  side [pc/enemy] (enemy): ").strip().lower() or "enemy")
        raw = {"name": name, "init": init, "side": side}
        if side != "pc":
            hp = input("  hp (blank=untracked): ").strip()
            if hp:
                raw["hp"] = int(hp)
            lr = input("  legendary resistance (0): ").strip()
            if lr:
                raw["lr"] = int(lr)
            la = input("  legendary actions (0): ").strip()
            if la:
                raw["la"] = int(la)
            rc = input("  recharge e.g. 'Roar 5-6' (blank=none): ").strip()
            if rc:
                rn, _, rspec = rc.rpartition(" ")
                raw["recharge"] = {rn: rspec}
        state.combatants.append(make_combatant(raw))
    except (ValueError, EOFError, KeyboardInterrupt):
        print("\n  add cancelled")


def handle(state, line):
    """Return True to keep looping, False to quit. Caller does snapshot/save."""
    parts = line.split()
    if not parts:
        return True
    cmd, args = parts[0].lower(), parts[1:]

    if cmd in ("q", "quit", "exit"):
        return False
    if cmd in ("h", "help", "?"):
        print(HELP)
        return True
    if cmd in ("s", "show"):
        return True  # render happens in loop
    if cmd == "undo":
        state.undo()
        return True

    if cmd in ("n", "next"):
        advance(state)
        return True

    if cmd == "add":
        cmd_add(state)
        return True

    if cmd == "roll":
        if args:
            total, detail = roll_dice(args[0])
            print(f"  {args[0]} = {total}" + (f"  ({detail})" if detail else ""))
        return True

    if cmd == "load":
        if args:
            load_into(state, args[0])
            if not args[0].endswith(".state.json"):     # an encounter -> new source
                state.source_path = os.path.abspath(args[0])
        return True
    if cmd in ("reset", "refresh"):
        if not state.source_path or not os.path.exists(state.source_path):
            print("  no source encounter to reset to — use `load FILE`")
            return True
        saved = state.undo_stack                        # keep undo across reset
        load_into(state, state.source_path)
        state.undo_stack = saved
        print(f"  reset to {os.path.basename(state.source_path)} (round 1, full)")
        return True
    if cmd == "save":
        path = args[0] if args else "combat_export.json"
        with open(path, "w") as f:
            json.dump(state.to_dict(), f, indent=2)
        print(f"  saved -> {path}")
        return True

    # everything below needs a target
    if not args:
        print("  needs a target, e.g. `d goblin 5`")
        return True
    c = state.find(args[0])
    if c is None:
        return True

    if cmd in ("d", "dmg", "damage"):
        if c["side"] == "pc":
            print(f"  {c['name']} is a PC — HP untracked; use `down {c['name']}`")
            return True
        n = int(args[1])
        c["hp"] = (c["hp"] or 0) - n
        msg = f"  {c['name']} {c['hp']+n} → {max(c['hp'],0)}"
        if c["hp"] <= 0:
            c["down"] = True
            msg += "  (DEAD)"
        print(msg)
    elif cmd in ("h", "heal"):
        if c["side"] == "pc":
            print(f"  {c['name']} is a PC — use `up {c['name']}` to revive")
            return True
        n = int(args[1])
        was = c["hp"] or 0
        c["hp"] = min((c["maxhp"] or was + n), was + n)
        if c["hp"] > 0:
            c["down"] = False
        print(f"  {c['name']} {was} → {c['hp']}")
    elif cmd == "hp":
        c["hp"] = int(args[1])
        c["maxhp"] = c["maxhp"] or c["hp"]
        c["down"] = c["hp"] <= 0
        print(f"  {c['name']} hp = {c['hp']}")
    elif cmd == "down":
        c["down"] = True
        print(f"  {c['name']} down (turns skipped)")
    elif cmd == "up":
        c["down"] = False
        print(f"  {c['name']} up")
    elif cmd == "lr":
        if c["lr"] > 0:
            c["lr"] -= 1
            print(f"  {c['name']} burns LR → {pips(c['lr'], c['maxlr'])}")
        else:
            print(f"  {c['name']} has no LR left!")
    elif cmd == "la":
        n = int(args[1]) if len(args) > 1 else 1
        if c["la"] >= n:
            c["la"] -= n
            print(f"  {c['name']} spends {n} LA → {c['la']}/{c['maxla']}")
        else:
            print(f"  {c['name']} only has {c['la']} LA!")
    elif cmd == "rla":
        c["la"] = c["maxla"]
        print(f"  {c['name']} LA refreshed → {c['la']}/{c['maxla']}")
    elif cmd in ("rx", "react", "reaction"):
        if c.get("reaction") is None:
            print(f"  {c['name']} has no tracked reaction (PC?)")
        elif c["reaction"]:
            c["reaction"] = False
            print(f"  {c['name']} uses its reaction")
        else:
            print(f"  {c['name']} has already used its reaction this round")
    elif cmd == "use":
        ab = " ".join(args[1:])
        match = next((k for k in c["recharge"] if k.lower().startswith(ab.lower())), None)
        if match:
            c["recharge"][match]["ready"] = False
            print(f"  {c['name']} uses {match} (now recharging)")
        else:
            print(f"  {c['name']} has no recharge ability '{ab}'")
    elif cmd == "ready":
        ab = " ".join(args[1:])
        match = next((k for k in c["recharge"] if k.lower().startswith(ab.lower())), None)
        if match:
            c["recharge"][match]["ready"] = True
            print(f"  {c['name']}: {match} ready")
    elif cmd == "cond":
        if len(args) < 2:
            print("  cond NAME TAG [rounds]")
            return True
        tag = args[1]
        rounds = int(args[2]) if len(args) > 2 else None
        c["conds"][tag] = rounds
        print(f"  {c['name']} +{tag}" + (f" ({rounds}r)" if rounds else ""))
    elif cmd in ("clr", "clear"):
        if len(args) > 1 and args[1] in c["conds"]:
            del c["conds"][args[1]]
            print(f"  {c['name']} -{args[1]}")
        else:
            c["conds"].clear()
            print(f"  {c['name']} conditions cleared")
    elif cmd in ("rm", "remove"):
        state.combatants.remove(c)
        print(f"  removed {c['name']}")
    else:
        print(f"  unknown command '{cmd}' — try `help`")
    return True


HELP = """\
  TURN     n / next            advance turn (auto: refresh LA, roll recharge, tick conds)
  HP       d NAME N            damage enemy (auto-down at 0)
           h NAME N            heal enemy
           hp NAME N           set current hp
  STATUS   down NAME           flag down (next skips it)
           up NAME             clear down
  LEGEND   lr NAME             spend a legendary resistance
           la NAME [N]         spend N legendary actions (default 1)
           rla NAME            manually refresh LA pool
           rx NAME             spend an enemy's reaction (refreshes on its turn)
  RECHARGE use NAME ABILITY    mark a recharge ability spent
           ready NAME ABILITY  force it ready
  CONDS    cond NAME TAG [R]   add condition (R rounds, or sticky)
           clr NAME [TAG]      remove one / all conditions
  SETUP    add                 add a combatant (prompts)
           rm NAME             remove
           load FILE           load an encounter / saved state
           reset / refresh     reload the source encounter (round 1, full)
           save [FILE]         export state
  MISC     roll XdY+Z          dice
           undo                undo last change
           s / show            reprint   ·   help   ·   q quit
  (names match by prefix: `d big 22` hits "Big Bad")"""


# ---- loading / boot --------------------------------------------------------
def load_into(state, path):
    if not os.path.exists(path):
        # convenience: allow bare name if file is right there
        print(f"  no such file: {path}")
        return
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list):                 # encounter definition -> fresh
        state.round = 1
        state.turn = 0
        state.combatants = [make_combatant(c) for c in data]
        print(f"  loaded encounter: {len(state.combatants)} combatants (round 1)")
    elif isinstance(data, dict):               # saved state -> resume
        state.round = data.get("round", 1)
        state.turn = data.get("turn", 0)
        state.combatants = [make_combatant(c) for c in data.get("combatants", [])]
        print(f"  resumed: round {state.round}, {len(state.combatants)} combatants")
    state.undo_stack.clear()


MUTATING = {"d", "dmg", "damage", "h", "heal", "hp", "down", "up", "lr",
            "la", "rla", "rx", "react", "reaction", "use", "ready",
            "cond", "clr", "clear", "n",
            "next", "add", "rm", "remove", "load", "reset", "refresh"}


def boot(state, argv):
    """Resolve the encounter/state to load and where autosave should write."""
    args = [a for a in argv if not a.startswith("-")]
    fresh = any(a in ("--fresh", "fresh", "-f") for a in argv)
    path = args[0] if args else None

    if path:
        path = os.path.abspath(path)
        base, fname = os.path.dirname(path), os.path.basename(path)
        if fname.endswith(".state.json"):                 # resume a saved state
            state.state_path = path
            guess = path[:-len(".state.json")] + ".json"  # infer source encounter
            state.source_path = guess if os.path.exists(guess) else None
            load_into(state, path)
            return
        stem = os.path.splitext(fname)[0]
        state.state_path = os.path.join(base, stem + ".state.json")
        state.source_path = path
        if os.path.exists(state.state_path) and not fresh:
            load_into(state, state.state_path)
            print("  (resumed; pass `fresh` to restart from the encounter)")
        else:
            load_into(state, path)                         # fresh from encounter
    else:                                                  # no file: cwd autosave
        state.state_path = os.path.abspath("combat_state.json")
        if os.path.exists(state.state_path):
            load_into(state, state.state_path)
            print("  (resumed from autosave)")


def main():
    state = State()
    boot(state, sys.argv[1:])
    print("combat tracker — type `help` for commands, `;` to chain, `q` to quit")
    render(state)

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        # one input line may chain several commands: `d five 15; cond cleric BI`
        segs = [s.strip() for s in line.split(";") if s.strip()]
        if not segs:
            continue
        mutating = any(s.split()[0].lower() in MUTATING for s in segs)
        if mutating:
            state.snapshot()  # one undo reverts the whole line / turn
        quitting = False
        for seg in segs:
            try:
                if not handle(state, seg):
                    quitting = True
                    break
            except (ValueError, IndexError) as e:
                print(f"  bad input: {e}")
        if mutating:
            state.autosave()
        render(state)
        if quitting:
            break
    print("bye")


if __name__ == "__main__":
    main()

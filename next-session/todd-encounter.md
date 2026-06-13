# The Todd Extraction — Philadelphia Holiday Inn (the detection encounter)

*A hidden-information cat-and-mouse, not a fight. The board is full of **unmarked minis** — sorting operators from civilians is the players' job. Escalation is gated on **detection**, not a timer. The cleaners are weak in a straight fight, so the encounter lives in **avoiding detection, protecting Todd from a needle, and getting out before a clean exit turns into a car chase.** This formalizes the table procedure: map, actors, the detection ledger, the state machine, DCs, and the injection mechanic.*

> Pairs with `todd.md` (who Todd is, the conversation, the letters, the Edmund/São Carlos payoff). **This doc is just the extraction.** Venue is now the **Philadelphia Holiday Inn**, lounge + bar, one floor.

---

## 1. The board (draw this)

One floor: **lounge + bar**, the **lobby/street** around it, and a ring of **buildings** that are stage-positions and hiding spots. Put it on a battlemat; place a *lot* of minis (below) without telling players which are which.

**Inside — the lounge/bar:**
- **The bar counter** (the **bartender-operator** behind it — the room's calm hub and the drink vector).
- **Lounge seating** — 4–5 clusters of low tables/armchairs; patrons scattered.
- **Todd's booth** — back corner, sightline to the door. **Deliberately in a camera blind wedge** (a column blocks the lounge cam). He chose it.
- **Lobby arch** → reception, elevators, the street.
- **Service corridor** behind the bar → kitchen → **back alley** exit.
- **Restroom hall** off one side (a quiet spot — and a kill-box).

**Cameras inside (mark arcs):**
| Cam | Covers | Note |
|----|----|----|
| **C1** | lobby arch | everyone in/out |
| **C2** | over the bar | the drink station |
| **C3** | lounge, wide | **column blind wedge → Todd's booth is unseen** |
| **C4** | service corridor | the back exit |
| **C5** | elevator alcove | off the lobby |

**Outside (roads + cameras + hiding spots):**
- **Front:** porte-cochère + **X1** (entrance cam), the main road, a bus shelter.
- **Side street:** the **Suburban** (driver) staged here; **X4** intersection traffic cam.
- **Back alley:** the service exit; **X3** loading-dock cam; dumpsters (cover).
- **Across the street (hiding spots / overwatch):** a **24-hr diner** (**X6** cam), a **closed dry-cleaner**, a **4-level parking structure** (the **overwatch operator's perch**, eyes on X1), a row of **townhouses**, an **ATM** (**X5** cam). The garage ramp has **X2**.

*Blind spots are the gold:* Todd's booth (C3 wedge), the back alley behind the dumpsters, the dry-cleaner doorway. PCs who find them can act without feeding a camera.

---

## 2. The actors (unmarked minis — this is the truth behind them)

**Civilians (~14 inside):** bar patrons (2 at the bar, a date in the lounge, a loud foursome, a laptop business traveler, a lone reader), a real **server**, two **front-desk** staff visible through the arch. **~3 are on their phones** (filming/streaming — mobile cameras, see §5).

**Operators (6 — only mark these on your side):**
| Op | Cover / position | Role |
|----|----|----|
| **Garrity** | businessman, lounge, drink | lead; gives the move order |
| **"Mara" — the Bartender** | staff, behind the bar | **high-Cha** room-reader + the **drink-poison** vector; last to be suspected |
| **Voss** | at the bar, "watching the game" | shooter / grabber |
| **Pike** | lounge, near the corner, **closest to Todd's booth** | **the hostage-op** (the needle on Todd) |
| **Renner** | parking structure across the street | **overwatch** — eyes on X1, phone-camera, calls the chase |
| **Driver** | Suburban, side street | exfil + chase |

**Rough stats (adjust to faceplanting):** AC 15, ~45 HP, concealed pistol +5 (2d6+3), **Stillpoint injector + 1 antidote** each. Passive Perception 13 (**Garrity 15**), Insight — **Bartender 16**. Deception: **Bartender +9, Garrity +6, others +4.** Earpieces (detection is shared instantly).

---

## 3. The detection ledger (the core mechanic)

Keep a **round counter** and a two-column ledger:

**Track A — operators who've made a PC** (the danger).
**Track B — operators a PC has made** (their progress).

### Operators detecting a PC
An operator gets a detection check on a PC who does anything noticeable in their sightline: **enters, crosses an arc, lingers/cases, approaches Todd, drinks something, or acts off.**
- **Opposed:** PC **Deception or Stealth** (Cha/Dex) **vs. the operator's passive (Perception 13 / Garrity 15 / Bartender 16 Insight).** Fail → that op flags the PC (mark Track A; **earpiece shares it instantly**).
- **A flagged PC may notice:** Perception vs the op's Stealth/Deception → success = "you clock that you've been clocked."

### PCs detecting an operator (proactively)
A PC can **study a mini** (part of a turn / a few seconds) to read it: **Insight vs the op's Deception** (Bartender 18, Garrity 16, others 14) → success = "that one's a player." Rewards casing the room before committing. *(And per your rule: any PC who gets detected immediately rolls Perception to **make the op back.**)*

### Cameras = remote detectors (delayed)
A PC who does something **overt in a camera arc** (or **on a phone**, §5) isn't seen by the room — but the footage reaches **Renner (overwatch)**, who flags them **at the top of the next round.** Avoid by routing through blind spots (**Investigation DC 13** to read the arcs, then **Stealth DC 13** to move) or by going invisible.

---

## 4. The state machine (escalation)

| State | Trigger | Operators do |
|----|----|----|
| **0 — Cold** | no PC detected | passive; scan, blend. PCs case/approach/plan. |
| **1 — One PC made** | 1 mark on Track A | quiet repositioning; **Bartender starts a drink**; earpiece chatter. No overt move. |
| **2 — THE MOVE** | **2+ PCs made**, *or* a PC makes contact with Todd (§6) | **offensive: simultaneous injection** — Pike needles **Todd**, another needles/poisons a **made PC** (§7). |
| **3 — Open conflict** | the needle lands or steel is drawn | operators fight to **secure/kill Todd & exfil**; civilians panic (crowd hazard); Renner + Driver converge. |
| **4 — Extraction** | PCs move Todd toward an exit | exits, the Suburban, the back alley. |
| **5 — Pursuit** | extraction **while detected** (§8) | covert vehicles chase → **a separate encounter.** |

---

## 5. Cameras, invisibility, spells (rulings)

- **Invisibility** (upcast hides up to 3): an invisible PC isn't seen by ops or cameras — **but breaks on attack/cast**, and physical interaction (a door, a bump) lets an adjacent op roll Perception to pinpoint. Casting *to go* invisible is itself visible if done in view.
- **Casting/attacking in a camera arc or an op's sightline = detection.** Narrate the tell: *"the air folds where you stood — dead-center on C3."*
- **Phones:** acting overtly within ~15 ft of a phone-up bystander = filmed → same as a camera (Renner sees it next round) **and** it's loose footage later. A phone is a hazard *and* a thing they can deal with (snatch it, talk the person down, blind-spot it).
- **Spell-noise tiers (rule fast):** This party has **no subtle casting.**
  - *Low-key:* **Suggestion** (looks like talking), **Disguise Self** pre-cast off-camera. Won't auto-burn them if unwitnessed.
  - *Flagrant (instant total detection + "anomaly" report → guarantees §5 pursuit and a harder one):* **Hypnotic Pattern, Dimension Door, Wild Shape, Spirit Guardians, Eldritch Blast.** They *work* — but they end the hidden game and put the operators on the radio screaming that the "dead" four are alive and *not normal.*

---

## 6. Reaching Todd + the code words

- **Banana = safe, Apple = unsafe** (pre-arranged). Todd will try to work **"apple"** into his first sentence if a PC reaches him — one round of warning that the move is coming.
- **The contact rule:** a PC who sits/speaks with Todd gets a **moment** with him — then, because Todd is watched, **an operator auto-detects that PC right after** (no roll; talking to the marked man flags you). That tips **State 2**: **Pike needles Todd, a second op needles the contact PC.** So "just walk up to Todd" buys a sentence and springs the trap.
- **False-banana (optional teeth):** if the cleaners intercepted the phone call, the **Bartender** (posing as staff) may deliver a warm **"the gentleman says it's all *banana*, he's ready for you"** — a lure. Catch it: **Insight DC 16** (her Deception is high). Biting it walks them into the booth at State 2.

---

## 7. The injection — Stillpoint (the immediate threat)

The one thing that makes detection *scary.* On the move, ops inject (touch) or serve a **poisoned drink.**
- **DC 16 Constitution save.** **Fail:** poisoned; **falls unconscious at the end of the target's 2nd turn**, then dying (reads as cardiac — deniable). **Success:** shrug it (poisoned 1 round, no KO).
- **Todd auto-fails** (frail; treat as fail, or roll at disadvantage). **One needle and he's on a 2-round clock.**
- **Cures:** **Lesser Restoration** (Sally has it), the **looted antidote** (1 per op), or *Protection from Poison.*
- **Drinks:** the Bartender can have **pre-set a poisoned drink** in front of Todd or a PC — ingesting is the save. *(Tell for sharp players: nobody should drink anything they didn't watch poured.)*
- **Why it survives the alpha strike:** **Pike sits at the booth with Todd — outside the lounge cluster.** A Hypnotic Pattern on the clustered ops **doesn't catch Pike**, and the needle still lands. The party can't AoE their way out of the hostage problem; they have to solve **the man on Todd** specifically and fast.

---

## 8. Extraction + the pursuit

- **Clean (never hit State 2):** if they get Todd out without the operators ever confirming the contacts — **no pursuit.** The reward for winning the detection game. Hard, but real.
- **Burned (State 2+ / any flagrant magic):** getting Todd to a car or the back alley **does not end it** — **covert vehicles pursue** (Driver + a second car + Renner vectoring): **a separate chase encounter** through the city grid, with the predefined buildings as break-line-of-sight options. *(Stub — build it as its own scene.)*
- **Dimension Door:** gets Todd 500 ft to a scouted blind spot — **but it's flagrant** (§5): instant detection, an "anomaly" report, **guaranteed pursuit, and a sharper one** (the operators now know what they're chasing). It's the "win the room, *buy* the chase" button — the cost is immediate (the pursuit), not bookkeeping.

---

## 9. Operator tactics (so it isn't a 1-round delete)

- **Stay spread** — never clustered; one AoE catches two at most.
- **Pike holds Todd** at the booth, apart from the others — the hostage-op (above).
- **Bartender is the hub** — best read, controls drinks, last suspected; she calls the move if Garrity's down.
- **Earpieces** → flag one PC, all know; the move is **simultaneous** (Todd + a PC) so the party can't stop both.
- **Mission priority:** Todd first (secure or needle), casters second.
- **Exfil discipline:** they fight *toward* the Suburban and Renner's overwatch, turning a fight into a chase rather than a last stand.

---

## 10. Running it (quick procedure)

1. Place all minis. Start **State 0**, round counter at 1.
2. Players declare approach (invisible? disguised? split? case first?). Resolve **camera routing** and **detection checks** as they act.
3. Each round: PCs act → for each noticeable action, roll **op detection** (Track A); offer PCs **Insight studies** (Track B) and **notice-you're-made** Perception.
4. Watch the **State table.** At **2 marks / Todd-contact**, fire **the move** (§7).
5. From State 3, run it as combat **but keep the levers live:** the poison clock on Todd, civilians/crowd, cameras/phones still recording, the exits.
6. On extraction, check **clean vs burned** → end, or roll into **the pursuit.**

*The encounter "lasts" exactly as long as they stay in the detection game. Win it quietly → a tense, bloodless extraction. Trip it → injection crisis → fight → chase. Flash big magic → straight to the hardest version. Their call, every step.*

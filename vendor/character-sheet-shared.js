(function () {
  const VERSION = 1;

  const ABILITIES = [
    { key: "str", label: "Strength", short: "STR" },
    { key: "dex", label: "Dexterity", short: "DEX" },
    { key: "con", label: "Constitution", short: "CON" },
    { key: "int", label: "Intelligence", short: "INT" },
    { key: "wis", label: "Wisdom", short: "WIS" },
    { key: "cha", label: "Charisma", short: "CHA" }
  ];

  const META_FIELDS = [
    { key: "characterName", label: "Character Name" },
    { key: "className", label: "Class" },
    { key: "subclass", label: "Subclass" },
    { key: "level", label: "Level", type: "number" },
    { key: "background", label: "Background" },
    { key: "race", label: "Race / Species" },
    { key: "playerName", label: "Player Name" }
  ];

  const SKILLS = [
    { key: "acrobatics", label: "Acrobatics", ability: "dex" },
    { key: "animalHandling", label: "Animal Handling", ability: "wis" },
    { key: "arcana", label: "Arcana", ability: "int" },
    { key: "athletics", label: "Athletics", ability: "str" },
    { key: "deception", label: "Deception", ability: "cha" },
    { key: "history", label: "History", ability: "int" },
    { key: "insight", label: "Insight", ability: "wis" },
    { key: "intimidation", label: "Intimidation", ability: "cha" },
    { key: "investigation", label: "Investigation", ability: "int" },
    { key: "medicine", label: "Medicine", ability: "wis" },
    { key: "nature", label: "Nature", ability: "int" },
    { key: "perception", label: "Perception", ability: "wis" },
    { key: "performance", label: "Performance", ability: "cha" },
    { key: "persuasion", label: "Persuasion", ability: "cha" },
    { key: "religion", label: "Religion", ability: "int" },
    { key: "sleightOfHand", label: "Sleight of Hand", ability: "dex" },
    { key: "stealth", label: "Stealth", ability: "dex" },
    { key: "survival", label: "Survival", ability: "wis" }
  ];

  const PERSONALITY_FIELDS = [
    { key: "traits", label: "Personality Traits" },
    { key: "ideals", label: "Ideals" },
    { key: "bonds", label: "Bonds" },
    { key: "flaws", label: "Flaws" }
  ];

  const ATTACK_ROWS = 4;
  const EQUIPMENT_ROWS = 7;

  const SPELL_LEVELS = [
    { key: "cantrips", label: "Cantrips", slots: false },
    { key: "level1", label: "Level 1", slots: true },
    { key: "level2", label: "Level 2", slots: true },
    { key: "level3", label: "Level 3", slots: true },
    { key: "level4", label: "Level 4", slots: true },
    { key: "level5", label: "Level 5", slots: true },
    { key: "level6", label: "Level 6", slots: true },
    { key: "level7", label: "Level 7", slots: true },
    { key: "level8", label: "Level 8", slots: true },
    { key: "level9", label: "Level 9", slots: true }
  ];

  function appBasePath(pathname) {
    if (!pathname) return "/";
    return pathname.endsWith("/") ? pathname : pathname.slice(0, pathname.lastIndexOf("/") + 1);
  }

  function storageKey(pathname) {
    return `helix:${appBasePath(pathname)}:character-sheet-v${VERSION}`;
  }

  function emptyAbilities() {
    const abilities = {};
    for (const ability of ABILITIES) abilities[ability.key] = 10;
    return abilities;
  }

  function emptySaves() {
    const saves = {};
    for (const ability of ABILITIES) saves[ability.key] = false;
    return saves;
  }

  function emptySkills() {
    const skills = {};
    for (const skill of SKILLS) skills[skill.key] = 0;
    return skills;
  }

  function emptyAttacks() {
    return Array.from({ length: ATTACK_ROWS }, function () {
      return { name: "", bonus: "", damage: "" };
    });
  }

  function emptyEquipment() {
    return Array.from({ length: EQUIPMENT_ROWS }, function () {
      return { qty: "", item: "", cost: "", weight: "" };
    });
  }

  function emptySpellbook() {
    const spellcasting = {
      className: "",
      ability: "",
      saveDcOverride: "",
      attackBonusOverride: "",
      levels: {}
    };

    for (const level of SPELL_LEVELS) {
      spellcasting.levels[level.key] = {
        spells: "",
        maxSlots: "",
        usedSlots: ""
      };
    }

    return spellcasting;
  }

  function defaultData() {
    return {
      version: VERSION,
      meta: {
        characterName: "",
        className: "",
        subclass: "",
        level: 1,
        background: "",
        race: "",
        playerName: ""
      },
      inspiration: false,
      abilities: emptyAbilities(),
      combat: {
        armorClass: "",
        initiativeBonus: "",
        speed: "",
        hpMax: "",
        hpCurrent: "",
        hpTemp: "",
        hitDice: "",
        deathSuccesses: 0,
        deathFailures: 0
      },
      saves: emptySaves(),
      skills: emptySkills(),
      personality: {
        traits: "",
        ideals: "",
        bonds: "",
        flaws: ""
      },
      attacks: emptyAttacks(),
      weaponsArmor: "",
      toolsLanguages: "",
      featuresTraits: "",
      equipment: emptyEquipment(),
      currency: {
        cp: "",
        sp: "",
        ep: "",
        gp: "",
        pp: ""
      },
      spellcasting: emptySpellbook()
    };
  }

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function normalizeNumber(value, fallback) {
    if (value === "" || value == null) return fallback;
    const numeric = Number(value);
    return Number.isFinite(numeric) ? numeric : fallback;
  }

  function numericValue(value) {
    const numeric = Number(value);
    return Number.isFinite(numeric) ? numeric : 0;
  }

  function normalizeData(input) {
    const base = defaultData();
    const source = input && typeof input === "object" ? input : {};

    const data = clone(base);
    data.version = VERSION;

    if (source.meta && typeof source.meta === "object") {
      for (const field of META_FIELDS) {
        if (field.key in source.meta) data.meta[field.key] = source.meta[field.key];
      }
    }

    data.meta.level = Math.max(1, normalizeNumber(data.meta.level, 1));
    data.inspiration = Boolean(source.inspiration);

    if (source.abilities && typeof source.abilities === "object") {
      for (const ability of ABILITIES) {
        data.abilities[ability.key] = normalizeNumber(source.abilities[ability.key], 10);
      }
    }

    if (source.combat && typeof source.combat === "object") {
      for (const key of Object.keys(data.combat)) {
        if (key in source.combat) data.combat[key] = source.combat[key];
      }
      data.combat.deathSuccesses = Math.max(0, Math.min(3, normalizeNumber(data.combat.deathSuccesses, 0)));
      data.combat.deathFailures = Math.max(0, Math.min(3, normalizeNumber(data.combat.deathFailures, 0)));
    }

    if (source.saves && typeof source.saves === "object") {
      for (const ability of ABILITIES) {
        data.saves[ability.key] = Boolean(source.saves[ability.key]);
      }
    }

    if (source.skills && typeof source.skills === "object") {
      for (const skill of SKILLS) {
        const proficiency = normalizeNumber(source.skills[skill.key], 0);
        data.skills[skill.key] = Math.max(0, Math.min(2, proficiency));
      }
    }

    if (source.personality && typeof source.personality === "object") {
      for (const field of PERSONALITY_FIELDS) {
        if (field.key in source.personality) data.personality[field.key] = source.personality[field.key];
      }
    }

    if (Array.isArray(source.attacks)) {
      data.attacks = emptyAttacks();
      source.attacks.slice(0, ATTACK_ROWS).forEach(function (attack, index) {
        if (!attack || typeof attack !== "object") return;
        data.attacks[index] = {
          name: attack.name || "",
          bonus: attack.bonus || "",
          damage: attack.damage || ""
        };
      });
    }

    if (Array.isArray(source.equipment)) {
      data.equipment = emptyEquipment();
      source.equipment.slice(0, EQUIPMENT_ROWS).forEach(function (item, index) {
        if (!item || typeof item !== "object") return;
        data.equipment[index] = {
          qty: item.qty || "",
          item: item.item || "",
          cost: item.cost || "",
          weight: item.weight || ""
        };
      });
    }

    if (source.currency && typeof source.currency === "object") {
      for (const key of Object.keys(data.currency)) {
        if (key in source.currency) data.currency[key] = source.currency[key];
      }
    }

    if (source.spellcasting && typeof source.spellcasting === "object") {
      const inputSpellcasting = source.spellcasting;
      data.spellcasting.className = inputSpellcasting.className || "";
      data.spellcasting.ability = inputSpellcasting.ability || "";
      data.spellcasting.saveDcOverride = inputSpellcasting.saveDcOverride || "";
      data.spellcasting.attackBonusOverride = inputSpellcasting.attackBonusOverride || "";

      if (inputSpellcasting.levels && typeof inputSpellcasting.levels === "object") {
        for (const level of SPELL_LEVELS) {
          const entry = inputSpellcasting.levels[level.key];
          if (!entry || typeof entry !== "object") continue;
          data.spellcasting.levels[level.key] = {
            spells: entry.spells || "",
            maxSlots: entry.maxSlots || "",
            usedSlots: entry.usedSlots || ""
          };
        }
      }
    }

    data.weaponsArmor = typeof source.weaponsArmor === "string" ? source.weaponsArmor : base.weaponsArmor;
    data.toolsLanguages = typeof source.toolsLanguages === "string" ? source.toolsLanguages : base.toolsLanguages;
    data.featuresTraits = typeof source.featuresTraits === "string" ? source.featuresTraits : base.featuresTraits;

    return data;
  }

  function load(pathname) {
    try {
      const raw = window.localStorage.getItem(storageKey(pathname || window.location.pathname));
      if (!raw) return defaultData();
      const parsed = JSON.parse(raw);
      return normalizeData(parsed);
    } catch (_error) {
      return defaultData();
    }
  }

  function save(data, pathname) {
    const normalized = normalizeData(data);
    try {
      window.localStorage.setItem(storageKey(pathname || window.location.pathname), JSON.stringify(normalized));
    } catch (_error) {
      // ignore storage failures
    }
    return normalized;
  }

  function abilityModifier(score) {
    return Math.floor((numericValue(score) - 10) / 2);
  }

  function proficiencyBonus(level) {
    return 2 + Math.floor((Math.max(1, numericValue(level) || 1) - 1) / 4);
  }

  function savingThrowBonus(data, abilityKey) {
    const normalized = normalizeData(data);
    const bonus = abilityModifier(normalized.abilities[abilityKey]);
    return bonus + (normalized.saves[abilityKey] ? proficiencyBonus(normalized.meta.level) : 0);
  }

  function skillBonus(data, skillKey) {
    const normalized = normalizeData(data);
    const skill = SKILLS.find(function (entry) { return entry.key === skillKey; });
    if (!skill) return 0;
    const rank = numericValue(normalized.skills[skillKey]);
    return abilityModifier(normalized.abilities[skill.ability]) + proficiencyBonus(normalized.meta.level) * rank;
  }

  function passivePerception(data) {
    return 10 + skillBonus(data, "perception");
  }

  function initiativeTotal(data) {
    const normalized = normalizeData(data);
    return abilityModifier(normalized.abilities.dex) + numericValue(normalized.combat.initiativeBonus);
  }

  function spellcastingAbilityModifier(data) {
    const normalized = normalizeData(data);
    const abilityKey = normalized.spellcasting.ability;
    if (!abilityKey) return 0;
    return abilityModifier(normalized.abilities[abilityKey]);
  }

  function spellSaveDc(data) {
    const normalized = normalizeData(data);
    if (normalized.spellcasting.saveDcOverride !== "") return numericValue(normalized.spellcasting.saveDcOverride);
    if (!normalized.spellcasting.ability) return 0;
    return 8 + proficiencyBonus(normalized.meta.level) + spellcastingAbilityModifier(normalized);
  }

  function spellAttackBonus(data) {
    const normalized = normalizeData(data);
    if (normalized.spellcasting.attackBonusOverride !== "") return numericValue(normalized.spellcasting.attackBonusOverride);
    if (!normalized.spellcasting.ability) return 0;
    return proficiencyBonus(normalized.meta.level) + spellcastingAbilityModifier(normalized);
  }

  function totalEquipmentWeight(data) {
    const normalized = normalizeData(data);
    return normalized.equipment.reduce(function (sum, entry) {
      const quantity = numericValue(entry.qty || 0);
      const weight = numericValue(entry.weight || 0);
      return sum + quantity * weight;
    }, 0);
  }

  window.HELIX_CHARACTER_SHEET = {
    VERSION: VERSION,
    ABILITIES: ABILITIES,
    META_FIELDS: META_FIELDS,
    SKILLS: SKILLS,
    PERSONALITY_FIELDS: PERSONALITY_FIELDS,
    SPELL_LEVELS: SPELL_LEVELS,
    ATTACK_ROWS: ATTACK_ROWS,
    EQUIPMENT_ROWS: EQUIPMENT_ROWS,
    defaultData: defaultData,
    normalizeData: normalizeData,
    load: load,
    save: save,
    storageKey: storageKey,
    appBasePath: appBasePath,
    abilityModifier: abilityModifier,
    proficiencyBonus: proficiencyBonus,
    savingThrowBonus: savingThrowBonus,
    skillBonus: skillBonus,
    passivePerception: passivePerception,
    initiativeTotal: initiativeTotal,
    spellSaveDc: spellSaveDc,
    spellAttackBonus: spellAttackBonus,
    totalEquipmentWeight: totalEquipmentWeight
  };
})();

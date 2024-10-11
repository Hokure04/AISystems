templates = [
    {
        "pattern": r'является ли (.+) главным героем',
        "query": lambda name: f"is_main_character({name.strip()})."
    },
    {
        "pattern": r'является ли (.+) финальным боссом',
        "query": lambda name: f"is_final_boss({name.strip()})."
    },
    {
        "pattern": r'является ли (.+) боссом',
        "query": lambda name: f"is_boss({name.strip()})."
    },
    {
        "pattern": r'сколько способностей у (.+)',
        "query": lambda name: f"count_abilities({name.strip()}, Count)."
    },
    {
        "pattern": r'какие существуют персонажи',
        "query": lambda _: "character(X)."
    },
    {
        "pattern": r'какие персонажи являются боссами',
        "query": lambda _: "is_boss(X)."
    },
    {
        "pattern": r'какие персонажи являются странниками',
        "query": lambda _: "wanderer(X)."
    },
    {
        "pattern": r'у каких персонажей высокий уровень здоровья',
        "query": lambda _: "high_health(X)."
    },
    {
        "pattern": r'какие способности есть у (.+)',
        "query": lambda name: f"have({name.strip()}, Ability)."
    },
    {
        "pattern": r'кого одолел (.+)',
        "query": lambda name: f"defeated_by(Foe, {name.strip()})."
    },
    {
        "pattern": r'кто одолел (.+)',
        "query": lambda name: f"defeated_by({name.strip()}, Foe)."
    },
    {
        "pattern": r'сколько персонажей победил (.+)',
        "query": lambda name: f"findall(Enemy, defeated_by(Enemy, {name.strip()}), List), length(List, Count)."
    },
    {
        "pattern": r'кто является союзником для (.+)',
        "query": lambda name: f"is_ally({name.strip()}, Ally)."
    }
]

character_translation = {
    "рыцарь": "knight",
    "ложный рыцарь": "false_knight",
    "хорнет": "hornet",
    "лорды богомолов": "mantis_lords",
    "мастер душ": "soul_master",
    "носк": "nosk",
    "коллекционер": "collector",
    "предавший лорд": "betrayed_lord",
    "пропавший собрат": "lost_brother",
    "тремоматка": "trem_mother",
    "навозный защитник": "dung_guard",
    "полый рыцарь": "hollow_knight",
    "изельда": "iselda",
    "слай": "sly",
    "пожиратель ног": "foot_eater",
    "могучий зот": "mighty_zot",
    "квирелл": "quirell",
    "тряпочка": "cloth",
    "тисо": "tiso",
    "сияние": "effulgence"
}
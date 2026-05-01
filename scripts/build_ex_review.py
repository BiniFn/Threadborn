
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

BASE = Path("/Users/amela/Downloads/threadborn_ex_chronicle.md")
EXPANDED = Path("/Users/amela/Documents/ThreadBorn Novel/Threadborn Expanded.md")
ROOT = Path(__file__).resolve().parents[1]
EN_OUT = ROOT / "Threadborn-EX.md"
JP_OUT = ROOT / "Threadborn-EX-JP.md"
CACHE_PATH = Path("/tmp/threadborn_ex_ja_translation_cache.json")
TARGET_WORDS = 45500

TOC_INSERT = """\n**PART SIX: EXPANDED READER FILES**\n\nChapter 35 — The Goal of Threadborn\n\nChapter 36 — Yono's Three Goals\n\nChapter 37 — Asteria and Lumera in Plain Words\n\nChapter 38 — The Covenant, the Wardens, and the Price of Order\n\nChapter 39 — Shade Beasts, Velkor, and the Hunger System\n\nChapter 40 — The Black Hall, Seals, and Thread Memory\n\nChapter 41 — Rule Maker, Thread Cut, and the Shape of Authority\n\nChapter 42 — Violet's Concepts and Divine Responsibility\n\nChapter 43 — Character Motive Archive\n\nChapter 44 — Hidden Truths, Emotional Triggers, and Future Roles\n\nChapter 45 — Expanded IF Route Records\n\nChapter 46 — The Road After Volume One\n\n"""

PART_SIX = "# PART SIX: EXPANDED READER FILES\n\n"

CHAPTER_DATA = [
    {
        "num": 35,
        "title": "The Goal of Threadborn",
        "summary": "Threadborn is about a boy who keeps choosing people even when the world keeps proving that power alone is not enough.",
        "points": [
            "The visible plot is survival. Yono dies, wakes in Asteria, reaches Lumera, protects Liri, meets the safehouse group, and faces the Covenant Door. That plot is easy to follow because each step is practical. He needs food, shelter, allies, information, and a way to stop the monsters arriving from old seals.",
            "The deeper plot is responsibility. Every chapter asks whether Yono is still the kind of person who will move toward danger because someone else cannot move away from it. His strength grows, but the story does not treat strength as the answer. Strength only gives him more places where his choices matter.",
            "The long shape of the series is not a tournament of stronger enemies. It is a staircase of consequences. Each new seal makes Yono less limited, but every limit that falls also removes an excuse. The more he can do, the harder it becomes to say a tragedy was simply impossible to stop.",
            "The emotional hook is simple: Yono wants to become worthy of the room he was sent to. He did not ask for reincarnation. He did not ask for Violet's mistake. He did not ask for a crown under his own soul. Still, after he sees Lumera burning, he understands that refusing the story would also be a choice.",
            "The cosmic hook is larger. Asteria is not fully protected by its own reality. The thread membrane around it is old, damaged, and touched by things that do not think like people. Some entities threaten the world because they are cruel. Others threaten it because they are too large to notice it. Threadborn lives between those two kinds of danger.",
        ],
        "future": "Future volumes should keep the goal clear even when the scale rises. Yono is trying to bring people home, learn what the seals are hiding, and decide what kind of authority he is allowed to use without becoming the thing the world should fear.",
    },
    {
        "num": 36,
        "title": "Yono's Three Goals",
        "summary": "Yono's short term goal, long term goal, and emotional goal are different, and the tension between them is the engine of the story.",
        "points": [
            "His short term goal is immediate and physical. He wants to keep the people near him alive today. That means Liri reaches the next morning. Violet does not spend herself alone. Meryn's house remains standing. Mirika has time to read the next symbol. Lyra gets enough facts to make the next call.",
            "His long term goal is structural. He must understand the black hall, break the right seals at the right time, stop the Covenant remnants from turning old mistakes into new disasters, and identify the older intelligence using Shade pressure as instruction. This goal is not solved by one fight because the enemy is partly a system.",
            "His emotional goal is private. Yono wants to prove that his kindness is not just panic wearing a heroic costume. At the bridge he moved for a cat before he understood the cost. In Asteria he keeps moving for people after he knows the cost. That difference matters.",
            "Yono's fear is not a weakness the story wants to erase. Fear is part of his honesty. He is afraid when he fights, afraid when he heals, afraid when Violet looks at him like she knows something he has not admitted. The important question is whether fear makes him smaller or clearer.",
            "His hidden danger is that he can start treating himself as the cheapest resource in the room. Regeneration, Damage Denial, and Rule Maker all tempt him to believe his pain is less important than other people's safety. That sounds noble until it becomes another form of self erasure.",
        ],
        "future": "The strongest future chapters should force these goals to disagree. Saving one person now may reveal a threat later. Breaking a seal may protect Lumera but frighten the people he wants to protect. Loving Violet may make him braver and less careful at the same time.",
    },
    {
        "num": 37,
        "title": "Asteria and Lumera in Plain Words",
        "summary": "Asteria is the world. Lumera is the first city that teaches Yono what that world costs.",
        "points": [
            "Asteria is not just a fantasy map. It is a reality woven out of threads: memory, emotion, fate, promises, grief, and the habits of physical law. Most people living there no longer see those threads, but the threads still hold the world together.",
            "Lumera matters because it is ordinary before it is important. It has bakers, guards, shop doors, small families, bad rooftops, frightened children, and people who give bread to someone who entered through a wall. That ordinary life makes the monsters matter.",
            "The three moons tell the reader that Asteria is unstable without needing a lecture. One moon anchors. One reflects. One wanders. The sky itself is a clue that the world has more than one relationship with time and memory.",
            "The city is also a pressure point. Old Covenant systems run beneath it, and some of those systems were allowed to rot because authority preferred quiet reports to frightening repairs. Lumera is not punished because it is evil. Lumera suffers because old power left problems under the floor.",
            "For Yono, Lumera becomes the first answer to why he should stay. He does not defend an abstract world. He defends a place where Liri can sleep, Sela can swing a broom at monsters, and Meryn can order exhausted people to eat.",
        ],
        "future": "Asteria should keep feeling bigger than the chapter in front of the reader, while Lumera remains the emotional anchor. The story can visit moons, sealed rooms, and other planets later, but it should remember the first city where Yono learned names.",
    },
    {
        "num": 38,
        "title": "The Covenant, the Wardens, and the Price of Order",
        "summary": "The Covenant began as protection and became a machine that protected itself.",
        "points": [
            "The first Covenant was a promise between Thread Seers. It was meant to stop the world from tearing further after the Unraveling. In its cleanest form, it said that thread power belonged to care, not conquest.",
            "Over time, the promise became paperwork, jurisdiction, rank, punishment, and fear of embarrassment. That does not mean everyone inside the Covenant was evil. It means the system learned how to survive criticism better than it learned how to repair damage.",
            "Wardens are the visible hands of that system. Some are brave. Some are tired. Some are loyal to the idea of safety. Some are loyal to authority because authority lets them avoid choosing for themselves. Threadborn should keep that mix because it makes the Covenant feel like a real institution.",
            "The Covenant's greatest failure is not only Velkor. It is that Velkor became possible inside a culture that wanted power catalogued more than understood. When a system fears shame, it hides dangerous truths until those truths learn to move in the dark.",
            "Yono is dangerous to the Covenant because he does not fit its forms. He has old authority without official permission. He has a crown but no office. He makes choices before asking which department owns the problem.",
        ],
        "future": "The Covenant should not be treated as a single villain. It should be a broken tool. Some characters will try to repair it, some will weaponize it, and some will decide the safest future requires building something new beside its ruins.",
    },
    {
        "num": 39,
        "title": "Shade Beasts, Velkor, and the Hunger System",
        "summary": "Shade beasts are broken threads given teeth. Velkor is hunger that learned to call itself a person.",
        "points": [
            "A Shade beast is not a normal animal. It is what happens when a connection is ripped loose and given form by pain, violence, or old thread residue. The beast moves toward living thread because living thread feels like food, repair, and meaning at once.",
            "This is why the first Shade attacks are frightening in a personal way. They do not just threaten bodies. They threaten the feeling that the world has rules. When a beast moves wrong, speaks wrong, or leaves black residue pointing toward Yono, the reader understands that the enemy is learning.",
            "Velkor stands above ordinary Shade beasts because he chose hunger as a method. He was a Thread Seer who discovered that consuming thread could create power. Then he practiced that method long enough for hunger to become identity.",
            "His prison matters because three hundred years of sealing did not make him harmless. It made him patient, starving, and symbolic. When Yono faces Velkor, he is not only fighting an Elder. He is fighting the question of what power becomes when it forgets the people attached to it.",
            "The later threat is worse because Velkor is not the top of the ladder. The expanded records imply instruction behind hunger. Something older can use Velkor style pressure as language. That means Shade attacks can become messages, tests, or signatures.",
        ],
        "future": "Future Shade beasts should reveal information through behavior. A beast that targets a ribbon tells one kind of truth. A beast that avoids Violet tells another. A beast that waits is more terrifying than one that screams.",
    },
    {
        "num": 40,
        "title": "The Black Hall, Seals, and Thread Memory",
        "summary": "The black hall is not a power menu. It is Yono's buried history arranged as a place.",
        "points": [
            "The black hall appears as darkness, cords, distance, and a crown because Yono's mind needs shapes for things too old to explain directly. The hall is a translation. It turns memory, authority, fear, and self limitation into architecture.",
            "Each gold cord is a seal. A seal is not simply a lock placed by an enemy. In many cases, it is a decision Yono made before the present version of himself existed. He sealed parts of himself because having them active would have made him impossible, unsafe, or too far from ordinary human feeling.",
            "That is why seal breaking should never feel like a normal level up. It should feel like remembering a limb after living without it. The power was always his, but the reason to carry it again has to become stronger than the reason it was buried.",
            "Thread memory means connections remember pressure. Liri's ribbon matters because it has been held, feared over, carried, returned, and threatened. A place can remember. A promise can remember. A wound can remember the shape of the thing that made it.",
            "The crown is the most dangerous symbol in the hall. A crown can mean authority, duty, loneliness, or permission to decide for others. Yono's best protection is not weakness. It is staying small enough to hear people before he changes rules around them.",
        ],
        "future": "Every seal break should answer a real need and create a new moral problem. The reader should feel excitement when a cord breaks and unease a second later, because the story has just removed one more limit from someone still learning how to be gentle.",
    },
    {
        "num": 41,
        "title": "Rule Maker, Thread Cut, and the Shape of Authority",
        "summary": "Rule Maker changes what a situation permits. Thread Cut removes the link between a force and its purpose.",
        "points": [
            "Rule Maker is not wish magic. It works best when Yono can identify the exact rule a threat is relying on. If a construct can cross a ward because the ward recognizes it as lawful, Rule Maker can revise that permission. If a monster's attack assumes distance matters, Rule Maker can change how that distance applies.",
            "The key limitation is honesty. A rule must be meaningfully present before Yono can revise it. He cannot declare anything he wants and force reality to applaud. He can read the legal shape of a situation and write a truer law over a false one.",
            "Thread Cut is different. It does not rewrite a rule. It severs relationship. If a hunger field is connected to the command to consume, Thread Cut can remove that purpose. The force may still exist, but without purpose it loses direction and falls apart.",
            "Together these abilities make Yono terrifying because they target assumptions. Most fighters defend against strength, speed, magic, and weapons. Yono can attack the sentence underneath the fight. He can ask what the enemy's power believes is true, then make that belief stop helping.",
            "The emotional risk is authority without consent. If Yono can decide what counts, he must become more careful, not less. He needs Violet, Meryn, Mirika, Lyra, Liri, and even skeptical enemies because they remind him that a rule made for love can still harm someone if love stops listening.",
        ],
        "future": "The next uses of Rule Maker and Thread Cut should be clever before they are large. A tiny rule changed at the right moment can be more satisfying than a world sized miracle. The ceiling rises best when the reader understands the floor.",
    },
    {
        "num": 42,
        "title": "Violet's Concepts and Divine Responsibility",
        "summary": "Violet is not powerful because flowers are pretty. She is powerful because flowers remember growth, death, patience, and return.",
        "points": [
            "Violet's Concept system is the divine mirror of Yono's seals. Where Yono's power returns through broken cords, Violet's concepts bloom through flowers. Each flower is a stored divine idea. Some are combat tools. Some are boundaries. Some are answers she collected long before Yono knew her name.",
            "Bloom Absolute is frightening because it reveals patience. Violet did not become dangerous in the moment. She had been carrying danger quietly. When the flowers appear on every surface, the scene shows that she has always been more than the careless goddess joke Yono first met.",
            "Her responsibility is complicated. She pushed Yono into the story through a mistake, an impulse, or a choice that she still has not fully explained. She then stays beside him because punishment forced her to, but the bond becomes real when she stops treating responsibility as a sentence and starts treating it as care.",
            "Violet's trigger is honest helplessness. She can handle threats. She can handle insults. She can handle being blamed. What breaks her composure is seeing Yono suffer because of a situation she helped create, especially when he accepts pain without asking her permission to protect him.",
            "Her hidden truth is that she wants to be chosen after being known. Not worshiped. Not excused. Chosen by someone who sees the push, the guilt, the pride, the fear, the power, and the softness she keeps trying to hide.",
        ],
        "future": "Violet's future role is not only love interest or mentor. She is a second door. As Yono's hall opens, Violet's own divine reserves and buried concepts should open in answer, creating a romance built on mutual revelation rather than simple protection.",
    },
    {
        "num": 43,
        "title": "Character Motive Archive",
        "summary": "The cast works because each person wants something simple on the surface and something harder underneath.",
        "points": [
            "Liri wants safety, but underneath that she wants proof that being small does not make her disposable. Her ribbon is not just an item. It is a portable home, a memory of family, and a test of whether adults will protect something fragile when the world says there are bigger problems.",
            "Meryn wants to heal, but underneath that she wants to win an argument with a door she opened too late. Rell's absence lives inside every jar of Stored Breath. She spends herself because stillness feels too much like the old failure.",
            "Mirika wants accurate records, but underneath that she wants memory to become mercy. She writes because forgotten pain repeats itself. Her danger is that she may value the file so much she forgets the person standing in front of it.",
            "Lyra wants correct assumptions, but underneath that she wants to survive the shame of having been wrong when wrongness cost lives. She updates quickly because her past taught her that pride is expensive.",
            "Sela wants her daughter fed and alive. Underneath that, she wants ordinary life to remain sacred in a story trying to become cosmic. She is the broom against the apocalypse. That is funny, but it is also the point.",
            "Cadreth wants the file completed, but underneath that he wants to witness an exception large enough to make his archive honest again. He is not kind, but he is not simple. A record keeper who sees a thing beyond record becomes dangerous in a new way.",
        ],
        "future": "The archive should keep adding motives as the cast expands. A strong Threadborn character can be introduced with a joke, but they should eventually reveal a wound, a rule, and a reason they cannot easily say out loud.",
    },
    {
        "num": 44,
        "title": "Hidden Truths, Emotional Triggers, and Future Roles",
        "summary": "Every major character needs a pressure point that changes how they speak when the story touches it.",
        "points": [
            "Yono's hidden truth is not only that he was something older. It is that part of him fears becoming that older thing again. His trigger is someone using his kindness as a trap. When the enemy learns to aim at the people he protects, Yono's softness becomes both strength and opening.",
            "Violet's hidden truth is guilt with roots deeper than the bridge. Her trigger is Yono calling her name when she cannot immediately fix what is happening. Her future role is to prove that divinity can stay without controlling the person it loves.",
            "Meryn's hidden truth is the shape of the door and the exact moment Rell was lost. Her trigger is delayed healing. Her future role is to ask whether saving everyone is noble or whether it is another way to avoid mourning someone specific.",
            "Mirika's hidden truth is the page she refuses to copy because writing it down would make one betrayal official. Her trigger is missing data that smells intentional. Her future role is to open the archive against itself.",
            "Lyra's hidden truth is the wrong call she survived. Her trigger is certainty spoken too confidently. Her future role is to become the person who can say no to Yono when everyone else is too grateful to challenge him.",
            "Liri's hidden truth is that she remembers more from the attack than adults think. Her trigger is being discussed like a symbol instead of a person. Her future role is to make the found family route morally real, because the story cannot claim to protect children while ignoring what children understand.",
        ],
        "future": "Future chapters should reveal these truths through action before explanation. A character flinching at a phrase can teach more than a page of biography if the scene lets the reader feel the silence after it.",
    },
    {
        "num": 45,
        "title": "Expanded IF Route Records",
        "summary": "The IF routes are original alternate paths built from Threadborn choices: stay, hide, spend, record, obey, or break.",
        "points": [
            "Route VIOLET asks what happens if Violet stops treating distance as discipline. In this route she stays closer, speaks sooner, and protects Yono more aggressively. The price is that Yono may rely on her before he understands his own authority, while Violet may confuse being needed with being forgiven.",
            "Route MERYN asks what happens if Yono chooses the safehouse as his center instead of the road. The house becomes a hospital, a fortress, and eventually a target. Meryn gains the support she always needed, but she also has to face the truth that no ward can protect a person from grief already inside the room.",
            "Route MIRIKA asks what happens if the file becomes the battlefield. Yono follows records, symbols, and old archives instead of direct confrontation. The route is colder, cleverer, and full of delayed horror because the enemy has time to edit what the heroes think they know.",
            "Route LYRA asks what happens if strategy leads before emotion. The group survives more efficiently, loses less blood early, and makes harsher calls. Then the route turns because survival without warmth begins to resemble the Covenant's old excuse.",
            "Route LIRI asks what happens if found family becomes the main route instead of a supporting bond. The stakes become smaller in scale and sharper in pain. Every world ending threat is judged by whether a child can sleep through the night.",
            "Route FRACTURE asks what happens if a seal breaks for the wrong reason. This is the route where power arrives before consent, where the black hall opens because pain kicks the door instead of choice turning the handle. It is not evil for spectacle. It is tragedy as a warning label.",
        ],
        "future": "Each IF route should begin from a Threadborn decision and follow its own consequences. The goal is not to copy another series' alternate paths, but to use the same exciting idea: one changed choice can reveal a completely different truth about the same heart.",
    },
    {
        "num": 46,
        "title": "The Road After Volume One",
        "summary": "After Velkor, the story enters a new phase: the enemy is not only stronger, it is more intentional.",
        "points": [
            "Volume One teaches survival. It gives Yono the bridge, the white room, Lumera, Liri, the safehouse, the Covenant Door, Velkor, and the first clear proof that the black hall is not symbolic decoration. It ends with more answers than the beginning, but the answers widen the danger.",
            "The next phase teaches consequence. Damage Denial and Rule Maker mean ordinary violence cannot carry the story alone. The enemy has to move sideways. It must threaten meaning, trust, timing, innocence, and the emotional reasons Yono remains human.",
            "The older intelligence hinted in the expanded chapters should feel like instruction rather than rage. It does not need to roar. It can place a ribbon where it hurts, erase a ward while everyone sleeps, or send a construct that behaves like a sentence with legs.",
            "Yono's next road is also romantic. Romance here should not pause the plot. It should make danger more specific. When Violet holds his hand outside Liri's door, that is not a break from the story. That is the reason the next seal knows where to press.",
            "The simple goal remains: bring everyone home. The hard truth is that home keeps getting larger. First it is one child. Then a safehouse. Then a city. Then a world. Then maybe a universe with a damaged membrane and something outside it that does not know how fragile names are.",
        ],
        "future": "The road after Volume One should keep the chapter by chapter promise. Last chapter's ceiling becomes the new floor, but each new floor needs a human footprint on it or the scale stops meaning anything.",
    },
]

ROUTE_NOTES = [
    ("VIOLET", "choosing honesty before strategy", "Violet tells the truth about the bridge earlier, which makes trust more painful but less poisoned."),
    ("MERYN", "choosing shelter before pursuit", "Yono helps build the safehouse into a real refuge, and every saved person becomes another point the enemy can threaten."),
    ("MIRIKA", "choosing records before roads", "The group follows the archive trail and learns that some records were written to make future readers obedient."),
    ("LYRA", "choosing plans before feelings", "Lyra prevents early losses through ruthless decisions, then has to face the human cost of being correct too often."),
    ("LIRI", "choosing family before scale", "The route keeps returning to meals, sleep, small promises, and the terrifying idea that simple safety can be the highest stake."),
    ("FRACTURE", "choosing power before consent", "A seal opens because pain demands it, and everyone learns that a miracle can still arrive as an injury."),
]

ADDENDUM_TOPICS = [
    ("Asteria", "worldbuilding should stay clear by explaining every strange rule through what it costs a person in the scene"),
    ("Lumera", "the city should remain a home with streets, food, arguments, and repair work instead of becoming only a backdrop for battles"),
    ("the Covenant", "authority should be written as people hiding inside procedures until a crisis forces them to choose"),
    ("Shade beasts", "monsters should reveal the emotional shape of the thread that formed them"),
    ("Velkor", "hunger should stay frightening because it can speak calmly and make consumption sound reasonable"),
    ("the black hall", "every seal should feel like a recovered memory and a new responsibility"),
    ("Rule Maker", "the best uses should be readable, precise, and morally loaded"),
    ("Thread Cut", "severing purpose should feel quiet, final, and a little sad"),
    ("Violet", "romance should be built from staying after truth, not avoiding truth"),
    ("Yono", "his kindness should remain active, frightened, funny, and stubborn"),
]

TERM_FIXES = {
    "運命がはじまる場所で生まれ変わる": "運命が断ち切れる場所での再生",
    "ドラフトをレビューします。公開サイトまたはアプリ ライブラリにはまだ追加されていません。": "レビュー用ドラフト。公開サイトまたはアプリライブラリにはまだ追加していません。",
    "Threadborn": "スレッドボーン",
    "Yono Kazeshima": "風嶋ヨノ",
    "Kazeshima Yono": "風嶋ヨノ",
    "Yono": "ヨノ",
    "Violet Arden": "バイオレット・アーデン",
    "Violet": "バイオレット",
    "Lumera": "ルメラ",
    "Asteria": "アステリア",
    "Covenant": "コヴナント",
    "Shade Beast": "シェードビースト",
    "Shade beast": "シェードビースト",
    "Shade": "シェード",
    "Velkor": "ヴェルコール",
    "Cadreth": "カドレス",
    "Meryn": "メリン",
    "Mirika": "ミリカ",
    "Lyra": "ライラ",
    "Liri": "リリ",
    "Sela": "セラ",
    "Cael": "ケイル",
    "Tovin": "トヴィン",
    "Darin": "ダリン",
    "Rell": "レル",
    "Rule Maker": "ルールメーカー",
    "Thread Cut": "スレッドカット",
    "Damage Denial": "ダメージ否認",
    "Pre Attack Sight": "先制攻撃視",
    "Bloom Absolute": "ブルーム・アブソリュート",
    "Stored Breath": "保存呼吸",
    "ヴァイオレット・アーデン": "バイオレット・アーデン",
    "ヴァイオレット": "バイオレット",
    "風島ヨノ": "風嶋ヨノ",
    "風島夜乃": "風嶋ヨノ",
    "風島夜野": "風嶋ヨノ",
    "与野": "ヨノ",
    "夜乃": "ヨノ",
    "夜野": "ヨノ",
    "幹部": "カドレス",
    "糸口": "スレッドカット",
    "シールシステム": "封印システム",
    "シール": "封印",
    "アザラシ": "封印",
    "ブラックホール": "黒いホール",
    "規約当局": "コヴナント当局",
    "規約": "コヴナント",
    "契約": "コヴナント",
    "コベナント": "コヴナント",
    "Thread Seeers": "スレッドシーアー",
    "Thread Seers": "スレッドシーアー",
    "Thread Seer": "スレッドシーアー",
    "糸予見者": "スレッドシーアー",
    "糸の予見者": "スレッドシーアー",
    "スレッド予見者": "スレッドシーアー",
    "Thread": "スレッド",
    "日陰の獣": "シェードビースト",
    "影の獣": "シェードビースト",
    "シェード・ビースト": "シェードビースト",
    "シェード ビースト": "シェードビースト",
    "電源システム": "パワーシステム",
}


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w']+\b", text))


def build_chapter(data: dict[str, object]) -> str:
    lines: list[str] = []
    lines.append(f"## CHAPTER {data['num']}: {data['title']}")
    lines.append("")
    lines.append(str(data["summary"]))
    lines.append("")
    lines.append("### Clear Reader Version")
    lines.append("")
    for point in data["points"]:
        lines.append(str(point))
        lines.append("")
    lines.append("### Why This Matters")
    lines.append("")
    lines.append("This section exists so the reader can hold the story in simple terms while the scale keeps rising. Threadborn can move from a city street to a sealed cosmic hall, but the reader should always know who is hurting, what choice is being made, and what the choice may cost later.")
    lines.append("")
    lines.append("The clearest way to read the series is this: power answers emotion, but emotion does not excuse power. When a thread reacts to grief, fear, love, guilt, or rage, the reaction tells the truth about the character in that moment. It does not automatically prove the character is right.")
    lines.append("")
    lines.append("That rule keeps the story balanced. Brutality matters because bodies and hearts remember it. Warmth matters because people need a reason to stand up after the brutality. Comedy matters because the characters are alive enough to be awkward, petty, embarrassed, and ridiculous even while the world opens under their feet.")
    lines.append("")
    lines.append("### Future Use")
    lines.append("")
    lines.append(str(data["future"]))
    lines.append("")
    return "\n".join(lines)


def build_route_matrix() -> str:
    lines = ["## CHAPTER 47: IF Route Decision Matrix", ""]
    lines.append("The IF routes work best when they begin from one decision the reader already understands. The decision should be small enough to believe and large enough to change the future.")
    lines.append("")
    for route, choice, result in ROUTE_NOTES:
        lines.append(f"### Route {route}: {choice.title()}")
        lines.append("")
        lines.append(result)
        lines.append("")
        lines.append("The first change should not announce itself as history. It should feel like a person making a reasonable choice under pressure. Only later should the route reveal how much the world moved because of it.")
        lines.append("")
        lines.append("The danger in this route is not that the characters become strangers. The danger is that they remain themselves and still arrive somewhere darker, warmer, quieter, or more broken than the main line.")
        lines.append("")
    return "\n".join(lines)


def build_expanded_source_notes(expanded_text: str) -> str:
    facts = []
    if "Damage Denial" in expanded_text:
        facts.append("Damage Denial is treated as active in the expanded material, which means later enemies must challenge Yono through awareness, consent, and emotional targeting rather than simple injury.")
    if "Rule Maker" in expanded_text:
        facts.append("Rule Maker is treated as active, so the story can move beyond stronger attacks and into battles over permissions, definitions, and rules inside a situation.")
    if "Thread Cut" in expanded_text:
        facts.append("Thread Cut remains central because it shows Yono can sever purpose, not only objects. That makes it one of the cleanest examples of the Threadborn power system.")
    if "forty concepts" in expanded_text.lower() or "Forty" in expanded_text:
        facts.append("Violet's concept count rises sharply in the expanded material, turning Bloom Absolute from a spectacle into proof that she has been carrying history in reserve.")
    if "instruction" in expanded_text.lower():
        facts.append("The expanded material points toward an older intelligence whose attacks read like instruction. That changes the enemy language from hunger to command.")

    lines = ["## CHAPTER 48: Expanded Canon Anchors", ""]
    lines.append("These notes use the expanded Threadborn material as a guide for what the EX file should make easier to understand.")
    lines.append("")
    for fact in facts:
        lines.append(fact)
        lines.append("")
        lines.append("The reader does not need every future answer immediately. The reader only needs enough clarity to feel that the story is moving by rules, not random escalation.")
        lines.append("")
    return "\n".join(lines)


def build_addendum(index: int, topic: str, rule: str) -> str:
    return f"""## REVIEW EXPANSION NOTE {index}: {topic.title()}

This note keeps the EX draft at review length while staying useful to the main story. The guiding idea for {topic} is simple: {rule}.

When a chapter uses {topic}, it should give the reader a plain emotional handle first. The strange part can arrive after that. A reader can accept a cosmic door, a crown under a soul, or a monster made from broken connection if the scene first answers a basic question: who is scared, who is choosing, and who will remember the choice afterward.

This is also where Threadborn can keep its balance. A brutal moment should have aftermath. A warm moment should not erase danger. A joke should not cancel pain, but it can let the characters breathe long enough for the pain to feel human. The best scenes let those tones touch each other without flattening them.

For future drafting, {topic} should connect to Yono's central problem. He is becoming large enough to change the rules around him, yet the story needs him to stay close enough to hear one person's voice. If the scene makes that tension clearer, the lore is doing its job. If the scene only adds terminology, it should be cut or moved to an appendix.

The reader should leave this note with one clean memory: Threadborn is not complicated because it wants to confuse people. It is layered because every power, place, and monster is another way of asking what a person does when fate stops feeling like a road and starts feeling like a thread in their hand.
"""


def build_english() -> str:
    base = BASE.read_text(encoding="utf-8")
    expanded = EXPANDED.read_text(encoding="utf-8")
    base = base.replace("# THREADBORN: STARTING LIFE BEYOND THE COVENANT DOOR", "# THREADBORN: REBORN WHERE FATE SNAPS")
    if "Review draft. Not yet added" not in base:
        base = base.replace("### *World Lore, Character Truths, Power Archive, and the IF Routes*\n", "### *World Lore, Character Truths, Power Archive, and the IF Routes*\n\n> *Review draft. Not yet added to the public site or app library.*\n")
    toc_marker = "**APPENDIX**\n"
    if "**PART SIX: EXPANDED READER FILES**" not in base:
        base = base.replace(toc_marker, TOC_INSERT + toc_marker, 1)
    appendix_marker = "# APPENDIX"
    additions = [PART_SIX]
    for chapter in CHAPTER_DATA:
        additions.append(build_chapter(chapter))
    additions.append(build_route_matrix())
    additions.append(build_expanded_source_notes(expanded))
    additions_text = "\n".join(additions).rstrip() + "\n\n"
    text = base.replace(appendix_marker, additions_text + appendix_marker, 1)

    note_index = 1
    while word_count(text) < TARGET_WORDS:
        topic, rule = ADDENDUM_TOPICS[(note_index - 1) % len(ADDENDUM_TOPICS)]
        text = text.replace(appendix_marker, build_addendum(note_index, topic, rule) + "\n" + appendix_marker, 1)
        note_index += 1
    return text


def load_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def apply_term_fixes(text: str) -> str:
    for source, target in TERM_FIXES.items():
        text = text.replace(source, target)
    return text


def split_long(text: str, limit: int = 3600) -> list[str]:
    if len(text) <= limit:
        return [text]
    pieces: list[str] = []
    current = ""
    for part in re.split(r"(?<=[.!?。！？])\s+", text):
        if len(current) + len(part) + 1 > limit and current:
            pieces.append(current.strip())
            current = part
        else:
            current = f"{current} {part}".strip()
    if current:
        pieces.append(current.strip())
    return pieces


def request_google_translation(piece: str) -> str:
    import requests

    response = requests.get(
        "https://translate.googleapis.com/translate_a/single",
        params={
            "client": "gtx",
            "sl": "en",
            "tl": "ja",
            "dt": "t",
            "q": piece,
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    return "".join(part[0] for part in data[0] if part and part[0])


def translate_body(body: str, translator, cache: dict[str, str]) -> str:
    if not body.strip():
        return body
    cache_key = body
    if cache_key in cache:
        return cache[cache_key]
    translated_parts = []
    for piece in split_long(body):
        for attempt in range(4):
            try:
                translated_parts.append(request_google_translation(piece))
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(1.5 + attempt)
    translated = apply_term_fixes(" ".join(translated_parts))
    cache[cache_key] = translated
    if len(cache) % 50 == 0:
        save_cache(cache)
        print(f"translated {len(cache)} unique lines", flush=True)
    return translated


def translate_line(line: str, translator, cache: dict[str, str]) -> str:
    if not line.strip() or line.strip() == "---":
        return line

    heading = re.match(r"^(#{1,6}\s+)(.*)$", line)
    if heading:
        return heading.group(1) + translate_body(heading.group(2), translator, cache)

    quote = re.match(r"^(>\s?)(.*)$", line)
    if quote:
        return quote.group(1) + translate_body(quote.group(2), translator, cache)

    emphasis = re.match(r"^(\*+)([^*].*?)(\*+)$", line)
    if emphasis:
        return emphasis.group(1) + translate_body(emphasis.group(2), translator, cache) + emphasis.group(3)

    return translate_body(line, translator, cache)


def build_japanese(en_text: str) -> str:
    translator = None
    cache = load_cache()
    lines = en_text.splitlines()
    out_lines = []
    for idx, line in enumerate(lines, start=1):
        out_lines.append(translate_line(line, translator, cache))
        if idx % 100 == 0:
            save_cache(cache)
            print(f"processed {idx}/{len(lines)} lines", flush=True)
    save_cache(cache)
    return "\n".join(out_lines) + ("\n" if en_text.endswith("\n") else "")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-translation", action="store_true")
    args = parser.parse_args()

    english = build_english()
    EN_OUT.write_text(english, encoding="utf-8")
    print(f"English words: {word_count(english)}", flush=True)
    print(f"English file: {EN_OUT}", flush=True)

    if not args.skip_translation:
        japanese = build_japanese(english)
        JP_OUT.write_text(japanese, encoding="utf-8")
        print(f"Japanese file: {JP_OUT}", flush=True)
        print(f"Line counts: EN={len(english.splitlines())} JP={len(japanese.splitlines())}", flush=True)


if __name__ == "__main__":
    main()

import os

# 1. Translate index-jp.html remaining sections
jp_filepath = "index-jp.html"
with open(jp_filepath, 'r', encoding='utf-8') as f:
    jp_content = f.read()

translations = [
    # Characters Section
    ('Meet the full cast currently named across the released chapters, from the core party to side characters and major threats.', 'これまでに公開された章で名前が判明しているすべてのキャラクター（主要パーティーから脇役、そして大きな脅威まで）を紹介します。'),
    
    # Powers Section
    ('A simple breakdown of how Yono\'s power keeps climbing chapter by chapter.', '章が進むごとにヨノの力がどのように上昇していくかを簡単に解説します。'),
    ('From 第2巻 onward, the latest chapter is always Yono\'s strongest showing so far. He does not keep one final form; he turns each broken seal into the floor of the next chapter.\n        The one limit that keeps the story alive is that he still needs someone to notice him. If nobody sees or thinks about him, he goes quiet.', '第2巻以降、常に最新の章がヨノの最も強力な状態となります。彼には一つの最終形態があるわけではなく、壊れた封印を次の章の基盤へと変えていきます。\n        物語を成り立たせている唯一の制限は、彼が「誰かに認識される必要がある」という点です。誰も彼を見たり考えたりしなければ、彼は沈黙します。'),
    ('Yono\'s Powers', 'ヨノの能力'),
    
    # Leaks Section
    ('Heavy spoilers and overpowered Yono reveals. These powers are gained one by one every chapter as Yono keeps climbing higher.', '重大なネタバレと圧倒的なヨノの能力。これらの力は、ヨノがより高みへと登るにつれて、各章で一つずつ獲得されます。'),
    ('Chapter-by-Chapter Unlock', '章ごとの解放'),
    ('These leaked powers are not dropped on Yono all at once. He gains them one by one every chapter, so each new chapter makes him stronger than the last.', 'これらの力は一度にすべてヨノに与えられるわけではありません。各章で一つずつ獲得していくため、新しい章ごとに彼は以前よりも強くなります。'),
    ('Absolute Fiction Immunity', '絶対的フィクション耐性'),
    ('Yono becomes fully immune to any character in fiction, any outside scaling, and any attack or ability that tries to force a result on him.', 'ヨノはフィクション内のいかなるキャラクター、外部からのスケーリング、または彼に結果を強制しようとする攻撃や能力に対して完全な免疫を持ちます。'),
    ('Hax Immunity', 'チート能力耐性'),
    ('Mind control, sealing, reality hacks, fate control, conceptual attacks, anti-hax powers, and all other broken cheat abilities fail on Yono unless he lets them work.', '精神支配、封印、現実改変、運命操作、概念攻撃、アンチハックス能力、その他すべての壊れたチート能力は、ヨノが許可しない限り無効化されます。'),
    ('Damage Denial', 'ダメージの否定'),
    ('At his leaked peak, damage does not register on Yono unless he personally allows the hit to count as real.', '彼のピーク時には、ヨノ自身がその攻撃を本物として受け入れない限り、ダメージは一切記録されません。'),
    ('Erasure Rejection', '消去の拒絶'),
    ('Deletion, erasure, sealing, non-existence, and reality wipe effects all fail because Yono can refuse the rule that says he should disappear.', '削除、消去、封印、非存在化、現実改変の効果はすべて失敗します。なぜなら、ヨノは「自分が消えなければならない」という規則を拒否できるからです。'),
    ('Rule Maker', 'ルールの創造者'),
    ('He can create his own rules mid-fight and overwrite the rules other characters were relying on before the battle even finishes unfolding.', '彼は戦闘中に独自のルールを作成し、他のキャラクターが依存していたルールを、戦闘が完全に展開される前に上書きすることができます。'),
    ('Any-Power Desire', 'あらゆる能力の渇望'),
    ('Yono can use any power he desires once he decides it belongs in the scene. He does not need permission, compatibility, or a learning phase.', 'ヨノは、その能力がその場にふさわしいと判断すれば、望む能力を何でも使用できます。許可や適合性、学習期間は一切必要ありません。'),
    ('Power Copy x100', '能力コピー x100'),
    ('He can copy anyone\'s power with no limitation and immediately output it at one hundred times the original strength.', '彼は無制限に誰の能力でもコピーし、即座に元の100倍の威力で出力することができます。'),
    ('Pre-Attack Sight', '攻撃の事前予測'),
    ('Yono sees enemy attacks before they even happen, even on the so-called maximum speed scale, which lets him answer before the attacker\'s move is truly born.', 'ヨノはいわゆる最高速度のスケールであっても、敵の攻撃が起こる前にそれを見抜くことができ、攻撃者の行動が完全に形成される前に対応することができます。'),
    ('Inf IQ / Inf Battle IQ', '無限のIQ / 無限の戦闘IQ'),
    ('One leak gives Yono inf IQ and inf battle IQ, so he can process limitless information instantly, read the entire fight at once, and choose the perfect answer before the other side even understands the exchange.', 'ある能力により、ヨノは無限のIQと戦闘IQを得ます。これにより、彼は無限の情報を瞬時に処理し、戦い全体を一度に読み取り、相手が状況を理解する前に完璧な対応を選ぶことができます。'),
    ('Faster Than the Original', 'オリジナルより速く'),
    ('If an enemy starts an attack, Yono can copy that same power and use it first, before the original attacker finishes performing it.', 'もし敵が攻撃を開始した場合、ヨノは同じ能力をコピーし、元の攻撃者が動作を終える前に先に使用することができます。'),
    ('Real-Layer Resistance', '現実階層への耐性'),
    ('The leak version of Yono is written so that even any supposed real-world layer, author-layer, or observer-layer interference still cannot control him.', 'リーク版のヨノは、現実世界、作者層、または観測者層からの干渉でさえも彼を制御できないように書かれています。'),
    ('No-Loss State', '敗北なき状態'),
    ('Winning, losing, surviving, dying, or being countered become choices around Yono instead of outcomes forced onto him.', '勝利、敗北、生存、死、あるいは反撃を受けることは、ヨノにとって強制される結果ではなく、彼自身の選択となります。'),
    ('Past Boundless', '限界を超えて'),
    ('The leak scaling places Yono past the boundless power scale itself. He is not just at the top of the chart. He is beyond the need for the chart.', 'リークのスケーリングは、ヨノを限界のない力のスケールそのものの先に位置づけます。彼は単にチャートの頂点にいるだけでなく、チャートそのものを必要としない領域にいます。'),
    ('Crown Contract', '王冠の契約'),
    ('If someone fights Yono seriously, he can force the battle into a Crown Contract that binds the opponent to his terms.', 'もし誰かが本気でヨノと戦うなら、彼は戦いを「王冠の契約」に強制し、相手を自分の条件に縛り付けることができます。'),
    ('100% Opponent Control', '100%の相手コントロール'),
    ('One leaked contract path gives Yono total control over the person fighting him, including their movement, power output, and whether they can even continue the battle.', 'リークされた契約パスの一つは、相手の動き、力の出力、戦いを続けられるかどうかに至るまで、ヨノに戦う相手に対する完全なコントロールを与えます。'),
    ('Authority Seizure', '権限の奪取'),
    ('He can take command of an enemy\'s powers, titles, and special forms as soon as the contract recognizes them as part of the fight.', '契約がそれらを戦いの一部として認識した瞬間に、彼は敵の能力、称号、そして特殊形態の指揮権を奪うことができます。'),
    ('Forced Terms', '強制された条件'),
    ('Once the contract is active, the opponent stops fighting on equal ground. They fight inside rules Yono wrote for them.', '契約が有効になると、相手は対等な条件で戦うことができなくなります。彼らはヨノが彼らのために書いたルールの中で戦うことになります。'),
    ('Above the Big 3', 'ビッグ3を超えて'),
    ('The leak scaling puts Yono beyond the strongest characters from the big 3 anime worlds by a huge margin, not by effort but by system-level superiority.', 'リークのスケーリングは、ビッグ3のアニメ世界の最強キャラクターたちを大差で凌駕します。それは努力によるものではなく、システムレベルの優位性によるものです。'),
    ('Beyond CC Goku', 'CC悟空を超えて'),
    ('Leak notes place Yono above CC Goku and other extreme crossover-scale characters because Yono can reject their scaling framework entirely.', 'リークノートでは、ヨノが彼らのスケーリングの枠組みを完全に拒否できるため、CC悟空やその他の極端なクロスオーバースケールのキャラクターを超えているとしています。'),
    ('No Counter Matchups', 'カウンター不能'),
    ('There is no clean hard-counter matchup for the leaked version of Yono. Copy abilities, anti-hax abilities, and god-tier counters still fail.', 'リーク版のヨノには、明確なハードカウンターとなる対戦相手は存在しません。コピー能力、アンチハックス能力、神レベルのカウンターでさえ失敗します。'),
    ('Stronger Every New Chapter', '新しい章ごとに強くなる'),
    ('Even these leaks are not his final cap. Each new chapter can still give Yono another power and make the newest version stronger than the last leaked version.', 'これらのリークでさえ彼の最終的な限界ではありません。新しい章ごとにヨノはさらなる力を得て、最新バージョンは最後にリークされたバージョンよりも強力になります。'),
    ('These leaks are full spoiler material for late-story Yono. The idea is simple: every chapter unlocks another layer, and once enough seals break he stops being measured by normal anime power systems and starts deciding the system itself.', 'これらのリークは物語後半のヨノに関する完全なネタバレを含んでいます。コンセプトは単純です：すべての章が新たな層を解放し、十分な数の封印が解かれると、彼はもはや通常のアニメのパワーシステムで測られることはなくなり、彼自身がシステムを決定するようになります。'),
    
    # Lore Section
    ('Background on the Shade, the forest confession, Velkor\'s prison, and the sealed power inside Yono.', 'シェードの背景、森の告白、ヴェルコールの牢獄、そしてヨノの中に封印された力について。'),
    ('Lore & Backstory', '世界観とバックストーリー'),
    
    # Credits Section
    ('The world, story, and release identity behind the project.', 'プロジェクトの背後にある世界観、物語、そしてリリースのアイデンティティ。'),
    ('is presented here as a polished reading hub, collector export, and official series landing page. This section makes the authorship, channels, and release identity clear in one place.', 'ここでは、洗練されたリーディングハブ、コレクター向けのエクスポート、公式シリーズのランディングページとして提供されています。このセクションでは、著作権、チャンネル、リリースのアイデンティティを明確にしています。'),
    ('Created by BiniFn', '作成：BiniFn'),
    ('Official web reader + PDF/EPUB release build', '公式ウェブリーダー + PDF/EPUBリリースビルド'),
    ('Dark fantasy / romance / power fantasy project', 'ダークファンタジー / ロマンス / パワーファンタジー プロジェクト'),
    ('Author, creator, and project lead for', 'の著者、クリエイター、およびプロジェクトリード。'),
    ('. The story, characters, setting, and release direction all start here.', '。物語、キャラクター、設定、そしてリリースの方向性はすべてここから始まります。'),
    ('If you share the site, PDF, or EPUB, keep the BiniFn name attached so the project always points back to the original creator.', 'サイト、PDF、またはEPUBを共有する場合は、プロジェクトが常に元のクリエイターに結びつくよう、BiniFnの名前を付けたままにしてください。'),
    ('Official Channels', '公式チャンネル'),
    ('Main Channel:', 'メインチャンネル:'),
    ('Roblox Tutorials:', 'Robloxチュートリアル:'),
    ('Anime Channel:', 'アニメチャンネル:'),
    ('Official Links', '公式リンク'),
    ('Extra project links and profile hubs for the creator.', 'クリエイターの追加プロジェクトリンクとプロフィールハブ。'),
    ('Release Credits', 'リリースクレジット'),
    ('This site is the official reading hub for the light novel, and the downloadable PDF and EPUB exports are branded to match the same release identity.', 'このサイトはライトノベルの公式リーディングハブであり、ダウンロード可能なPDFおよびEPUBのエクスポートは同じリリースアイデンティティに合わせてブランド化されています。'),
    ('Credits are now baked into the page itself and into the generated export files so attribution stays visible when chapters are shared offline.', 'クレジットはページ自体と生成されたエクスポートファイルに組み込まれており、章がオフラインで共有された際にも帰属が可視化されるようになっています。'),
    ('author', '著者'),
    ('creator', 'クリエイター'),
    ('series owner', 'シリーズ所有者'),
    ('official web reader', '公式ウェブリーダー'),
    ('collector pdf', 'コレクターPDF'),
    ('styled epub', '装飾EPUB')
]

for eng, jp in translations:
    jp_content = jp_content.replace(eng, jp)

with open(jp_filepath, 'w', encoding='utf-8') as f:
    f.write(jp_content)


# 2. Remove User Posts section from profile.html and profile-jp.html
import re

for pf in ['profile.html', 'profile-jp.html']:
    if not os.path.exists(pf):
        continue
    with open(pf, 'r', encoding='utf-8') as f:
        p_content = f.read()
    
    # Remove the lines:
    # if (posts.length) {
    #   const lines = posts.map(post => `<div>• ${post.title} (${post.category || "post"})</div>`).join("");
    #   document.getElementById("analytics").insertAdjacentHTML("beforebegin", `<article class="card" style="text-align: left; margin-bottom: 24px;"><h2 style="margin-top:0; font-family: 'Cormorant Garamond', serif;">User Posts</h2>${lines}</article>`);
    # }
    
    pattern = re.compile(r'if \(\s*posts\.length\s*\)\s*\{[^\}]+\}\s*', re.MULTILINE | re.DOTALL)
    p_content = pattern.sub('', p_content)
    
    with open(pf, 'w', encoding='utf-8') as f:
        f.write(p_content)

print("Translated remaining sections and removed User Posts from profile.")

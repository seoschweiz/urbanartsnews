"""Generate localized, indexable Art Is Trash artist profiles."""

from html import escape
from pathlib import Path
import re


BASE = "https://urbanartsnews.com"
ORIGINAL = f"{BASE}/artists/art-is-trash/"
IMAGE = "/assets/images/art-is-trash/discarded-furniture-street-art.jpg"
INSTAGRAM = "https://www.instagram.com/artistrash/"

LANGUAGES = {
    "ca": {
        "name": "Català", "title": "Art Is Trash: art urbà de Francisco de Pájaro a Barcelona",
        "description": "Descobreix Art Is Trash, el projecte de Francisco de Pájaro que transforma residus i objectes abandonats dels carrers de Barcelona en art urbà efímer.",
        "heading": "Art Is Trash a Barcelona", "label": "Artista urbà · Barcelona",
        "sections": [
            ("Qui és Art Is Trash?", "Art Is Trash és el projecte artístic de Francisco de Pájaro, creador vinculat a Barcelona i conegut per convertir residus, cartrons, mobles trencats i objectes abandonats en personatges expressius. Les seves intervencions apareixen directament al carrer i transformen materials rebutjats en escenes plenes d’humor, crítica i energia visual."),
            ("El carrer com a espai de creació", "L’obra no espera una paret autoritzada ni una sala d’exposicions. De Pájaro treballa amb allò que troba i respon immediatament a la forma, la posició i l’estat de cada objecte. Barcelona es converteix així en estudi, escenari i públic. Les peces poden desaparèixer ràpidament quan els serveis de neteja retiren els materials."),
            ("Residus, personatges i crítica social", "Ulls, boques, braços i frases pintades donen una nova identitat a allò que la ciutat considera inútil. Aquesta transformació parla del consum, de l’exclusió i de la vida quotidiana, però també conserva un humor directe i accessible. L’espectador pot descobrir l’obra per casualitat, sense entrada ni coneixements previs."),
            ("Un arxiu d’art efímer", "Com que moltes intervencions duren només unes hores, la fotografia i les publicacions de l’artista són essencials. Urban Arts News reuneix obres seleccionades, una galeria visual i enllaços al perfil oficial perquè el públic pugui seguir l’evolució del projecte i entendre la seva relació amb Barcelona."),
        ],
        "gallery": "Veure la galeria d’Art Is Trash", "city": "Explorar l’art urbà de Barcelona", "original": "Llegir l’article original en anglès",
    },
    "es": {
        "name": "Español", "title": "Art Is Trash: arte urbano de Francisco de Pájaro en Barcelona",
        "description": "Descubre Art Is Trash, el proyecto de Francisco de Pájaro que transforma basura y objetos abandonados de Barcelona en arte urbano efímero.",
        "heading": "Art Is Trash en Barcelona", "label": "Artista urbano · Barcelona",
        "sections": [
            ("¿Quién es Art Is Trash?", "Art Is Trash es el proyecto artístico de Francisco de Pájaro, creador vinculado a Barcelona y conocido por convertir residuos, cartones, muebles rotos y objetos abandonados en personajes expresivos. Sus intervenciones aparecen directamente en la calle y transforman materiales desechados en escenas llenas de humor, crítica y energía visual."),
            ("La calle como espacio creativo", "La obra no espera una pared autorizada ni una sala de exposiciones. De Pájaro trabaja con lo que encuentra y responde inmediatamente a la forma, posición y estado de cada objeto. Barcelona se convierte en estudio, escenario y público. Las piezas pueden desaparecer rápidamente cuando los servicios de limpieza retiran los materiales."),
            ("Residuos, personajes y crítica social", "Ojos, bocas, brazos y frases pintadas dan una nueva identidad a aquello que la ciudad considera inútil. La transformación habla del consumo, la exclusión y la vida cotidiana, pero conserva un humor directo y accesible. Cualquier persona puede encontrar la obra por casualidad, sin entrada ni conocimientos previos."),
            ("Un archivo de arte efímero", "Muchas intervenciones duran solamente unas horas, por lo que la fotografía y las publicaciones del artista son esenciales. Urban Arts News reúne obras seleccionadas, una galería visual y enlaces al perfil oficial para seguir la evolución del proyecto y comprender su relación con Barcelona."),
        ],
        "gallery": "Ver la galería de Art Is Trash", "city": "Explorar el arte urbano de Barcelona", "original": "Leer el artículo original en inglés",
    },
    "de": {
        "name": "Deutsch", "title": "Art Is Trash: Urban Art von Francisco de Pájaro in Barcelona",
        "description": "Entdecke Art Is Trash von Francisco de Pájaro, der Abfall und weggeworfene Gegenstände auf Barcelonas Straßen in vergängliche urbane Kunst verwandelt.",
        "heading": "Art Is Trash in Barcelona", "label": "Urban Artist · Barcelona",
        "sections": [
            ("Wer ist Art Is Trash?", "Art Is Trash ist das Kunstprojekt von Francisco de Pájaro. Der mit Barcelona verbundene Künstler verwandelt Abfall, Karton, beschädigte Möbel und weggeworfene Gegenstände in ausdrucksstarke Figuren. Seine spontanen Eingriffe entstehen unmittelbar auf der Straße und machen aus übersehenen Materialien Szenen voller Humor, Kritik und visueller Energie."),
            ("Die Straße als Atelier", "Die Kunst wartet weder auf eine genehmigte Wand noch auf einen Ausstellungsraum. De Pájaro arbeitet mit dem, was er findet, und reagiert auf Form, Lage und Zustand jedes Objekts. Barcelona wird gleichzeitig Atelier, Bühne und Publikum. Viele Werke verschwinden schnell, sobald die Stadtreinigung die verwendeten Materialien entfernt."),
            ("Abfall, Figuren und Gesellschaftskritik", "Gemalte Augen, Münder, Arme und kurze Botschaften geben scheinbar nutzlosen Dingen eine neue Identität. Die Verwandlung spricht über Konsum, Ausgrenzung und den Alltag in der Stadt, bleibt dabei aber direkt und humorvoll. Passanten können die Arbeiten zufällig entdecken – kostenlos und ohne Vorwissen über zeitgenössische Kunst."),
            ("Ein Archiv vergänglicher Kunst", "Da manche Interventionen nur wenige Stunden bestehen, sind Fotografien und die öffentlichen Beiträge des Künstlers entscheidend. Urban Arts News verbindet ausgewählte Werke mit einer Bildergalerie, dem offiziellen Instagram-Profil und dem Barcelona-Archiv. So bleibt die Entwicklung von Art Is Trash auch nach dem Verschwinden der ursprünglichen Arbeiten nachvollziehbar."),
        ],
        "gallery": "Art-Is-Trash-Galerie ansehen", "city": "Urban Art in Barcelona entdecken", "original": "Englischen Originalartikel lesen",
    },
    "fr": {
        "name": "Français", "title": "Art Is Trash : l’art urbain de Francisco de Pájaro à Barcelone",
        "description": "Découvrez Art Is Trash, le projet de Francisco de Pájaro qui transforme déchets et objets abandonnés de Barcelone en art urbain éphémère.",
        "heading": "Art Is Trash à Barcelone", "label": "Artiste urbain · Barcelone",
        "sections": [
            ("Qui est Art Is Trash ?", "Art Is Trash est le projet artistique de Francisco de Pájaro, créateur lié à Barcelone et connu pour transformer déchets, cartons, meubles cassés et objets abandonnés en personnages expressifs. Ses interventions apparaissent directement dans la rue et donnent aux matériaux rejetés une nouvelle vie, pleine d’humour, de critique et d’énergie visuelle."),
            ("La rue comme espace de création", "L’œuvre n’attend ni mur autorisé ni salle d’exposition. De Pájaro travaille avec ce qu’il trouve et réagit immédiatement à la forme, à la position et à l’état de chaque objet. Barcelone devient atelier, scène et public. Les pièces peuvent disparaître rapidement lorsque les services de nettoyage retirent les matériaux."),
            ("Déchets, personnages et critique sociale", "Des yeux, des bouches, des bras et des phrases peintes donnent une identité à ce que la ville considère comme inutile. Cette transformation évoque la consommation, l’exclusion et la vie quotidienne tout en conservant un humour direct. Le public peut découvrir l’œuvre par hasard, gratuitement et sans connaissance préalable de l’art contemporain."),
            ("Une archive d’art éphémère", "De nombreuses interventions ne durent que quelques heures. La photographie et les publications de l’artiste deviennent donc essentielles. Urban Arts News rassemble des œuvres choisies, une galerie visuelle et des liens vers le profil officiel afin de suivre l’évolution du projet et sa relation particulière avec Barcelone."),
        ],
        "gallery": "Voir la galerie Art Is Trash", "city": "Découvrir l’art urbain à Barcelone", "original": "Lire l’article original en anglais",
    },
    "it": {
        "name": "Italiano", "title": "Art Is Trash: l’arte urbana di Francisco de Pájaro a Barcellona",
        "description": "Scopri Art Is Trash, il progetto di Francisco de Pájaro che trasforma rifiuti e oggetti abbandonati di Barcellona in arte urbana effimera.",
        "heading": "Art Is Trash a Barcellona", "label": "Artista urbano · Barcellona",
        "sections": [
            ("Chi è Art Is Trash?", "Art Is Trash è il progetto artistico di Francisco de Pájaro, autore legato a Barcellona e conosciuto per trasformare rifiuti, cartoni, mobili rotti e oggetti abbandonati in personaggi espressivi. I suoi interventi nascono direttamente in strada e convertono materiali scartati in scene cariche di umorismo, critica ed energia visiva."),
            ("La strada come spazio creativo", "L’opera non aspetta una parete autorizzata o una sala espositiva. De Pájaro lavora con ciò che trova e reagisce alla forma, alla posizione e alle condizioni di ogni oggetto. Barcellona diventa insieme studio, palcoscenico e pubblico. Le opere possono scomparire rapidamente quando i servizi di pulizia rimuovono i materiali."),
            ("Rifiuti, personaggi e critica sociale", "Occhi, bocche, braccia e brevi frasi dipinte danno una nuova identità a ciò che la città considera inutile. La trasformazione parla di consumo, esclusione e vita quotidiana, mantenendo però un umorismo diretto e accessibile. Chiunque può incontrare l’opera per caso, senza biglietto e senza conoscenze artistiche."),
            ("Un archivio di arte effimera", "Molti interventi durano soltanto poche ore, perciò le fotografie e le pubblicazioni dell’artista sono fondamentali. Urban Arts News riunisce opere selezionate, una galleria visiva e collegamenti al profilo ufficiale per seguire l’evoluzione del progetto e comprendere il suo rapporto con Barcellona."),
        ],
        "gallery": "Vedi la galleria di Art Is Trash", "city": "Esplora l’arte urbana di Barcellona", "original": "Leggi l’articolo originale in inglese",
    },
    "pt": {
        "name": "Português", "title": "Art Is Trash: arte urbana de Francisco de Pájaro em Barcelona",
        "description": "Descubra Art Is Trash, o projeto de Francisco de Pájaro que transforma lixo e objetos abandonados de Barcelona em arte urbana efêmera.",
        "heading": "Art Is Trash em Barcelona", "label": "Artista urbano · Barcelona",
        "sections": [
            ("Quem é Art Is Trash?", "Art Is Trash é o projeto artístico de Francisco de Pájaro, criador ligado a Barcelona e conhecido por transformar resíduos, papelão, móveis quebrados e objetos abandonados em personagens expressivos. As intervenções aparecem diretamente na rua e convertem materiais descartados em cenas cheias de humor, crítica e energia visual."),
            ("A rua como espaço criativo", "A obra não espera uma parede autorizada nem uma sala de exposição. De Pájaro trabalha com aquilo que encontra e reage imediatamente à forma, posição e estado de cada objeto. Barcelona torna-se estúdio, palco e público. As peças podem desaparecer rapidamente quando os serviços de limpeza retiram os materiais."),
            ("Resíduos, personagens e crítica social", "Olhos, bocas, braços e frases pintadas dão uma nova identidade ao que a cidade considera inútil. A transformação aborda consumo, exclusão e vida quotidiana, mantendo um humor direto e acessível. Qualquer pessoa pode encontrar a obra por acaso, sem bilhete e sem conhecimentos prévios de arte contemporânea."),
            ("Um arquivo de arte efêmera", "Muitas intervenções duram apenas algumas horas, por isso as fotografias e publicações do artista são essenciais. Urban Arts News reúne obras selecionadas, uma galeria visual e ligações ao perfil oficial para acompanhar a evolução do projeto e compreender a sua relação com Barcelona."),
        ],
        "gallery": "Ver a galeria Art Is Trash", "city": "Explorar a arte urbana de Barcelona", "original": "Ler o artigo original em inglês",
    },
    "sq": {
        "name": "Shqip", "title": "Art Is Trash: arti urban i Francisco de Pájaro në Barcelonë",
        "description": "Zbuloni Art Is Trash, projektin e Francisco de Pájaro që shndërron mbeturinat dhe objektet e braktisura të Barcelonës në art urban të përkohshëm.",
        "heading": "Art Is Trash në Barcelonë", "label": "Artist urban · Barcelonë",
        "sections": [
            ("Kush është Art Is Trash?", "Art Is Trash është projekti artistik i Francisco de Pájaro, një krijues i lidhur me Barcelonën dhe i njohur për shndërrimin e mbeturinave, kartonëve, mobilieve të thyera dhe objekteve të braktisura në personazhe ekspresive. Ndërhyrjet e tij shfaqen drejtpërdrejt në rrugë dhe u japin materialeve të hedhura humor, kritikë dhe energji vizuale."),
            ("Rruga si hapësirë krijuese", "Vepra nuk pret një mur të autorizuar apo një sallë ekspozite. De Pájaro punon me atë që gjen dhe reagon ndaj formës, pozicionit dhe gjendjes së çdo objekti. Barcelona bëhet njëkohësisht studio, skenë dhe publik. Punimet mund të zhduken shpejt kur shërbimet e pastrimit largojnë materialet."),
            ("Mbeturina, personazhe dhe kritikë sociale", "Sytë, gojët, krahët dhe frazat e pikturuara u japin identitet të ri gjërave që qyteti i konsideron të padobishme. Transformimi flet për konsumin, përjashtimin dhe jetën e përditshme, por ruan një humor të drejtpërdrejtë. Çdokush mund ta zbulojë veprën rastësisht, pa biletë dhe pa njohuri paraprake arti."),
            ("Një arkiv i artit të përkohshëm", "Shumë ndërhyrje zgjasin vetëm disa orë, prandaj fotografitë dhe publikimet e artistit janë thelbësore. Urban Arts News bashkon vepra të zgjedhura, një galeri pamore dhe lidhje me profilin zyrtar për të ndjekur zhvillimin e projektit dhe marrëdhënien e tij me Barcelonën."),
        ],
        "gallery": "Shikoni galerinë Art Is Trash", "city": "Eksploroni artin urban të Barcelonës", "original": "Lexoni artikullin origjinal në anglisht",
    },
    "ja": {
        "name": "日本語", "title": "Art Is Trash：フランシスコ・デ・パハロとバルセロナのアーバンアート",
        "description": "バルセロナの廃棄物や捨てられた家具を一時的なアーバンアートへ変える、フランシスコ・デ・パハロのArt Is Trashを紹介します。",
        "heading": "バルセロナのArt Is Trash", "label": "アーバンアーティスト · バルセロナ",
        "sections": [
            ("Art Is Trashとは", "Art Is Trashは、バルセロナと深く関わるアーティスト、フランシスコ・デ・パハロのプロジェクトです。段ボール、壊れた家具、袋、捨てられた物に目や口、手足を描き、強い表情を持つキャラクターへ変えます。路上で生まれる作品には、ユーモア、社会批評、即興的な視覚エネルギーが共存しています。"),
            ("制作空間としての路上", "作品は許可された壁や展示室を待ちません。デ・パハロはその場で見つけた物の形、位置、傷み方に反応しながら制作します。バルセロナの街はスタジオであり、舞台であり、観客でもあります。清掃によって素材が回収されれば、作品は数時間で消えてしまうこともあります。"),
            ("廃棄物と社会への視線", "都市が不要と判断した物に新しい人格を与える行為は、消費、排除、格差、日常生活について考えるきっかけになります。一方で、作品は難解な説明を必要としません。通行人は偶然作品に出会い、無料で、現代美術の知識がなくても、その表情やメッセージを感じ取ることができます。"),
            ("消える作品を残すアーカイブ", "多くの作品が短時間しか存在しないため、写真とアーティスト自身の公開記録は重要です。Urban Arts Newsでは、選ばれた作品、画像ギャラリー、公式Instagram、バルセロナの都市ページを結び、プロジェクトの変化と街との関係を継続的に紹介します。"),
        ],
        "gallery": "Art Is Trashギャラリーを見る", "city": "バルセロナのアーバンアートを探す", "original": "英語のオリジナル記事を読む",
    },
    "ar": {
        "name": "العربية", "title": "Art Is Trash: الفن الحضري لفرانسيسكو دي باخارو في برشلونة",
        "description": "اكتشف مشروع Art Is Trash لفرانسيسكو دي باخارو، الذي يحول النفايات والأشياء المهملة في شوارع برشلونة إلى فن حضري مؤقت.",
        "heading": "Art Is Trash في برشلونة", "label": "فنان حضري · برشلونة",
        "sections": [
            ("من هو Art Is Trash؟", "Art Is Trash هو المشروع الفني لفرانسيسكو دي باخارو، الفنان المرتبط ببرشلونة والمعروف بتحويل الورق المقوى والأثاث المكسور والأكياس والأشياء المهملة إلى شخصيات ذات تعبير قوي. تظهر تدخلاته مباشرة في الشارع، حيث تمنح المواد المرفوضة حياة جديدة تجمع بين الفكاهة والنقد والطاقة البصرية."),
            ("الشارع مساحة للإبداع", "لا ينتظر العمل جداراً مرخصاً أو قاعة عرض. يعمل دي باخارو بما يجده ويستجيب فوراً لشكل كل غرض وموقعه وحالته. تتحول برشلونة إلى مرسم ومسرح وجمهور في الوقت نفسه. وقد تختفي القطع بسرعة عندما تزيل خدمات النظافة المواد المستخدمة، لذلك يصبح الزمن جزءاً أساسياً من العمل."),
            ("النفايات والشخصيات والنقد الاجتماعي", "تمنح العيون والأفواه والأذرع والعبارات المرسومة هوية جديدة لما تعتبره المدينة عديم الفائدة. يتناول هذا التحول الاستهلاك والإقصاء والحياة اليومية، لكنه يحافظ على روح مباشرة يسهل فهمها. يستطيع المارة اكتشاف العمل بالمصادفة، من دون تذكرة أو معرفة سابقة بالفن المعاصر."),
            ("أرشيف لفن سريع الزوال", "لا تدوم تدخلات كثيرة سوى ساعات قليلة، ولذلك تكتسب الصور ومنشورات الفنان أهمية كبيرة. يجمع Urban Arts News أعمالاً مختارة ومعرضاً بصرياً وروابط إلى الحساب الرسمي وصفحة برشلونة، حتى يتمكن الجمهور من متابعة تطور المشروع وفهم علاقته الخاصة بالمدينة."),
        ],
        "gallery": "شاهد معرض Art Is Trash", "city": "اكتشف الفن الحضري في برشلونة", "original": "اقرأ المقال الأصلي بالإنجليزية",
    },
}

EXTRA_SECTIONS = {
    "ca": [("De Zafra a Barcelona i al món", "Francisco de Pájaro és originari de Zafra, a Extremadura, i viu i treballa a Barcelona. Des d’aquesta base ha viatjat arreu del món, ha realitzat importants encàrrecs murals i ha participat en exposicions internacionals. La seva obra també forma part de col·leccions d’art rellevants."), ("Escultura efímera, missatge polític i col·leccionisme", "Art Is Trash ocupa una posició poc habitual dins l’art urbà: converteix objectes trobats en escultures efímeres amb una força expressiva extraordinària. No és una obra simplement decorativa; parla de consum, residus, desigualtat i exclusió. Per als col·leccionistes que pensen a llarg termini, la seva originalitat, trajectòria internacional i escassetat documentada poden resultar especialment interessants, tot i que cap obra garanteix un rendiment financer.")],
    "es": [("De Zafra a Barcelona y al mundo", "Francisco de Pájaro es originario de Zafra, en Extremadura, y vive y trabaja en Barcelona. Desde esta base ha viajado por todo el mundo, ha realizado importantes encargos de murales y ha participado en exposiciones internacionales. Su obra también está presente en destacadas colecciones de arte."), ("Escultura efímera, mensaje político y coleccionismo", "Art Is Trash ocupa una posición poco común dentro del arte urbano: convierte objetos encontrados en esculturas efímeras con una extraordinaria fuerza expresiva. No es una obra meramente decorativa; aborda consumo, residuos, desigualdad y exclusión. Para coleccionistas con una visión a largo plazo, su originalidad, trayectoria internacional y escasez documentada pueden resultar especialmente atractivas, aunque ninguna obra garantiza rentabilidad financiera.")],
    "de": [("Von Zafra über Barcelona in die Welt", "Francisco de Pájaro stammt aus Zafra in der Extremadura und lebt und arbeitet heute in Barcelona. Von dort aus bereiste er die Welt, realisierte bedeutende Auftragsmurals und nahm an internationalen Ausstellungen teil. Seine Werke sind zudem in wichtigen Kunstsammlungen vertreten."), ("Vergängliche Skulptur, politische Botschaft und Sammeln", "Art Is Trash nimmt innerhalb der Urban Art eine seltene Position ein: Gefundene Gegenstände werden zu ephemeren Skulpturen von außergewöhnlicher Ausdruckskraft. Die Arbeiten sind nicht bloß dekorativ, sondern thematisieren Konsum, Abfall, Ungleichheit und Ausgrenzung. Für langfristig orientierte Sammler können Originalität, internationale Laufbahn und dokumentierte Seltenheit besonders interessant sein – eine finanzielle Wertentwicklung lässt sich bei Kunst jedoch nie garantieren.")],
    "fr": [("De Zafra à Barcelone, puis dans le monde", "Originaire de Zafra, en Estrémadure, Francisco de Pájaro vit et travaille aujourd’hui à Barcelone. Depuis cette base, il a parcouru le monde, réalisé d’importantes commandes de peintures murales et participé à des expositions internationales. Son œuvre figure également dans d’importantes collections d’art."), ("Sculpture éphémère, message politique et collection", "Art Is Trash occupe une place rare dans l’art urbain : des objets trouvés deviennent des sculptures éphémères d’une force expressive exceptionnelle. L’œuvre n’est pas simplement décorative; elle aborde consommation, déchets, inégalité et exclusion. Pour les collectionneurs à long terme, son originalité, sa carrière internationale et sa rareté documentée peuvent être particulièrement intéressantes, sans qu’aucune œuvre puisse garantir un rendement financier.")],
    "it": [("Da Zafra a Barcellona e nel mondo", "Francisco de Pájaro è originario di Zafra, in Estremadura, e vive e lavora a Barcellona. Da questa base ha viaggiato in tutto il mondo, realizzato importanti murales su commissione e partecipato a esposizioni internazionali. Le sue opere sono inoltre presenti in importanti collezioni d’arte."), ("Scultura effimera, messaggio politico e collezionismo", "Art Is Trash occupa una posizione rara nell’arte urbana: trasforma oggetti trovati in sculture effimere di straordinaria forza espressiva. Non si tratta di arte puramente decorativa; affronta consumo, rifiuti, disuguaglianza ed esclusione. Per i collezionisti orientati al lungo periodo, originalità, carriera internazionale e scarsità documentata possono essere particolarmente interessanti, anche se nessuna opera garantisce un rendimento finanziario.")],
    "pt": [("De Zafra a Barcelona e ao mundo", "Francisco de Pájaro é natural de Zafra, na Extremadura, e vive e trabalha em Barcelona. A partir dessa base viajou pelo mundo, realizou importantes murais por encomenda e participou em exposições internacionais. A sua obra também integra importantes coleções de arte."), ("Escultura efêmera, mensagem política e colecionismo", "Art Is Trash ocupa uma posição rara na arte urbana: transforma objetos encontrados em esculturas efêmeras de extraordinária força expressiva. Não é uma arte meramente decorativa; aborda consumo, resíduos, desigualdade e exclusão. Para colecionadores com visão de longo prazo, originalidade, carreira internacional e escassez documentada podem ser particularmente interessantes, embora nenhuma obra garanta retorno financeiro.")],
    "sq": [("Nga Zafra në Barcelonë dhe në botë", "Francisco de Pájaro vjen nga Zafra në Extremadura dhe jeton e punon në Barcelonë. Prej kësaj baze ka udhëtuar nëpër botë, ka realizuar murale të rëndësishme me porosi dhe ka marrë pjesë në ekspozita ndërkombëtare. Veprat e tij gjenden gjithashtu në koleksione të rëndësishme arti."), ("Skulpturë kalimtare, mesazh politik dhe koleksionim", "Art Is Trash zë një vend të rrallë në artin urban: objektet e gjetura bëhen skulptura kalimtare me fuqi të jashtëzakonshme shprehëse. Arti nuk është thjesht dekorativ; trajton konsumin, mbeturinat, pabarazinë dhe përjashtimin. Për koleksionistët afatgjatë, origjinaliteti, karriera ndërkombëtare dhe rrallësia e dokumentuar mund të jenë veçanërisht interesante, megjithëse asnjë vepër nuk garanton kthim financiar.")],
    "ja": [("サフラからバルセロナ、そして世界へ", "フランシスコ・デ・パハロはエストレマドゥーラ州サフラ出身で、現在はバルセロナで生活し制作しています。世界各地を旅し、大規模な壁画制作や国際展に参加してきました。作品は重要なアートコレクションにも収蔵されています。"), ("一時的な彫刻、政治的メッセージ、収集価値", "Art Is Trashは、拾われた物を強い表現力を持つ一時的な都市彫刻へ変える、アーバンアートの中でも珍しい存在です。単なる装飾ではなく、消費、廃棄、不平等、排除を問いかけます。独創性、国際的な活動、記録された希少性は長期的な視点を持つコレクターにとって魅力となり得ますが、芸術作品の経済的利益が保証されることはありません。")],
    "ar": [("من زافرا إلى برشلونة والعالم", "ينحدر فرانسيسكو دي باخارو من زافرا في إكستريمادورا، ويعيش ويعمل اليوم في برشلونة. ومن هذه القاعدة سافر حول العالم، ونفذ تكليفات مهمة لجداريات، وشارك في معارض دولية. كما توجد أعماله ضمن مجموعات فنية مهمة."), ("نحت مؤقت ورسالة سياسية واقتناء فني", "يحتل Art Is Trash موقعاً نادراً في الفن الحضري، إذ يحول الأشياء الموجودة إلى منحوتات مؤقتة ذات قوة تعبيرية استثنائية. ليست الأعمال مجرد زينة؛ فهي تناقش الاستهلاك والنفايات وعدم المساواة والإقصاء. وقد تكون الأصالة والمسيرة الدولية والندرة الموثقة جذابة لهواة الجمع ذوي الرؤية الطويلة، لكن لا يمكن لأي عمل فني أن يضمن عائداً مالياً.")],
}

for _code, _sections in EXTRA_SECTIONS.items():
    LANGUAGES[_code]["sections"].extend(_sections)

CSS = """*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f4f4f2;color:#171717;line-height:1.75}a{color:inherit}.top{background:#090909;color:#fff;padding:20px 6%}.logo{text-decoration:none;font-size:28px;font-weight:900}.logo span,.accent{color:#ff5b21}.hero{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(280px,.8fr);background:#111;color:#fff}.hero-copy{padding:75px 8%}.eyebrow{color:#ff5b21;font-weight:900;text-transform:uppercase}.hero h1{font-size:clamp(42px,7vw,78px);line-height:.98;margin:14px 0 22px}.hero p{font-size:20px;color:#ccc}.hero img{width:100%;height:100%;min-height:470px;object-fit:cover}.wrap{width:min(1020px,90%);margin:55px auto}.article{background:#fff;padding:clamp(28px,6vw,60px);box-shadow:0 10px 35px #00000012}.article h2{font-size:clamp(25px,4vw,36px);line-height:1.15;margin:38px 0 12px}.article h2:first-child{margin-top:0}.article p{font-size:18px}.actions,.language-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:35px}.button,.language-links a{display:inline-block;background:#ff5b21;color:#fff;text-decoration:none;font-weight:800;padding:12px 16px}.button.dark,.language-links a{background:#111}.language-box{margin-top:45px;border-top:4px solid #ff5b21;padding-top:25px}.language-box h2{margin-top:0}.language-links a.active{background:#ff5b21}footer{background:#090909;color:#aaa;text-align:center;padding:35px;margin-top:60px}@media(max-width:800px){.hero{grid-template-columns:1fr}.hero img{min-height:300px}.hero-copy{padding:55px 6%}}"""


def language_url(code):
    return f"{BASE}/{code}/artists/art-is-trash/"


def alternates():
    links = [f'<link rel="alternate" hreflang="en" href="{ORIGINAL}">', f'<link rel="alternate" hreflang="x-default" href="{ORIGINAL}">']
    links += [f'<link rel="alternate" hreflang="{code}" href="{language_url(code)}">' for code in LANGUAGES]
    return "\n".join(links)


def language_links(active="en"):
    links = [f'<a class="{"active" if active == "en" else ""}" href="{ORIGINAL}" hreflang="en">English</a>']
    for code, item in LANGUAGES.items():
        active_class = "active" if active == code else ""
        links.append(f'<a class="{active_class}" href="/{code}/artists/art-is-trash/" hreflang="{code}">{escape(item["name"])}</a>')
    return "".join(links)


def render_page(code, item):
    canonical = language_url(code)
    direction = ' dir="rtl"' if code == "ar" else ""
    sections = "".join(f'<section><h2>{escape(title)}</h2><p>{escape(text)}</p></section>' for title, text in item["sections"])
    return f'''<!DOCTYPE html><html lang="{code}"{direction}><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(item['title'])} | Urban Arts News</title><meta name="description" content="{escape(item['description'], quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}">{alternates()}<style>{CSS}</style></head><body><header class="top"><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a></header><section class="hero"><div class="hero-copy"><div class="eyebrow">{escape(item['label'])}</div><h1>{escape(item['heading'])}</h1><p>{escape(item['description'])}</p></div><img src="{IMAGE}" alt="Art Is Trash Francisco de Pájaro Barcelona street art" width="1600" height="1067"></section><main class="wrap"><article class="article">{sections}<div class="actions"><a class="button" href="/artists/art-is-trash/gallery/">{escape(item['gallery'])} →</a><a class="button dark" href="/urban-art-city/barcelona/spain/">{escape(item['city'])} →</a><a class="button dark" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram →</a><a class="button dark" href="{ORIGINAL}">{escape(item['original'])} →</a></div><section class="language-box"><h2>Art Is Trash · Languages</h2><div class="language-links">{language_links(code)}</div></section></article></main><footer><a href="/artists/art-is-trash/">Art Is Trash</a> · <a href="/artists/">Urban Artists</a> · <a href="/languages/">Languages</a></footer></body></html>'''


def patch_original():
    path = Path("artists/art-is-trash/index.html")
    html = path.read_text(encoding="utf-8")
    html = re.sub(r'\n?<section class="artist-language-versions[^"]*".*?</section>\n?', "\n", html, flags=re.I | re.S)
    block = f'''<section class="artist-language-versions"><h2>Urban Art Article Languages</h2><div class="language-links">{language_links('en')}</div></section>'''
    artist_info_marker = '<aside class="artist-info">'
    marker_position = html.find(artist_info_marker)
    if marker_position == -1:
        raise RuntimeError("Artist information block not found")
    copy_end = html.rfind("</div>", 0, marker_position)
    if copy_end == -1:
        raise RuntimeError("Artist text ending not found")
    html = html[:copy_end] + block + "\n\n" + html[copy_end:]
    html = re.sub(r'\n{3,}(?=<section class="artist-language-versions")', "\n\n", html)
    if "artist-language-style" not in html:
        style = '<style id="artist-language-style">.language-links{display:flex;flex-wrap:wrap;gap:9px;margin-top:18px}.language-links a{background:#111;color:#fff;padding:9px 12px;text-decoration:none;font-weight:800}.language-links a:hover,.language-links a.active{background:#ff5b21}</style>'
        html = html.replace("</head>", alternates() + style + "</head>", 1)
    html = re.sub(r'(?m)^[ \t]+$', '', html)
    path.write_text(html, encoding="utf-8")


def main():
    for code, item in LANGUAGES.items():
        output = Path(code) / "artists" / "art-is-trash" / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_page(code, item), encoding="utf-8")
    patch_original()
    print(f"Art Is Trash language profiles generated: {len(LANGUAGES)} plus English original")


if __name__ == "__main__":
    main()

from __future__ import annotations

from typing import Any

MESSAGES: dict[str, dict[str, Any]] = {
    "tr": {
        "app_title": "Kitap Atlası",
        "sidebar_tag": "Türkiye edebiyat haritası",
        "lang_label": "Dil",
        "btn_books": "Kitap listesi",
        "btn_search": "Kitap Ara",
        "btn_online_read": "Çevrimiçi Oku",
        "btn_stats": "İstatistikler",
        "btn_why_read": "Neden Kitap Okumalısın?",
        "btn_about": "Hakkımızda",
        "btn_map": "\U0001F5FA  Harita",
        "footer": "Kitap Atlası",
        "search_placeholder": "Kitap adı, yazar veya şehir ara\u2026",
        "search_hint": "Eşleşen kitap başlıkları",
        "book_list_window": "Kitap listesi",
        "book_list_title": "Tüm kitaplar",
        "book_list_hint": "Haritada göstermek için bir satıra çift tıklayın.",
        "online_reader_window": "Çevrimiçi Kitap Oku",
        "online_reader_title": "Ücretsiz Kitap Oku",
        "online_reader_hint": "Aşağıdan kitap arayabilir ve ücretsiz önizlemeleri okuyabilirsiniz.",
        "reader_search_btn": "Ara",
        "reader_read_btn": "\U0001F4D6 Çevrimiçi Oku",
        "reader_placeholder": "<i>Arama sonucunda bir kitap seçin</i>",
        "close": "Kapat",
        "about_window": "Kitap Atlası \u2014 Hakkımızda",
        "about_head": "Kitap Atlası",
        "about_sub": "Edebi mekânlar ve tarihsel bağlam",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "Teknik Altyapı",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>Dinamik Veri Entegrasyonu ve Okuma Arayüzü</b></p>"
            "<p>Bu proje, statik bir veri tabanı yerine RESTful API mimarisini "
            "kullanarak dinamik bir edebi içerik ekosistemi oluşturur. "
            "Sistemin \"Çevrimiçi Oku\" ve \"Kitap Bilgisi\" fonksiyonları, "
            "Open Library API uç noktaları (endpoints) üzerinden aşağıdaki "
            "protokollerle optimize edilmiştir:</p>"
            "<ul>"
            "<li><b>Arama ve Veri Sorgulama (Search Endpoint):</b> Uygulama, "
            "kullanıcı sorgularını <code>/search.json</code> uç noktasına "
            "ileterek asenkron bir veri çekme işlemi gerçekleştirir. Bu "
            "aşamada JSON formatında dönen ham veriler parse edilerek eserin "
            "OLID (Open Library Identifier) ve ISBN bilgileri ayıklanır.</li>"
            "<li><b>Görsel İşleme (Covers API):</b> Kullanıcı arayüzündeki "
            "(UI) estetik bütünlüğü sağlamak amacıyla, "
            "<code>/covers/{key_type}/{value}-{size}.jpg</code> protokolü "
            "kullanılır. Kitap kapakları, ISBN verisi üzerinden çekilerek "
            "belleği yormadan \"cache\" mekanizmasıyla arayüzdeki QLabel "
            "bileşenlerine dinamik olarak giydirilir.</li>"
            "<li><b>Mekansal Okuma Modülü (Books & Works API):</b> Harita "
            "üzerinde seçilen koordinatla eşleşen eserler, "
            "<code>/works/{olid}.json</code> yolu üzerinden sorgulanır. "
            "Eğer eserin telif durumu \"Public Domain\" (Kamu Malı) olarak "
            "işaretlenmişse, API'den dönen <code>read_url</code> bilgisi "
            "uygulamaya gömülü web motoru (QWebEngineView) üzerinden "
            "kullanıcıya sunulur.</li>"
            "<li><b>Sürdürülebilirlik ve Etik Kullanım:</b> Ticari "
            "kısıtlamaları ve maliyet gereksinimleri olan kapalı devre "
            "sistemler yerine; açık kaynaklı, API anahtarı gerektirmeyen "
            "ve anonim erişime izin veren bir yapı tercih edilmiştir. "
            "Bu, projenin ölçeklenebilirliğini ve akademik erişilebilirliğini "
            "artırmaktadır.</li>"
            "</ul></div>"
        ),
        "stats_window": "İstatistikler",
        "chart_top_cities": "En çok geçen 5 il (kitap sayısı)",
        "chart_books": "Kitap",
        "chart_count": "Adet",
        "chart_no_data": "Veri yok",
        "stats_genre_tab": "Tür",
        "stats_year_tab": "Yıl",
        "stats_sentiment_tab": "Duygu",
        "stats_records": "kitap kaydı",
        "status_loading": "Veri yükleniyor\u2026",
        "status_loaded": "{n} kitap yüklendi",
        "status_load_error": "Veri yüklenemedi",
        "msg_data_error": "Veri hatası",
    },
    "en": {
        "app_title": "Kitap Atlas",
        "sidebar_tag": "Map of Turkish literature",
        "lang_label": "Lang",
        "btn_books": "Book list",
        "btn_search": "Search Books",
        "btn_online_read": "Read Online",
        "btn_stats": "Statistics",
        "btn_why_read": "Why Read Books?",
        "btn_about": "About us",
        "btn_map": "\U0001F5FA  Map",
        "footer": "Kitap Atlas",
        "search_placeholder": "Search title, author, or city\u2026",
        "search_hint": "Matching book titles",
        "book_list_window": "Book list",
        "book_list_title": "All books",
        "book_list_hint": "Double-click a row to show it on the map.",
        "online_reader_window": "Read Books Online",
        "online_reader_title": "Read Free Books",
        "online_reader_hint": "Search for books below and read free previews.",
        "reader_search_btn": "Search",
        "reader_read_btn": "\U0001F4D6 Read Online",
        "reader_placeholder": "<i>Select a book from search results</i>",
        "close": "Close",
        "about_window": "Kitap Atlas \u2014 About",
        "about_head": "Kitap Atlas",
        "about_sub": "Literary places and historical context",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "Technical Infrastructure",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>Dynamic Data Integration & Reading Interface</b></p>"
            "<p>This project creates a dynamic literary content ecosystem "
            "using RESTful API architecture rather than a static database. "
            "The system's \"Read Online\" and \"Book Info\" functions "
            "are optimized through the following Open Library API "
            "endpoints and protocols:</p>"
            "<ul>"
            "<li><b>Search & Data Query (Search Endpoint):</b> The "
            "application sends user queries to the <code>/search.json</code> "
            "endpoint, performing an asynchronous data fetch. Raw JSON "
            "responses are parsed to extract the work's OLID (Open Library "
            "Identifier) and ISBN information.</li>"
            "<li><b>Image Processing (Covers API):</b> To maintain UI "
            "aesthetic integrity, the <code>/covers/{key_type}/{value}-{size}.jpg</code> "
            "protocol is used. Book covers are fetched via ISBN data and "
            "dynamically rendered into QLabel components through a "
            "memory-friendly cache mechanism.</li>"
            "<li><b>Spatial Reading Module (Books & Works API):</b> Works "
            "matching selected map coordinates are queried via "
            "<code>/works/{olid}.json</code>. If the work is marked as "
            "Public Domain, the <code>read_url</code> returned by the API "
            "is presented to the user through the embedded web engine "
            "(QWebEngineView).</li>"
            "<li><b>Sustainability & Ethical Use:</b> Instead of closed "
            "systems with commercial restrictions and API key requirements, "
            "an open-source, API-key-free architecture that allows anonymous "
            "access has been preferred. This enhances the project's "
            "scalability and academic accessibility.</li>"
            "</ul></div>"
        ),
        "stats_window": "Statistics",
        "chart_top_cities": "Top 5 provinces by book count",
        "chart_books": "Books",
        "chart_count": "Count",
        "chart_no_data": "No data",
        "stats_genre_tab": "Genre",
        "stats_year_tab": "Year",
        "stats_sentiment_tab": "Sentiment",
        "stats_records": "book records",
        "status_loading": "Loading data\u2026",
        "status_loaded": "{n} books loaded",
        "status_load_error": "Failed to load data",
        "msg_data_error": "Data error",
    },
    "de": {
        "app_title": "Kitap Atlas",
        "sidebar_tag": "Karte der türkischen Literatur",
        "lang_label": "Sprache",
        "btn_books": "Bücherliste",
        "btn_search": "Bücher suchen",
        "btn_online_read": "Online Lesen",
        "btn_stats": "Statistiken",
        "btn_why_read": "Warum Bücher lesen?",
        "btn_about": "Über uns",
        "btn_map": "\U0001F5FA  Karte",
        "footer": "Kitap Atlas",
        "search_placeholder": "Titel, Autor oder Stadt suchen\u2026",
        "search_hint": "Passende Buchtitel",
        "book_list_window": "Bücherliste",
        "book_list_title": "Alle Bücher",
        "book_list_hint": "Doppelklicken Sie eine Zeile, um sie auf der Karte anzuzeigen.",
        "online_reader_window": "Bücher Online Lesen",
        "online_reader_title": "Kostenlose Bücher Lesen",
        "online_reader_hint": "Suchen Sie unten nach Büchern und lesen Sie kostenlose Vorschauen.",
        "reader_search_btn": "Suchen",
        "reader_read_btn": "\U0001F4D6 Online lesen",
        "reader_placeholder": "<i>Wählen Sie ein Buch aus den Suchergebnissen</i>",
        "close": "Schließen",
        "about_window": "Kitap Atlas \u2014 Über",
        "about_head": "Kitap Atlas",
        "about_sub": "Literarische Orte und historischer Kontext",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "Technische Infrastruktur",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>Dynamische Datenintegration & Leseschnittstelle</b></p>"
            "<p>Dieses Projekt schafft ein dynamisches literarisches "
            "Inhaltsökosystem unter Verwendung einer RESTful-API-Architektur "
            "anstelle einer statischen Datenbank. Die Funktionen \"Online "
            "Lesen\" und \"Buchinfo\" werden durch die folgenden Open "
            "Library-API-Endpunkte optimiert:</p>"
            "<ul>"
            "<li><b>Suche & Datenabfrage:</b> Die Anwendung sendet "
            "Benutzeranfragen an den <code>/search.json</code>-Endpunkt "
            "und führt einen asynchronen Datenabruf durch.</li>"
            "<li><b>Bildverarbeitung (Covers API):</b> Zur Wahrung der "
            "ästhetischen Integrität der Benutzeroberfläche wird das "
            "<code>/covers/{key_type}/{value}-{size}.jpg</code>-Protokoll "
            "verwendet.</li>"
            "<li><b>Räumliches Lesemodul (Books & Works API):</b> Werke, "
            "die mit ausgewählten Kartenkoordinaten übereinstimmen, werden "
            "über <code>/works/{olid}.json</code> abgefragt.</li>"
            "</ul></div>"
        ),
        "stats_window": "Statistiken",
        "chart_top_cities": "Top 5 Provinzen nach Buchanzahl",
        "chart_books": "Bücher",
        "chart_count": "Anzahl",
        "chart_no_data": "Keine Daten",
        "stats_genre_tab": "Genre",
        "stats_year_tab": "Jahr",
        "stats_sentiment_tab": "Stimmung",
        "stats_records": "Buchdatensätze",
        "status_loading": "Daten werden geladen\u2026",
        "status_loaded": "{n} Bücher geladen",
        "status_load_error": "Daten konnten nicht geladen werden",
        "msg_data_error": "Datenfehler",
    },
    "es": {
        "app_title": "Kitap Atlas",
        "sidebar_tag": "Mapa de la literatura turca",
        "lang_label": "Idioma",
        "btn_books": "Lista de libros",
        "btn_search": "Buscar libros",
        "btn_online_read": "Leer en línea",
        "btn_stats": "Estadísticas",
        "btn_why_read": "¿Por qué leer libros?",
        "btn_about": "Sobre nosotros",
        "btn_map": "\U0001F5FA  Mapa",
        "footer": "Kitap Atlas",
        "search_placeholder": "Buscar título, autor o ciudad\u2026",
        "search_hint": "Títulos de libros coincidentes",
        "book_list_window": "Lista de libros",
        "book_list_title": "Todos los libros",
        "book_list_hint": "Haga doble clic en una fila para mostrarla en el mapa.",
        "online_reader_window": "Leer Libros en Línea",
        "online_reader_title": "Leer Libros Gratis",
        "online_reader_hint": "Busque libros a continuación y lea vistas previas gratuitas.",
        "reader_search_btn": "Buscar",
        "reader_read_btn": "\U0001F4D6 Leer en línea",
        "reader_placeholder": "<i>Seleccione un libro de los resultados</i>",
        "close": "Cerrar",
        "about_window": "Kitap Atlas \u2014 Acerca de",
        "about_head": "Kitap Atlas",
        "about_sub": "Lugares literarios y contexto histórico",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "Infraestructura Técnica",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>Integración Dinámica de Datos e Interfaz de Lectura</b></p>"
            "<p>Este proyecto crea un ecosistema dinámico de contenido "
            "literario utilizando una arquitectura API RESTful en lugar "
            "de una base de datos estática.</p>"
            "<ul>"
            "<li><b>Búsqueda y Consulta de Datos:</b> La aplicación envía "
            "consultas al endpoint <code>/search.json</code>.</li>"
            "<li><b>Procesamiento de Imágenes (Covers API):</b> Se utiliza "
            "el protocolo <code>/covers/{key_type}/{value}-{size}.jpg</code>.</li>"
            "</ul></div>"
        ),
        "stats_window": "Estadísticas",
        "chart_top_cities": "Top 5 provincias por cantidad de libros",
        "chart_books": "Libros",
        "chart_count": "Cantidad",
        "chart_no_data": "Sin datos",
        "stats_genre_tab": "Género",
        "stats_year_tab": "Año",
        "stats_sentiment_tab": "Sentimiento",
        "stats_records": "registros de libros",
        "status_loading": "Cargando datos\u2026",
        "status_loaded": "{n} libros cargados",
        "status_load_error": "No se pudieron cargar los datos",
        "msg_data_error": "Error de datos",
    },
    "fr": {
        "app_title": "Kitap Atlas",
        "sidebar_tag": "Carte de la littérature turque",
        "lang_label": "Langue",
        "btn_books": "Liste des livres",
        "btn_search": "Rechercher des livres",
        "btn_online_read": "Lire en ligne",
        "btn_stats": "Statistiques",
        "btn_why_read": "Pourquoi lire des livres?",
        "btn_about": "À propos",
        "btn_map": "\U0001F5FA  Carte",
        "footer": "Kitap Atlas",
        "search_placeholder": "Rechercher titre, auteur ou ville\u2026",
        "search_hint": "Titres de livres correspondants",
        "book_list_window": "Liste des livres",
        "book_list_title": "Tous les livres",
        "book_list_hint": "Double-cliquez sur une ligne pour l'afficher sur la carte.",
        "online_reader_window": "Lire des livres en ligne",
        "online_reader_title": "Lire des livres gratuits",
        "online_reader_hint": "Recherchez des livres ci-dessous et lisez des aperçus gratuits.",
        "reader_search_btn": "Rechercher",
        "reader_read_btn": "\U0001F4D6 Lire en ligne",
        "reader_placeholder": "<i>Sélectionnez un livre dans les résultats</i>",
        "close": "Fermer",
        "about_window": "Kitap Atlas \u2014 À propos",
        "about_head": "Kitap Atlas",
        "about_sub": "Lieux littéraires et contexte historique",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "Infrastructure Technique",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>Intégration Dynamique des Données et Interface de Lecture</b></p>"
            "<p>Ce projet crée un écosystème dynamique de contenu littéraire "
            "en utilisant une architecture API RESTful.</p>"
            "<ul>"
            "<li><b>Recherche & Interrogation de Données :</b> L'application "
            "envoie les requêtes à l'endpoint <code>/search.json</code>.</li>"
            "<li><b>Traitement d'Images (Covers API) :</b> Le protocole "
            "<code>/covers/{key_type}/{value}-{size}.jpg</code> est utilisé.</li>"
            "</ul></div>"
        ),
        "stats_window": "Statistiques",
        "chart_top_cities": "Top 5 provinces par nombre de livres",
        "chart_books": "Livres",
        "chart_count": "Nombre",
        "chart_no_data": "Pas de données",
        "stats_genre_tab": "Genre",
        "stats_year_tab": "Année",
        "stats_sentiment_tab": "Sentiment",
        "stats_records": "enregistrements de livres",
        "status_loading": "Chargement des données\u2026",
        "status_loaded": "{n} livres chargés",
        "status_load_error": "Échec du chargement des données",
        "msg_data_error": "Erreur de données",
    },
    "ja": {
        "app_title": "キタップ・アトラス",
        "sidebar_tag": "トルコ文学の地図",
        "lang_label": "言語",
        "btn_books": "書籍一覧",
        "btn_search": "本を検索",
        "btn_online_read": "オンラインで読む",
        "btn_stats": "統計",
        "btn_why_read": "なぜ本を読むのか？",
        "btn_about": "概要",
        "btn_map": "\U0001F5FA  地図",
        "footer": "Kitap Atlas",
        "search_placeholder": "タイトル、作者、都市を検索\u2026",
        "search_hint": "一致する書籍タイトル",
        "book_list_window": "書籍一覧",
        "book_list_title": "すべての書籍",
        "book_list_hint": "行をダブルクリックして地図に表示します。",
        "online_reader_window": "オンラインで書籍を読む",
        "online_reader_title": "無料で書籍を読む",
        "online_reader_hint": "以下で書籍を検索し、無料プレビューをお読みいただけます。",
        "reader_search_btn": "検索",
        "reader_read_btn": "\U0001F4D6 オンラインで読む",
        "reader_placeholder": "<i>検索結果から本を選択</i>",
        "close": "閉じる",
        "about_window": "Kitap Atlas \u2014 概要",
        "about_head": "Kitap Atlas",
        "about_sub": "文学の場所と歴史的背景",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "技術インフラ",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>動的データ統合と読書インターフェース</b></p>"
            "<p>このプロジェクトは、静的データベースの代わりにRESTful API "
            "アーキテクチャを使用して、動的な文学コンテンツエコシステムを"
            "作成します。</p>"
            "<ul>"
            "<li><b>検索とデータクエリ:</b> アプリケーションはユーザークエリを"
            "<code>/search.json</code>エンドポイントに送信します。</li>"
            "<li><b>画像処理（Covers API）:</b> "
            "<code>/covers/{key_type}/{value}-{size}.jpg</code>プロトコルが"
            "使用されます。</li>"
            "</ul></div>"
        ),
        "stats_window": "統計",
        "chart_top_cities": "書籍数の多い上位5県",
        "chart_books": "書籍",
        "chart_count": "数",
        "chart_no_data": "データなし",
        "stats_genre_tab": "ジャンル",
        "stats_year_tab": "年",
        "stats_sentiment_tab": "感情",
        "stats_records": "書籍レコード",
        "status_loading": "データを読み込み中\u2026",
        "status_loaded": "{n} 冊の本を読み込みました",
        "status_load_error": "データの読み込みに失敗しました",
        "msg_data_error": "データエラー",
    },
    "ru": {
        "app_title": "Китап Атлас",
        "sidebar_tag": "Карта турецкой литературы",
        "lang_label": "Язык",
        "btn_books": "Список книг",
        "btn_search": "Поиск книг",
        "btn_online_read": "Читать онлайн",
        "btn_stats": "Статистика",
        "btn_why_read": "Зачем читать книги?",
        "btn_about": "О нас",
        "btn_map": "\U0001F5FA  Карта",
        "footer": "Kitap Atlas",
        "search_placeholder": "Поиск названия, автора или города\u2026",
        "search_hint": "Совпадающие названия книг",
        "book_list_window": "Список книг",
        "book_list_title": "Все книги",
        "book_list_hint": "Дважды щелкните строку, чтобы показать ее на карте.",
        "online_reader_window": "Читать книги онлайн",
        "online_reader_title": "Читать бесплатные книги",
        "online_reader_hint": "Ищите книги ниже и читайте бесплатные превью.",
        "reader_search_btn": "Поиск",
        "reader_read_btn": "\U0001F4D6 Читать онлайн",
        "reader_placeholder": "<i>Выберите книгу из результатов поиска</i>",
        "close": "Закрыть",
        "about_window": "Kitap Atlas \u2014 О нас",
        "about_head": "Kitap Atlas",
        "about_sub": "Литературные места и исторический контекст",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "Техническая инфраструктура",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>Динамическая интеграция данных и интерфейс чтения</b></p>"
            "<p>Этот проект создает динамическую экосистему литературного "
            "контента, используя архитектуру RESTful API вместо статической "
            "базы данных.</p>"
            "<ul>"
            "<li><b>Поиск и запрос данных:</b> Приложение отправляет запросы "
            "пользователя на endpoint <code>/search.json</code>.</li>"
            "<li><b>Обработка изображений (Covers API):</b> Используется "
            "протокол <code>/covers/{key_type}/{value}-{size}.jpg</code>.</li>"
            "</ul></div>"
        ),
        "stats_window": "Статистика",
        "chart_top_cities": "Топ-5 провинций по количеству книг",
        "chart_books": "Книги",
        "chart_count": "Количество",
        "chart_no_data": "Нет данных",
        "stats_genre_tab": "Жанр",
        "stats_year_tab": "Год",
        "stats_sentiment_tab": "Настроение",
        "stats_records": "записей книг",
        "status_loading": "Загрузка данных\u2026",
        "status_loaded": "{n} книг загружено",
        "status_load_error": "Не удалось загрузить данные",
        "msg_data_error": "Ошибка данных",
    },
    "zh": {
        "app_title": "基塔普地图集",
        "sidebar_tag": "土耳其文学地图",
        "lang_label": "语言",
        "btn_books": "书单",
        "btn_search": "搜索书籍",
        "btn_online_read": "在线阅读",
        "btn_stats": "统计",
        "btn_why_read": "为什么要读书？",
        "btn_about": "关于我们",
        "btn_map": "\U0001F5FA  地图",
        "footer": "Kitap Atlas",
        "search_placeholder": "搜索书名、作者或城市\u2026",
        "search_hint": "匹配的书名",
        "book_list_window": "书单",
        "book_list_title": "所有书籍",
        "book_list_hint": "双击一行以在地图上显示。",
        "online_reader_window": "在线阅读书籍",
        "online_reader_title": "阅读免费书籍",
        "online_reader_hint": "在下方搜索书籍并阅读免费预览。",
        "reader_search_btn": "搜索",
        "reader_read_btn": "\U0001F4D6 在线阅读",
        "reader_placeholder": "<i>从搜索结果中选择一本书</i>",
        "close": "关闭",
        "about_window": "Kitap Atlas \u2014 关于",
        "about_head": "Kitap Atlas",
        "about_sub": "文学场所与历史背景",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "技术基础设施",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>动态数据集成与阅读界面</b></p>"
            "<p>本项目使用RESTful API架构而非静态数据库，"
            "创建了一个动态的文学内容生态系统。</p>"
            "<ul>"
            "<li><b>搜索与数据查询：</b>应用程序将用户查询发送到"
            "<code>/search.json</code>端点。</li>"
            "<li><b>图像处理（Covers API）：</b>使用"
            "<code>/covers/{key_type}/{value}-{size}.jpg</code>协议。</li>"
            "</ul></div>"
        ),
        "stats_window": "统计",
        "chart_top_cities": "书籍数量前5的省份",
        "chart_books": "书籍",
        "chart_count": "数量",
        "chart_no_data": "无数据",
        "stats_genre_tab": "流派",
        "stats_year_tab": "年份",
        "stats_sentiment_tab": "情感",
        "stats_records": "书籍记录",
        "status_loading": "正在加载数据\u2026",
        "status_loaded": "已加载 {n} 本书",
        "status_load_error": "数据加载失败",
        "msg_data_error": "数据错误",
    },
    "he": {
        "app_title": "קיטאפ אטלס",
        "sidebar_tag": "מפת הספרות הטורקית",
        "lang_label": "שפה",
        "btn_books": "רשימת ספרים",
        "btn_search": "חיפוש ספרים",
        "btn_online_read": "קריאה מקוונת",
        "btn_stats": "סטטיסטיקות",
        "btn_why_read": "למה לקרוא ספרים?",
        "btn_about": "אודות",
        "btn_map": "\U0001F5FA  מפה",
        "footer": "Kitap Atlas",
        "search_placeholder": "חיפוש כותרת, מחבר או עיר\u2026",
        "search_hint": "כותרות ספרים תואמות",
        "book_list_window": "רשימת ספרים",
        "book_list_title": "כל הספרים",
        "book_list_hint": "לחץ פעמיים על שורה כדי להציגה במפה.",
        "online_reader_window": "קריאת ספרים מקוונת",
        "online_reader_title": "קריאת ספרים חינם",
        "online_reader_hint": "חפש ספרים למטה וקרא תצוגות מקדימות בחינם.",
        "reader_search_btn": "חיפוש",
        "reader_read_btn": "\U0001F4D6 קרא באינטרנט",
        "reader_placeholder": "<i>בחר ספר מתוצאות החיפוש</i>",
        "close": "סגור",
        "about_window": "Kitap Atlas \u2014 אודות",
        "about_head": "Kitap Atlas",
        "about_sub": "מקומות ספרותיים והקשר היסטורי",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "תשתית טכנית",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>אינטגרציה דינמית של נתונים וממשק קריאה</b></p>"
            "<p>פרוייקט זה יוצר מערכת אקולוגית דינמית של תוכן ספרותי "
            "באמצעות ארכיטקטורת RESTful API במקום מסד נתונים סטטי.</p>"
            "<ul>"
            "<li><b>חיפוש ושאילתת נתונים:</b> היישום שולח שאילתות משתמש "
            "ל- endpoint <code>/search.json</code>.</li>"
            "<li><b>עיבוד תמונות (Covers API):</b> נעשה שימוש בפרוטוקול "
            "<code>/covers/{key_type}/{value}-{size}.jpg</code>.</li>"
            "</ul></div>"
        ),
        "stats_window": "סטטיסטיקות",
        "chart_top_cities": "5 המחוזות המובילים לפי מספר ספרים",
        "chart_books": "ספרים",
        "chart_count": "כמות",
        "chart_no_data": "אין נתונים",
        "stats_genre_tab": "ז'אנר",
        "stats_year_tab": "שנה",
        "stats_sentiment_tab": "רגש",
        "stats_records": "רשומות ספרים",
        "status_loading": "טוען נתונים\u2026",
        "status_loaded": "{n} ספרים נטענו",
        "status_load_error": "טעינת הנתונים נכשלה",
        "msg_data_error": "שגיאת נתונים",
    },
    "ky": {
        "app_title": "Китап Атлас",
        "sidebar_tag": "Түрк адабиятынын картасы",
        "lang_label": "Тил",
        "btn_books": "Китеп тизмеси",
        "btn_search": "Китеп издөө",
        "btn_online_read": "Онлайн окуу",
        "btn_stats": "Статистика",
        "btn_why_read": "Эмне үчүн китеп окуу керек?",
        "btn_about": "Биз жөнүндө",
        "btn_map": "\U0001F5FA  Карта",
        "footer": "Kitap Atlas",
        "search_placeholder": "Аталыш, автор же шаар издөө\u2026",
        "search_hint": "Шайкеш келген китеп аталыштары",
        "book_list_window": "Китеп тизмеси",
        "book_list_title": "Бардык китептер",
        "book_list_hint": "Картада көрсөтүү үчүн сапты эки жолу басыңыз.",
        "online_reader_window": "Китептерди Онлайн Окуу",
        "online_reader_title": "Акысыз Китептерди Окуу",
        "online_reader_hint": "Төмөндө китептерди издеп, акысыз көрүнүштөрдү окуңуз.",
        "reader_search_btn": "Издөө",
        "reader_read_btn": "\U0001F4D6 Онлайн окуу",
        "reader_placeholder": "<i>Издөө жыйынтыктарынан китеп тандаңыз</i>",
        "close": "Жабуу",
        "about_window": "Kitap Atlas \u2014 Биз жөнүндө",
        "about_head": "Kitap Atlas",
        "about_sub": "Адабий жерлер жана тарыхый контекст",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "about_techspec_title": "Техникалык инфраструктура",
        "about_techspec": (
            "<div style='line-height:1.6; font-size:12px;'>"
            "<p><b>Динамикалык маалыматтарды интеграциялоо жана окуу "
            "интерфейси</b></p>"
            "<p>Бул долбоор статикалык маалымат базасынын ордуна RESTful "
            "API архитектурасын колдонуу менен динамикалык адабий контент "
            "экосистемасын түзөт.</p>"
            "<ul>"
            "<li><b>Издөө жана маалымат суроо:</b> Колдонмо колдонуучунун "
            "суроолорун <code>/search.json</code> endpointке жөнөтөт.</li>"
            "<li><b>Сүрөт иштетүү (Covers API):</b> "
            "<code>/covers/{key_type}/{value}-{size}.jpg</code> протоколу "
            "колдонулат.</li>"
            "</ul></div>"
        ),
        "stats_window": "Статистика",
        "chart_top_cities": "Китеп саны боюнча алдыңкы 5 облус",
        "chart_books": "Китептер",
        "chart_count": "Саны",
        "chart_no_data": "Маалымат жок",
        "stats_genre_tab": "Жанр",
        "stats_year_tab": "Жыл",
        "stats_sentiment_tab": "Сезим",
        "stats_records": "китеп жазуулары",
        "status_loading": "Маалымат жүктөлүүдө\u2026",
        "status_loaded": "{n} китеп жүктөлдү",
        "status_load_error": "Маалыматтарды жүктөө мүмкүн эмес",
        "msg_data_error": "Маалымат катасы",
    },
}


def t(locale: str, key: str) -> Any:
    lang = locale.lower()
    if lang in MESSAGES:
        return MESSAGES[lang].get(key, MESSAGES["en"].get(key, key))
    if lang.startswith("tr"):
        return MESSAGES["tr"].get(key, key)
    return MESSAGES["en"].get(key, key)

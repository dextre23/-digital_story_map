import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "cached_books.json"
books = json.loads(DATA.read_text(encoding="utf-8"))

LONG_DESCRIPTIONS = {
    1: (
        "Çukurova'nın bereketli topraklarında geçen İnce Memed, toprak ağalığı düzenine başkaldıran "
        "bir gencin efsaneleşen hikâyesidir. Yaşar Kemal'in destansı anlatımıyla, Memed'in "
        "dağlarda tek başına başlattığı isyan, kısa sürede bütün bölgeye yayılır. Adana'nın "
        "sıcak ovalarında, pamuk tarlalarında ve Toros Dağları'nın eteklerinde geçen bu roman, "
        "bir yandan doğanın eşsiz tasvirlerini sunarken diğer yandan insan ruhunun derinliklerine iner. "
        "Memed'in adalet arayışı, haksızlığa karşı duruşu ve özgürlük tutkusu, ona halkın "
        "gözünde bir efsane kimliği kazandırır. Yaşar Kemal'in şiirsel diliyle bezeli bu başyapıt, "
        "Türk edebiyatının en önemli romanlarından biri olarak kabul edilir."
    ),
    2: (
        "Sezai Karakoç'un doğduğu topraklar olan Adıyaman/Kahta, Diriliş şairinin şiirlerinde "
        "sıkça yankılanır. Karakoç'un mistik şiir anlayışı, Kahta'nın kadim topraklarından "
        "beslenerek evrensel bir medeniyet tasavvuruna dönüşür. Şairin 'Soframız Nur Hanemiz Mamur' "
        "eserinde, Doğu ile Batı arasında sıkışmış bir ruhun diriliş mücadelesi anlatılır. "
        "Adıyaman'ın tarihi ve kültürel dokusu, Karakoç'un şiirlerinde sembolik bir dille yeniden "
        "inşa edilir. Bu eser, İslami düşüncenin modern Türk şiirindeki en önemli temsilcilerinden "
        "biridir ve okuru manevi bir yolculuğa çıkarır."
    ),
}

new_books = []
max_id = max(b["id"] for b in books)

extra_entries = [
    {
        "id": 0, "title": "Tutunamayanlar", "author": "Oğuz Atay",
        "publication_year": 1972, "city": "İstanbul",
        "location_name": "Beyoğlu, İstanbul",
        "coordinates": [41.0369, 28.9775],
        "genre": "Roman", "spatial_type": "Semt", "sentiment": "Ironik",
        "quote": "Hayat, anlamını yitirmiş bir oyundan ibaretti.",
        "description": "",
        "historical_context": "1970'ler Türk romanında modernizm ve bireyci varoluşçuluk.",
        "historical_context_en": "Modernism and individualist existentialism in 1970s Turkish novel."
    },
    {
        "id": 0, "title": "Saatleri Ayarlama Enstitüsü", "author": "Ahmet Hamdi Tanpınar",
        "publication_year": 1961, "city": "İstanbul",
        "location_name": "Sirkeci, İstanbul",
        "coordinates": [41.0150, 28.9770],
        "genre": "Roman", "spatial_type": "Semt", "sentiment": "Ironik",
        "quote": "Zaman, insanın içinde akar; saatler sadece birer araçtır.",
        "description": "",
        "historical_context": "Cumhuriyet modernleşmesi ve Doğu-Batı çatışması.",
        "historical_context_en": "Republican modernization and East-West conflict."
    },
    {
        "id": 0, "title": "Kürk Mantolu Madonna", "author": "Sabahattin Ali",
        "publication_year": 1943, "city": "Ankara",
        "location_name": "Merkez, Ankara",
        "coordinates": [39.9334, 32.8597],
        "genre": "Roman", "spatial_type": "Başkent", "sentiment": "Romantik",
        "quote": "Beni asıl anlayan, içimdeki yalnızlıktı.",
        "description": "",
        "historical_context": "1940'lar Türkiye'sinde aşk, yalnızlık ve yabancılaşma.",
        "historical_context_en": "Love, loneliness and alienation in 1940s Turkey."
    },
    {
        "id": 0, "title": "Bin Hüzünlü Haz", "author": "İsmet Özel",
        "publication_year": 1973, "city": "Kayseri",
        "location_name": "Merkez, Kayseri",
        "coordinates": [38.7312, 35.4787],
        "genre": "Şiir", "spatial_type": "İl merkezi", "sentiment": "Düşünsel",
        "quote": "Bin hüzünlü hazdır yaşamak, anladıkça çoğalan.",
        "description": "",
        "historical_context": "1970'ler Türk şiirinde ideolojik kırılmalar.",
        "historical_context_en": "Ideological shifts in 1970s Turkish poetry."
    },
    {
        "id": 0, "title": "Ruh Adam", "author": "Necip Fazıl Kısakürek",
        "publication_year": 1970, "city": "İstanbul",
        "location_name": "Üsküdar, İstanbul",
        "coordinates": [41.0250, 29.0150],
        "genre": "Roman", "spatial_type": "Semt", "sentiment": "Mistik",
        "quote": "Ruh, bedenin zindanında özgürlüğü arar.",
        "description": "",
        "historical_context": "Cumhuriyet dönemi mistik edebiyat ve birey ruhu.",
        "historical_context_en": "Republican-era mystical literature and the individual soul."
    },
    {
        "id": 0, "title": "Eylül", "author": "Mehmet Rauf",
        "publication_year": 1901, "city": "İstanbul",
        "location_name": "Boğaziçi, İstanbul",
        "coordinates": [41.0750, 29.0500],
        "genre": "Roman", "spatial_type": "Semt", "sentiment": "Melankolik",
        "quote": "Eylül, ayrılıkların ve hüznün mevsimidir.",
        "description": "",
        "historical_context": "Servet-i Fünûn dönemi ve psikolojik roman geleneği.",
        "historical_context_en": "Servet-i Fünun period and psychological novel tradition."
    },
]

LONG_TR = {
    "Tutunamayanlar": (
        "Oğuz Atay'ın başyapıtı Tutunamayanlar, modern Türk edebiyatının en önemli "
        "eserlerinden biridir. Roman, mühendis Turgut Özben'in arkadaşı Selim Işık'ın "
        "intiharının ardından onun hayatını araştırmasıyla başlar. İstanbul'un karmaşık "
        "sokaklarında, Beyoğlu'nun arka mahallelerinde geçen bu yolculuk, sıradan bir "
        "araştırmadan çok daha fazlasına dönüşür. Atay, ironik üslubuyla Türk aydınının "
        "bunalımını, toplumun dayattığı rolleri reddeden 'tutunamayan'ların hikâyesini "
        "anlatır. Roman, bilinç akışı tekniği, mektuplar, günlükler ve resmî belgeler gibi "
        "farklı anlatım biçimlerini bir araya getirerek postmodern edebiyatın Türkiye'deki "
        "en önemli örneklerinden biri haline gelir."
    ),
    "Saatleri Ayarlama Enstitüsü": (
        "Ahmet Hamdi Tanpınar'ın başyapıtı Saatleri Ayarlama Enstitüsü, Cumhuriyet'in ilk "
        "yıllarında kurulan hayalî bir kurum etrafında Türk modernleşmesinin absürtlüğünü "
        "hicveder. Romanın kahramanı Hayri İrdal, çocukluğundan itibaren zaman kavramıyla "
        "takıntılı bir ilişki geliştirir. Sirkeci'den Beyoğlu'na, İstanbul'un dönüşen "
        "yüzünde geçen bu hikâye, Doğu ile Batı arasında sıkışmış bir toplumun trajikomik "
        "portresini çizer. Tanpınar, saat metaforuyla modernleşmenin yüzeyselliğini ve "
        "insanın zamana yabancılaşmasını ustalıkla işler. Eser, Türk edebiyatında modern "
        "romanın doruk noktalarından biri kabul edilir."
    ),
    "Kürk Mantolu Madonna": (
        "Sabahattin Ali'nin en çok okunan eserlerinden Kürk Mantolu Madonna, Ankara'da "
        "sıradan bir memur olan Raif Efendi'nin geçmişte Almanya'da yaşadığı büyük aşkı "
        "anlatır. Roman, Ankara'nın soğuk sokaklarında başlayan bir tanışıklıkla açılır "
        "ve Raif Efendi'nin hatıra defteriyle geçmişe uzanır. Berlin'de tanıdığı ressam "
        "Maria Puder'e duyduğu derin ve karşılıksız aşk, onun iç dünyasını bütünüyle "
        "değiştirir. Sabahattin Ali, yalın ama etkileyici diliyle içe kapanık bir adamın "
        "zengin iç dünyasını ve aşkın dönüştürücü gücünü ustalıkla betimler. Eser, "
        "yalnızlık, aşk ve yabancılaşma temalarıyla evrensel bir değer taşır."
    ),
    "Bin Hüzünlü Haz": (
        "İsmet Özel'in gençlik dönemi şiirlerini topladığı Bin Hüzünlü Haz, Türk şiirinde "
        "bir dönüm noktasıdır. Kayseri'nin bozkırında başlayıp İstanbul'un karmaşasına "
        "uzanan şairin iç yolculuğu, bu eserde somut bir ifade bulur. Özel'in keskin imgelerle "
        "ördüğü şiirler, bireyin modern dünyadaki yalnızlığını ve varoluşsal sancılarını "
        "dile getirir. Şairin sosyalist düşünceden İslami duyarlılığa geçişinin izlerini "
        "taşıyan bu eser, ideolojik dönüşümlerin şiirsel bir haritası gibidir. İsmet Özel, "
        "bu kitapla Türk şiirine yeni bir soluk getirmiş ve kendine özgü bir şiir dili inşa etmiştir."
    ),
    "Ruh Adam": (
        "Necip Fazıl Kısakürek'in mistik romanı Ruh Adam, maddi dünyanın sınırlamalarından "
        "kurtulup ruhun özgürlüğüne ulaşma mücadelesini anlatır. Üsküdar'ın tarihî "
        "atmosferinde geçen roman, başkarakter Selim'in içsel hesaplaşmaları etrafında "
        "şekillenir. Necip Fazıl, sembolik ve fantastik ögelerle bezeli anlatımıyla, "
        "insanın görünenin ötesindeki gerçeklikle yüzleşmesini işler. Roman, zamanın "
        "ötesinde bir hikâye sunarak okuru ruhun derinliklerine doğru bir yolculuğa çıkarır. "
        "Türk edebiyatında mistik roman türünün en önemli örneklerinden biri olarak kabul edilir."
    ),
    "Eylül": (
        "Mehmet Rauf'un psikolojik romanı Eylül, Türk edebiyatında psikolojik türün ilk "
        "başarılı örneğidir. Boğaziçi'nin büyüleyici manzarası eşliğinde geçen romanda, "
        "bir yalıda yaşayan Suat ve Süreyya çiftinin arasına giren Suat'ın kuzeni Necip "
        "ile birlikte başlayan duygusal gerilim anlatılır. Mehmet Rauf, kahramanlarının "
        "iç dünyalarını ustalıkla betimleyerek yasak aşkın, kıskançlığın ve pişmanlığın "
        "ince bir analizini sunar. Eylül'ün melankolik atmosferi, mevsimin hüznüyle "
        "birleşerek okuru derinden etkileyen bir aşk hikâyesine dönüşür. Servet-i Fünûn "
        "edebiyatının en olgun eserlerinden biri olan roman, Türk romancılığında önemli bir dönüm noktasıdır."
    ),
}

for b in books:
    bid = b["id"]
    if bid in LONG_DESCRIPTIONS:
        b["description"] = LONG_DESCRIPTIONS[bid]
        b["description_tr"] = LONG_DESCRIPTIONS[bid]
    else:
        parts = b.get("description", "").split(".")
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) >= 2:
            extra_detail = (
                f" Eser, {b['city']} ve çevresinin tarihî, kültürel ve coğrafi "
                f"özelliklerini edebî bir dille yansıtarak okuyucuyu zamanda ve mekânda "
                f"bir yolculuğa çıkarır. {b['author']}\"in/ın benzersiz üslubuyla kaleme "
                f"alınan bu eser, {b['city']}\"in ruhunu ve insanlarının yaşayışını "
                f"derinlemesine keşfetme fırsatı sunar."
            )
            b["description"] = b["description"] + extra_detail
            b["description_tr"] = b["description_tr"] + extra_detail

next_id = max_id + 1
for entry in extra_entries:
    entry["id"] = next_id
    title = entry["title"]
    if title in LONG_TR:
        entry["description"] = LONG_TR[title]
        entry["description_tr"] = LONG_TR[title]
    else:
        entry["description"] = f"{title} eseri hakkında detaylı bilgi."
        entry["description_tr"] = f"{title} eseri hakkında detaylı bilgi."
    new_books.append(entry)
    next_id += 1

books.extend(new_books)
DATA.write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Updated: {len(books)} books total (added {len(new_books)} new)")

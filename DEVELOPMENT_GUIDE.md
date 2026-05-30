# Apex Data Solutions: Apify Actor Development Guide & AI Prompt

Tämä opas on tarkoitettu sinulle ja tuleville tekoälyapureillesi (kuten Antigravity). Se selittää tarkasti, miten nykyiset Actorit on rakennettu, miten uusia kehitetään, miten ne testataan paikallisesti ja miten ne julkaistaan tuottamaan rahaa.

Kopioi tiedoston lopussa oleva **AI-PROMPT** suoraan uudelle tekoälylle, kun haluat luoda uuden Actorin!

---

## 💡 Kultaiset säännöt rahan tienaamiseen Apify Storessa

1.  **Valitse oikea hinnoittelu (Pay-Per-Event / PPE)**:
    *   Aseta hinnoitteluksi **1,00 $ per 1 000 hakutulosta** (eli `$0.001` per tietorivi). Tämä houkuttelee asiakkaita kokeilemaan työkalua matalalla kynnyksellä.
2.  **Minimoi suorituskulut (Compute Costs)**:
    *   Käytä ensisijaisesti **suoria API-kutsuja (kuten Pexels API)** tai kevyitä HTTP-kirjastoja (kuten `httpx`, `BeautifulSoup` tai `Crawlee` Pythonilla).
    *   Vältä raskaita selaimia (Playwright/Puppeteer/Selenium), ellei se ole täysin välttämätöntä. Kevyt koodi pyörii **256 MB RAM**-muistilla sekunneissa, jolloin alustakustannukset ovat lähes 0,00 $ ja katteesi on 100 %.
3.  **Löydä matalan kilpailun markkinat**:
    *   Hae [Apify Ideas](https://apify.com/ideas) -taulusta ideoita, joilla on ääniä (esim. >10), mutta joita ei ole vielä tehty.
    *   AI-sisällöntuotannon apuvälineet (kuten kuvien/videoiden bulk-haku tekoälykanaville) ovat tällä hetkellä erittäin kysyttyjä.

---

## 📁 Projektin kansiorakenne (Python Boilerplate)

Jokainen uusi Actor rakennetaan seuraavalla rakenteella:

```text
apify_projekti/
│
├── .actor/
│   ├── actor.json          # Actorin metatiedot
│   ├── Dockerfile          # Ohje kontin rakentamiseen
│   └── INPUT_SCHEMA.json   # Konsolin syötekenttien määritys (käyttöliittymä)
│
├── src/
│   ├── __init__.py         # Paketin alustus
│   ├── __main__.py         # Asynkroninen käynnistystiedosto
│   └── main.py             # Varsinainen skraperi/logiikkakoodi
│
├── storage/                # Luodaan automaattisesti paikallisessa testauksessa
│   └── key_value_stores/
│       └── default/
│           └── INPUT.json  # Paikallisen testiajon syötteet
│
├── requirements.txt        # Python-kirjastot (esim. apify, httpx)
└── README.md               # Storen esittelysivu (markkinointiteksti)
```

---

## 🛠️ Paikallinen testaus (Local Workflow)

Ennen kuin lataat koodin Apifyhyn, testaa se aina paikallisesti:

1.  **Luo testisyöte**:
    Kirjoita tiedostoon `storage/key_value_stores/default/INPUT.json` haluamasi testiparametrit, esimerkiksi:
    ```json
    {
        "query": "nature",
        "maxResults": 5
    }
    ```
2.  **Asenna riippuvuudet**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Aja skripti**:
    ```bash
    python -m src
    ```
4.  **Tarkista tulokset**:
    Tulokset tallentuvat kansioon `storage/datasets/default/`. Avaa `.json`-tiedostot ja varmista, että data on oikeassa muodossa.

---

## 🚀 Julkaisu Apify Storessa

Kun koodi toimii paikallisesti:

1.  Mene [Apify Consoleen](https://console.apify.com/) ja valitse **Actors -> My Actors -> Create new**.
2.  Valitse **Python empty template**.
3.  Anna Actorille nimeksi haluamasi (esim. `pexels-scraper`).
4.  Mene **Source**-välilehdelle ja kopioi/tallenna tiedostojen sisällöt verkkoeditoriin. Varmista, että kansiorakenne vastaa paikallista (siirrä tiedostot oikeisiin kansioihin).
5.  Klikkaa **Save & Build** oikeasta yläkulmasta ja odota, että Build valmistuu (vihreä valo).
6.  Klikkaa Actoria ja aja testiajo (Run) varmistaaksesi, että se toimii alustalla.
7.  Mene **Publication**-välilehdelle:
    *   Täytä näyttönimi, lyhyt kuvaus ja kategoriat.
    *   Valitse **Monetization**: Aseta **Pay-per-event (PPE)** ja hinnaksi `$1.00 / 1000` tapahtumalle `result` (apify-default-dataset-item).
    *   Tallenna ja klikkaa **Publish on Store**.

---

## 🤖 KOPIOITAVA TEKOÄLY-PROMPT UUTTA PROJEKTIA VARTEN

Kopioi alla oleva teksti ja lähetä se tekoälylle, kun haluat aloittaa uuden Actorin tekemisen:

```text
Sinä olet asiantunteva AI-koodausassistentti. Tehtäväsi on luoda uusi Apify Actor (Python) noudattaen Apex Data Solutionsin kehitysstandardeja. 

Kehitämme uutta Actoria kansioon "c:\Users\mikko\Desktop\apify_[projektin_nimi]".

Noudata seuraavia ohjeita tarkasti:
1. Luo seuraava tiedostorakenne:
   - requirements.txt (asenna vähintään 'apify>=1.3.0' ja 'httpx>=0.27.0')
   - .actor/actor.json (määritä nimi, versio "0.1" ja Dockerfile-polku)
   - .actor/Dockerfile (käytä kuvaa 'apify/actor-python:3.11', aja komento 'CMD ["python3", "-m", "src"]')
   - .actor/INPUT_SCHEMA.json (määritä käyttöliittymän syötteet: hakusanat, limitit jne.)
   - src/__init__.py
   - src/__main__.py (käynnistää asynkronisen main-funktion)
   - src/main.py (sisältää Actor.get_input(), asynkronisen httpx-haun, virheidenkäsittelyn ja Actor.push_data())
   - README.md (houkutteleva englanninkielinen esittely Apify Storea varten, jossa mainitaan PPE-hinnoittelu)

2. Ohjeet koodaukseen:
   - Käytä aina tehokasta asynkronista httpx.AsyncClient-kirjastoa suoriin API- tai verkkohakuihin.
   - Varmista, että koodi on kevyt eikä käytä turhaan selaimia (kuten Playwrightia), ellei kohdesivusto vaadi sitä.
   - Normalisoi tulokset siistiksi JSON-rakenteeksi ennen tallennusta.
   - Käytä virheidenkäsittelyssä ja ilmoituksissa Apify SDK:n sisäänrakennettuja työkaluja (Actor.fail(), Actor.exit()).

3. Paikallinen testaus:
   - Luo mock-syöte tiedostoon 'storage/key_value_stores/default/INPUT.json' ja aja paikallinen testi komennolla 'python -m src' varmistaaksesi toimivuuden.

Kun olet luonut tiedostot ja testannut ne, käytä selaintyökaluja (browser-subagent) luodaksesi uuden Actorin Apify Consoleen, siirtääksesi koodit sinne, buildataksesi sen ja julkaistaksesi sen Apify Storeen PPE-hinnoittelulla ($1.00 per 1000 tulosta).
```

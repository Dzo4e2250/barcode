# EAN Barcode Generator

EAN Barcode Generator je spletna aplikacija namenjena uporabnikom, ki prejemajo seznam EAN kod (13-mestne številke) in potrebujejo hitro generiranje barkod v PDF formatu. Aplikacija omogoča enostaven vnos EAN kod s kopiranjem in lepljenjem podatkov iz preglednice, nato pa generira PDF dokument, kjer se barkode izpišejo na desni tretjini A4 strani. To je idealno za tiste, ki se ukvarjajo s skladiščem, trgovino ali logistiko in potrebujejo hiter način za pretvorbo EAN kod v skenirljive barkode.

## Funkcionalnosti

- **Vnos EAN kod**: Uporabnik lahko vnese več EAN kod naenkrat tako, da jih kopira in prilepi v obrazec.
- **Generiranje PDF dokumenta**: Aplikacija generira PDF, kjer so barkode prikazane na desni tretjini strani, eno pod drugo.
- **Prilagoditev za A4 format**: Barkode so prilagojene tako, da se prilegajo desni tretjini A4 strani, PDF pa se samodejno prilagodi tudi, če je več kod, kot jih lahko prikaže na eni strani.
- **Uporaba Dockerja**: Enostavno nameščanje in zagon aplikacije s pomočjo Dockerja.

## Za koga je aplikacija namenjena?

EAN Barcode Generator je namenjen uporabnikom, ki redno delajo s tabelami EAN kod in potrebujejo skenirljive barkode. Z aplikacijo lahko preprosto kopirajo in prilepijo svoje EAN kode ter dobijo PDF dokument, ki vsebuje vse barkode na enem mestu. To je posebej uporabno za:

- **Skladiščne delavce in vodje**: Za hitro generiranje barkodov za prepoznavanje izdelkov.
- **Logistična podjetja**: Za organizacijo in označevanje paketov.
- **Trgovine in maloprodajo**: Za generiranje barkodov pri sledenju zalogam.

## Kako zagnati aplikacijo

### Predpogoji

- [Docker](https://www.docker.com/) mora biti nameščen na vašem sistemu.
- Priporočamo tudi Git za kloniranje repozitorija, vendar ni nujno potreben.

### Koraki za zagon aplikacije

1. Klonirajte repozitorij:
   ```bash
   git clone https://github.com/Dzo4e2250/barcode
   cd barcode-main
2. Zgradi Docker sliko:
   ```bash
   docker build -t ean-barcode-app .
3. Zaženi Docker kontejner:
   ```bash
   docker run -d -p 5000:5000 ean-barcode-app
4. Odpri aplikacijo v brskalniku: Ko je kontejner zažene, lahko dostopaš do aplikacije na naslovu:
   ```bash
   http://localhost:5000

##Uporaba aplikacije:

- Vnesite ali prilepite EAN kode v obrazec na spletni strani.
- Kliknite na gumb Generiraj PDF z barkodami.
- Aplikacija bo generirala PDF dokument, ki ga lahko prenesete in uporabite.

###Struktura datotek

- **app.py**: Glavna Python aplikacija, ki uporablja Flask za spletno streženje in ReportLab za generiranje PDF dokumentov.
- **templates/index.html**: Spletna stran za vnos EAN kod.
- **Dockerfile**: Konfiguracijska datoteka za ustvarjanje Docker slike.
- **requirements.txt**: Seznam Python knjižnic, ki jih aplikacija potrebuje za delovanje.

##Tehnične zahteve

Aplikacija uporablja naslednje knjižnice:

- **Flask**: Za izdelavo spletnega vmesnika.
- **ReportLab**: Za generiranje PDF dokumentov.
- **python-barcode**: Za generiranje barkodov iz EAN kod.

Vse potrebne knjižnice so navedene v datoteki **requirements.txt** in se avtomatično namestijo, ko Docker slika gradi aplikacijo.

5. Pogosta vprašanja

##Zakaj se aplikacija ne zažene?
Preverite, ali imate pravilno nameščen Docker in če sledite korakom za zagon slike in kontejnerja.

6. PDF dokument ne prikazuje barkodov, kaj naj storim?
Poskrbite, da so vse EAN kode pravilno vnešene kot 13-mestne številke. Če napaka še vedno vztraja, preverite loge Docker kontejnerja s tem ukazom:
   ```bash
      docker logs <container_id>

7. Kako ustavim aplikacijo?
Poiščite ID kontejnerja z ukazom docker ps, nato pa ustavite kontejner z naslednjim ukazom:
   ```bash
   docker stop <container_id>
8. Prispevanje
Če želite prispevati k projektu, se obrnite na nas ali predložite pull request. Veselimo se vaših izboljšav in predlogov!




  

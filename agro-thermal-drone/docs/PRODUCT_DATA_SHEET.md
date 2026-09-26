# KARTA PRODUKTU (PRODUCT DATA SHEET)
# URSUS AGRO-SENTINEL 7" THERMAL
### Autonomiczny bezzałogowy system monitoringu upraw i aktywnego odstraszania zwierzyny

---

## 1. OPIS SYSTEMU
**URSUS AGRO-SENTINEL 7"** to ultra-lekki, autonomiczny dron rolniczy nowej generacji, zaprojektowany do nocnego i porannego patrolowania pól uprawnych (kukurydza, rzepak, zboża, łąki). 

Wyposażony w miniaturową matrycę termowizyjną **Caddx Eclipse**, pokładowy procesor sztucznej inteligencji **NPU** oraz kierunkową **syrenę odstraszającą 118 dB**, system w pełni samodzielnie patroluje uprawy po zaplanowanej siatce, wykrywa żerujące dziki lub jelenie i natychmiast wypłasza je w stronę lasu, ratując plony przed szkodami łowieckimi.

---

## 2. GŁÓWNE ZASTOSOWANIA
* **Aktywny patrol anty-dzik:** Nocne i poranne wykrywanie watah dzików w wysokim łanie kukurydzy i ich automatyczne wypłaszanie syreną piezo i stroboskopem.
* **Ratowanie koźląt (Fawn Rescue):** Skanowanie łąk przed pierwszym pokosem traw w celu ochrony młodych saren przed kosiarkami (cichy tryb zapisu pozycji GPS).
* **Szacowanie i dokumentacja strat:** Generowanie georeferencyjnych raportów PDF ze zdjęciami termicznymi dla kół łowieckich i ubezpieczycieli.

---

## 3. SPECYFIKACJA TECHNICZNA

| Kategoria | Parametr | Wartość / Opis |
| :--- | :--- | :--- |
| **Konstrukcja** | Typ płatowca | Składany Quadcopter węglowy klasy 7" Long-Range |
| | Wymiary transportowe | Mieści się w standardowym plecaku turystycznym |
| | Masa startowa (AUW) | **1,47 kg** (z baterią 6S2P i pełnym wyposażeniem) |
| **Osiągi i Zasilanie** | Czas misji roboczej | **ok. 37 minut** (z 15% rezerwą na powrót RTL; max. 43 min) |
| | Pokrycie terenu na 1 locie | **ponad 50 hektarów** (21 km pokonanej trasy w siatce) |
| | Akumulator | Pakiet Li-Ion 6S2P (12x ogniwa Molicel INR-21700-P45B, 9000 mAh) |
| | Odporność na wiatr | Do 10–12 m/s (silniki 2807 1300KV, śmigła 7") |
| **System Wizyjny** | Kamera termowizyjna | **Caddx Eclipse** (mikrobolometr VOx, 640×512 lub 384×288 px, 50 Hz, waga 32 g) |
| | Kamera dzienna | Caddx Ratel 2 (podgląd dzienny z przełącznikiem obrazu) |
| | Transmisja wideo | Cyfrowa Walksnail Avatar HD Mini V2 lub analogowa 1.6W (zasięg >10 km) |
| **Sztuczna Inteligencja** | Koprocesor pokładowy | **Rockchip NPU (RV1106)**, waga 9 g, pobór mocy < 1,5 W |
| | Model detekcji | **YOLOv8-Nano INT8** (30 FPS na żywo w locie) |
| | Identyfikowane klasy | Dzik, Sarna/Jeleń, Koźlę leżące w trawie, Człowiek, Bydło |
| | Rzutowanie GPS celu | Automatyczny przelicznik: piksel matrycy $\rightarrow$ współrzędne GPS celu |
| **System Odstraszania** | Akustyka | Podwójna syrena piezoelektryczna **118 dB SPL @ 1 m** (częstotliwość 2,8–3,5 kHz) |
| | Optyka płosząca | Dioda stroboskopowa LED 10W (błyski 14 Hz dezorientujące zwierzynę nocną) |
| | Masa modułu | Łącznie zaledwie **45 gramów** (pobór prądu < 3W) |
| **Nawigacja i Awionika**| Autopilot | SpeedyBee F405 V4 Stack z oprogramowaniem **ArduPilot** |
| | Pozycjonowanie | Moduł GNSS Matek M10Q (GPS/Galileo/GLONASS) + Kompas |
| | Utrzymanie pułapu | Lidar laserowy (precyzyjne śledzenie wysokości nad łanem uprawy) |
| **Oprogramowanie GCS** | Aplikacja sterująca | Dedykowana aplikacja **"Ursus Agro-Pilot"** (na tablet/laptop) |
| | Funkcjonalności | 1-przyciskowy start misji, import granic działek z ARiMR/Geoportalu, automatyczny raport PDF |

---

## 4. KOSZT I EKONOMIA PROJEKTU
* **Szacowany koszt jednostkowy komponentów (BOM):** **~3 500 – 3 800 PLN netto**
* **Porównanie z konkurencją:** Tradycyjny dron przemysłowy z termowizją (np. DJI Mavic 3 Enterprise Thermal) to wydatek rzędu **25 000 – 30 000 PLN** i brak wbudowanego systemu odstraszania.
* **Cena rynkowa (propozycja):** 6 900 – 8 900 PLN brutto (marża brutto na poziomie >100% przy zachowaniu bezkonkurencyjnej ceny dla rolnika).

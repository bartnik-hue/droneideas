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
| **System Wizyjny** | Kamera termowizyjna | **Caddx Eclipse** (mikrobolometr VOx, 640×512 lub 384×288 px, 50 Hz, waga 32 g) – szeroki skan z 45m |
| | Kamera dzienna / RGB | **SIYI A8 mini** (1/1.7" Sony Starlight 4K, 6X zoom, 3-osiowy gimbal bezszczotkowy, slot MicroSD 4K, waga zaledwie 95 g) |
| | Doświetlenie nocne | Dolny reflektor LED 10–20W (5000 lm) o podwójnej roli (szperacz weryfikacyjny + stroboskop płoszący) |
| | Transmisja wideo | Cyfrowa Walksnail Avatar HD Mini V2 lub analogowa 1.6W (zasięg >10 km) |
| **Sztuczna Inteligencja** | Procedura detekcji | **Dwuetapowa (Two-Stage):** 1. Wykrycie plamy ciepła w termowizji -> 2. Zniżenie na 15m, doświetlenie LED i weryfikacja RGB |
| | Koprocesor pokładowy | **Rockchip NPU (RV1106)**, waga 9 g, pobór mocy < 1,5 W |
| | Model detekcji | **YOLOv8-Nano INT8** (30 FPS na żywo w locie) |
| | Identyfikowane klasy | Dzik, Sarna/Jeleń, Koźlę leżące w trawie, Człowiek, Bydło (eliminacja nagrzanych kamieni) |
| | Rzutowanie GPS celu | Automatyczny przelicznik: piksel matrycy $\rightarrow$ współrzędne GPS celu |
| **System Odstraszania** | Akustyka | Podwójna syrena piezoelektryczna **118 dB SPL @ 1 m** (częstotliwość 2,8–3,5 kHz) |
| | Optyka płosząca | Dioda stroboskopowa LED 10W (błyski 14 Hz dezorientujące zwierzynę nocną po potwierdzeniu dzika) |
| | Masa modułu | Łącznie zaledwie **45 gramów** (pobór prądu < 3W podczas wycia) |
| **Nawigacja i Awionika**| Autopilot | SpeedyBee F405 V4 Stack z oprogramowaniem **ArduPilot** |
| | Pozycjonowanie | Moduł GNSS Matek M10Q (GPS/Galileo/GLONASS) + Kompas |
| | Utrzymanie pułapu | Lidar laserowy (precyzyjne śledzenie wysokości nad łanem uprawy) |
| **Oprogramowanie GCS** | Aplikacja sterująca | Dedykowana aplikacja **"Ursus Agro-Pilot"** (na tablet/laptop) |
| **Stacja Dokująca (Opcja)**| Pozycjonowanie i Dokowanie | Stacja bazowa RTK (u-blox ZED-F9P, precyzja 1–2 cm) + optyczny AprilTag IR (850 nm) |
| | Ładowanie i Bezpieczeństwo | Płyta stykowa CC-CV (25,2V 7A, 50-60 min) z autodetekcją polaryzacji i odcięciem 0V |
| | Sensoryka Pogodowa | Ultradźwiękowy anemometr (wiatr), optyczny czujnik opadów deszczu, modem 4G LTE |

---

## 4. KOSZT I EKONOMIA PROJEKTU (ZESTAWIENIE MODUŁOWE)

### 4.1. Wariant 1: Dron "Agro-Sentinel 7"" Solo (Manualny start z plecaka)
* **Koszt komponentów (BOM):** **~5 750 PLN netto** (z kamerą termowizyjną Caddx 640 VOx, 3-osiowym gimbalem 4K SIYI A8 mini, NPU RV1106, RTK Rover i syreną 118 dB)
* **Sugerowana cena detaliczna:** **~11 900 PLN brutto**
* **Porównanie rynkowe:** DJI Mavic 3 Enterprise Thermal to wydatek rzędu **~27 000 PLN brutto** (nasz system jest ponad 2× tańszy, a posiada wbudowaną syrenę płoszącą, stroboskop i NPU AI).

### 4.2. Wariant 2: Pełny System Autonomiczny (Dron + Stacja Dokująca 230V)
* **Koszt komponentów (BOM):** **~11 130 PLN netto** (Dron ~5 755 zł + Stacja dokująca ze stacją meteo i bazą RTK ~5 375 zł)
* **Sugerowana cena detaliczna:** **~23 900 PLN brutto**
* **Porównanie rynkowe:** Komercyjna stacja **DJI Dock 2 + Matrice 3TD** kosztuje **~54 000 PLN brutto** (nasz system oferuje 100% autonomii nocnej przy ponad 2-krotnie niższej cenie i dedykowanym algorytmie ochrony przed dzikami).

### 4.3. Wariant 3: System Polowy Off-Grid (Dron + Stacja + Solary 380W + LiFePO4)
* **Koszt komponentów (BOM):** **~13 270 PLN netto** (w tym panel PV 380W, regulator MPPT i magazyn energii LiFePO4 1,28 kWh)
* **Sugerowana cena detaliczna:** **~27 900 PLN brutto** (odpowiednik przemysłowych stacji Heisha / Percepto za 80 000 – 120 000 PLN).

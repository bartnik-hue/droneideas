# SZCZEGÓŁOWA ANALIZA KOSZTÓW I ZESTAWIENIE BOM
## System Autonomiczny "Ursus Agro-Sentinel 7"" & Stacja Bazowa (Drone-in-a-Box)

---

### 1. Wprowadzenie do Kalkulacji Finansowej

Wraz z rozbudową projektu o:
1. **Głowicę dzienną 4K na 3-osiowym gimbalu ([SIYI A8 mini](file:///d:/URSUS/agro-thermal-drone/hardware/RGB_CAMERA_AND_GIMBAL_SELECTION.md))** do dwuetapowej weryfikacji celów,
2. **Pokładowy koprocesor neuronowy [Rockchip RV1106 NPU](file:///d:/URSUS/agro-thermal-drone/software/AI_INFERENCE_ARCHITECTURE.md)** do inferencji YOLOv8 w 30 FPS,
3. **Moduł odbiornika nawigacji RTK Rover** na dronie (dokładność 1–2 cm),
4. **Autonomiczną Stację Bazową ([Drone-in-a-Box Base Station](file:///d:/URSUS/agro-thermal-drone/hardware/BASE_STATION_COMPONENTS.md))** z ładowaniem stykowym, stacją meteo i bazą RTK,

kosztorys został podzielony na **dwie niezależne pozycje modułowe**:
* **Moduł A:** Samodzielny Dron Rolniczy (obsługa ręczna / z plecaka przez rolnika).
* **Moduł B:** Autonomiczna Stacja Bazowa (przekształcająca drona w system w 100% bezzałogowy).

---

### 2. BOM Drona: "Ursus Agro-Sentinel 7"" (Zestaw Lotny)

Poniższe zestawienie obejmuje pełen koszt części (BOM) gotowego do lotu quadcoptera 7" z podwójną sensoryką (termowizja Caddx + gimbal 4K SIYI), koprocesorem AI, nawigacją RTK i aktywnym systemem odstraszania:

| Lp. | Podsystem / Komponent | Rekomendowany Model / Specyfikacja | Waga (g) | Koszt Netto (PLN) |
| :---: | :--- | :--- | :---: | :---: |
| **1** | **Płatowiec (Rama)** | 7" Long-Range Carbon 3K (grubość ramion 5–6 mm) | 190 g | 240 zł |
| **2** | **Zespół napędowy** | 4x EMAX ECO II 2807 1300KV + śmigła HQProp 7x4x3 | 225 g | 400 zł |
| **3** | **Sterowanie lotem (Stack)**| SpeedyBee F405 V4 55A ESC (z firmware ArduPilot) | 45 g | 360 zł |
| **4** | **Nawigacja precyzyjna** | Odbiornik Matek M10-RTK / F9P Rover + Kompas | 24 g | 480 zł |
| **5** | **Wysokościomierz AGL** | Mini Lidar laserowy (ToF 0,1–12 m, pomiar nad uprawą) | 12 g | 110 zł |
| **6** | **Kamera termowizyjna** | **Caddx Eclipse 640 VOx** (50 Hz, mikrobolometr) | 32 g | 1 650 zł |
| **7** | **Kamera dzienna + Gimbal** | **SIYI A8 mini 4K** (1/1.7" Sony, 6X zoom, gimbal 3-osiowy, MicroSD) | 95 g | 1 350 zł |
| **8** | **Koprocesor Edge AI** | Rockchip RV1106 NPU (0.5 TOPS, YOLOv8-Nano INT8) | 9 g | 75 zł |
| **9** | **Doświetlenie nocne LED** | Szperacz / Stroboskop LED 20W (5000 lm) z radiatorem | 28 g | 65 zł |
| **10**| **System odstraszania** | Podwójna syrena piezoelektryczna 118 dB SPL @ 1m + MOSFET | 45 g | 45 zł |
| **11**| **Transmisja VTX / C2** | Cyfrowy Walksnail Avatar HD Mini V2 (lub Analog 1.6W) | 28 g | 420 zł |
| **12**| **Link RC / Telemetria** | ExpressLRS 868 MHz Dual Diversity (zasięg >15 km) | 8 g | 95 zł |
| **13**| **Złącza lądowiska stacji** | 4x Sprężynowe styki Pogo-Pin wysokoprądowe (na płozach) | 15 g | 35 zł |
| **14**| **Akumulator Li-Ion** | Pakiet 6S2P (12x ogniw Molicel INR-21700-P45B, 9000 mAh) | 880 g | 370 zł |
| **15**| **Okablowanie i drobnica** | Kable silikonowe, kondensatory low-ESR, śruby tytanowe | 40 g | 60 zł |
| -- | **SUMA (DRON GOTOWY DO LOTU)** | **Masa startowa: ~1 648 g (AUW)** | **~1,65 kg** | **~5 755 zł netto** |

> **Uwaga optymalizacyjna (Wariant Budżetowy Drona):**  
> W przypadku zastosowania matrycy termowizyjnej Caddx Eclipse 384 (zamiast 640) oraz standardowego sensora GNSS M10Q, koszt BOM drona spada do **~4 400 zł netto**.

---

### 3. BOM Autonomicznej Stacji Bazowej (Drone-in-a-Box)

Poniższe zestawienie obejmuje podzespoły naziemnej stacji dokującej umożliwiającej bezzałogowy cykl życia drona:

| Lp. | Podsystem Stacji | Rekomendowany Podzespół | Rola i Funkcja | Koszt Netto (PLN) |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Baza GNSS RTK** | **u-blox ZED-F9P Multi-Band** + antena geodezyjna survey | Nadawanie poprawek RTCM3 do drona (dokładność lądowania 1–2 cm) | 1 180 zł |
| **2** | **Optyka dokowania** | Znacznik AprilTag/ArUco + ring diod IR 850 nm (12V) | Wizualne centrowanie drona w nocy (kamera dolna) | 120 zł |
| **3** | **Płyta lądowiska** | Płyta ze stykami mosiężnymi niklowanymi + sensory nacisku | Fizyczne lądowisko i detekcja obecności drona | 380 zł |
| **4** | **Autodetekcja polaryzacji** | Mostek prostowniczy MOSFET (Ideal Diode Controller) | Umożliwia lądowanie pod dowolnym kątem obrotu | 140 zł |
| **5** | **Szybka ładowarka CC/CV** | Moduł przemysłowy 25.2V 7.0A (180W) sterowany UART | Ładowanie pakietu 6S2P 9000 mAh w 50–60 min | 260 zł |
| **6** | **Przekaźnik bezpieczeństwa** | Przekaźnik półprzewodnikowy SSR / Contactor | 0,0V na stykach dopóki dron nie wyląduje (ochrona przed zwarciem) | 75 zł |
| **7** | **Anemometr wiatru** | Ultradźwiękowy anemometr RS485 (Sonic Anemometer) | Pomiar prędkości i porywów wiatru (brak ruchomych części) | 480 zł |
| **8** | **Sensor opadów** | Optyczny czujnik deszczu (na podczerwień) | Błyskawiczna detekcja pierwszych kropel deszczu | 160 zł |
| **9** | **Sensor środowiskowy** | Moduł BME280 (temperatura, wilgotność, ciśnienie) | Obliczanie punktu rosy (ochrona przed oblodzeniem) | 35 zł |
| **10**| **Mózg stacji (SBC)** | **Raspberry Pi 5 (4GB)** + obudowa DIN + radiator | Zarządzanie harmonogramem, pre-flight check, diagnostyka | 390 zł |
| **11**| **Pamięć masowa stacji** | Dysk SSD NVMe 256GB (ze złączem PCIe HAT) | Bufor nagrań 4K z nocnych misji przed wysłaniem | 140 zł |
| **12**| **Modem komórkowy** | Przemysłowy router 4G LTE **Teltonika RUT241** (lub Quectel) | Przesyłanie alertów SMS/Telegram i raportów PDF rolnikowi | 690 zł |
| **13**| **Lokalne Wi-Fi** | Karta Wi-Fi 5 GHz (802.11ac) z anteną dookólną | Zrzut nagrań 4K z kamery SIYI A8 mini w < 90 sekund | 85 zł |
| **14**| **Telemetria daleka** | Moduł LoRa 868 MHz 1000 mW (MAVLink Ground Radio) | Niezależny kanał nadzoru lotu do 10 km bez sieci GSM | 110 zł |
| **15**| **Zasilanie stacji (230V)** | Zasilacz Mean Well LRS-350-24 + mini bufor UPS | Zasilanie stacji z sieci gospodarstwa | 280 zł |
| **16**| **Konstrukcja i siłowniki**| Obudowa IP65, siłownik elektryczny klap 12V, uszczelki | Fizyczna ochrona drona przed deszczem i mrozem | 850 zł |
| -- | **SUMA (STACJA BAZOWA 230V)**| **Kompletna stacja dokująca ze stacją meteo i RTK** | **BOM Stacji (zasilanie sieciowe 230V)** | **~5 375 zł netto** |

---

### 4. Opcjonalny Moduł Zasilania Polowego (Off-Grid Solar Pack)

Dla stacji montowanych na odległych polach bez dostępu do sieci 230V:
* **Panel fotowoltaiczny monokrystaliczny (380W):** 420 zł
* **Regulator ładowania słonecznego MPPT (Victron SmartSolar 100/20):** 390 zł
* **Akumulator buforowy LiFePO4 12V 100Ah (1,28 kWh energii, ogniwa z matą grzewczą):** 1 150 zł
* **Maszt i okablowanie solarne:** 180 zł
* **Dopłata do wersji Off-Grid:** **+ 2 140 zł netto**.

---

### 5. Zestawienie Pakietów i Porównanie Rynkowe

```
+----------------------------------------------------------------------------------------------------+
|                                    ZESTAWIENIE PAKIETÓW I KOSZTÓW                                   |
+------------------------------------+--------------------+--------------------+---------------------+
| PAKIET                             | KOSZT CZĘŚCI (BOM) | SUGEROWANA CENA    | ODPOWIEDNIK RYNKOWY |
|                                    | (NETTO)            | SPRZEDAŻY (BRUTTO) | (CENA BRUTTO)       |
+------------------------------------+--------------------+--------------------+---------------------+
| 1. Dron "Agro-Sentinel 7"" Solo    | ~5 750 zł          | ~11 900 zł         | DJI Mavic 3T        |
|    (Manualny start z plecaka)      |                    |                    | (~27 000 zł)        |
+------------------------------------+--------------------+--------------------+---------------------+
| 2. Pełny System: Dron + Stacja     | ~11 130 zł         | ~23 900 zł         | DJI Dock 2 + M3TD   |
|    Dokująca 230V (Automatyczny)    |                    |                    | (~54 000 zł)        |
+------------------------------------+--------------------+--------------------+---------------------+
| 3. System Off-Grid Solar: Dron +   | ~13 270 zł         | ~27 900 zł         | Heisha / Percepto   |
|    Stacja Dokująca + Solary 380W   |                    |                    | (~80 000 - 120 000) |
+------------------------------------+--------------------+--------------------+---------------------+
```

---

### 6. Wnioski Biznesowe i Przewaga Konkurencyjna

1. **Ponad 50% taniej niż DJI Dock 2:**
   Kompletny zestaw autonomiczny ze stacją dokującą zamyka się w koszcie BOM **~11 100 zł netto**, co pozwala zaoferować rolnikowi gotowy produkt za **~24 000 zł brutto** (z marżą ponad 100% na montaż, wsparcie i oprogramowanie). DJI Dock 2 kosztuje obecnie ponad **50 000 – 55 000 zł**.
2. **Unikalna funkcja na rynku (Aktywne Płoszenie):**
   Żaden komercyjny dron (DJI, Autel, Parrot) nie posiada wbudowanego algorytmu automatycznego rozpoznawania dzików połączonego z kierunkową syreną 118 dB i stroboskopem LED. Drony konkurencji potrafią jedynie nagrać szkodnika, ale go nie odstraszą.
3. **Brak abonamentów chmurowych:**
   System DJI wymaga drogich licencji FlightHub. System Ursus bazuje na darmowym stacku open-source (ArduPilot + MAVLink + własna aplikacja webowa/desktopowa bez ukrytych opłat).

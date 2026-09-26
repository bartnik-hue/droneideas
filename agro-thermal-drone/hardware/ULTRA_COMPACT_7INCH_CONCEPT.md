# ULTRA-KOMPAKTOWY I NISKOBUDŻETOWY DRON AGRO (7-CALOWY ENDURANCE)
## Architektura oparta o kamery Caddx i technologie FPV Long-Range

---

### 1. Zmiana paradygmatu: Dron przemysłowy (5 kg) vs. Lekki Dron FPV Agro (1,2 kg)

Przejście na komponenty ze świata **Long-Range FPV** oraz matryce **Caddx Eclipse (Thermal)** pozwala:
1. **Zredukować koszt:** z ~25 000 – 35 000 PLN do zaledwie **~3 000 – 4 500 PLN** (redukcja o ~85%).
2. **Zredukować masę (AUW):** z 5,05 kg do **1,15 – 1,45 kg** (redukcja o ponad 70%).
3. **Zredukować gabaryty:** do rozmiaru 7-calowej ramy (mieści się w zwykłym plecaku turystycznym).
4. **Zachować długi czas lotu:** **35 – 45 minut** dzięki bateriom Li-Ion 6S 21700.

---

### 2. Kluczowy komponent: Kamery termowizyjne Caddx

Firma Caddx oferuje dedykowaną linię modułów termowizyjnych dla dronów – **Caddx Eclipse**:

* **Typ matrycy:** Niechłodzony mikrobolometr VOx (tlenek wanadu).
* **Masa modułu:** zaledwie **25 – 35 gramów** (wobec 500g przemysłowych głowic gimbalowych).
* **Warianty:**
  - *Caddx Eclipse 002 / 004SL:* 256×192 do 384×288 px (wersja ultra-tania, ok. 800 – 1 200 PLN).
  - *Caddx Eclipse 006 / 009:* 640×512 (z technologią Pixelpump AI) – idealna do detekcji z 50–70 m AGL (koszt ok. 1 500 – 1 900 PLN).
* **Wyjście wideo:** Podwójne – analogowe CVBS (PAL) o zerowym opóźnieniu oraz cyfrowe UVC (USB) do transmisji strumieniowej.
* **Integracja:** Możliwość montażu na mikro-gimbalu 1-osiowym (serwomechanizm mikro 9g sterowany z autopilota do zmiany kąta pochylenia tilt: dół/przód).

---

### 3. Sprytne cięcie kosztów i masy: AI przeniesione na ziemię (Ground Edge AI)

Zamiast dźwigać na dronie ciężki, prądożerny i drogi komputer pokładowy (NVIDIA Jetson za 1800 zł / 200g / 15W):
1. Dron przesyła strumień wideo z kamery Caddx przez cyfrowy link **Walksnail Avatar HD** (lub mocny link analogowy 5.8 GHz) do bazy na ziemi.
2. Na ziemi odbiornik wpięty jest do taniego laptopa, tabletu lub minikomputera z kartą graficzną / Raspberry Pi 5.
3. Model **YOLOv8-Thermal** analizuje obraz na ziemi w czasie rzeczywistym.
4. Po wykryciu dzika/zwierzęcia w granicach pola, stacja naziemna automatycznie wysyła do drona krótką komendę telemetryczną MAVLink (`DO_SET_SERVO / RELAY`), która natychmiast uruchamia pokładową syrenę i stroboskop!

---

### 4. Lekkie i głośne odstraszanie (Micro-Deterrence)

Zamiast 350-gramowego megafonu tubowego:
* **Przetwornik:** Podwójna syrena piezoelektryczna 12V (np. mini syrena alarmowa piezo o natężeniu **115 – 120 dB SPL @ 1m**).
* **Masa:** zaledwie **35 – 45 gramów**.
* **Pobór mocy:** 12V / 200 mA (poniżej 3W).
* **Stroboskop:** Dioda LED 10W (High-Power LED) z soczewką skupiającą (masa 8g).
* **Efekt:** Z wysokości 20–25 m nad kukurydzą dźwięk 118 dB piezo generuje na ziemi hałas ~90 dB o częstotliwości 2,8–3,5 kHz, który dla wrażliwego słuchu dzika jest skrajnie nieprzyjemny i zmusza go do ucieczki.

---

### 5. Specyfikacja i Kosztorys Zestawu (BOM ~3500 PLN)

| Element | Rekomendowany model | Waga | Orientacyjny koszt (PLN) |
| :--- | :--- | :---: | :---: |
| **Rama** | **7-calowa węglowa Long-Range** (np. GEPRC Crocodile 7 / Mark4 7") | 190 g | 220 zł |
| **Silniki** | **4x EMAX ECO II 2807 1300KV** lub BrotherHobby 2806.5 | 190 g | 360 zł |
| **Stack FC/ESC** | **SpeedyBee F405 V4 55A Stack** (z obsługą ArduPilot) | 45 g | 340 zł |
| **Nawigacja** | **Matek M10Q-5883 GNSS + Kompas** | 18 g | 140 zł |
| **Kamera Termo**| **Caddx Eclipse 640** (lub wersja 384) | 32 g | 1 550 zł |
| **Kamera dzienna**| Caddx Ratel 2 / Ant (do podglądu dziennego z przełącznikiem) | 12 g | 120 zł |
| **Transmisja VTX**| **Walksnail Avatar HD Mini 1S/V2** lub Analog 1.6W | 25 g | 450 zł |
| **Odstraszacz** | Mini syrena piezo 118 dB + stroboskop LED 10W + sterownik FET | 45 g | 45 zł |
| **Odbiornik RC** | **ExpressLRS 868/915 MHz** (zasięg >15 km) | 4 g | 80 zł |
| **Śmigła** | HQProp 7x4x3 lub Gemfan 7040 (2 komplety) | 35 g | 40 zł |
| **Bateria** | **Pakiet 6S2P Li-Ion (12x Molicel P45B, 9000 mAh)** | 880 g | 350 zł |
| **SUMA:** | **Gotowy dron do lotu z baterią i termowizją** | **~1 476 g** | **~3 700 zł** |

---

### 6. Czas lotu i osiągi wariantu 7-calowego

* **Masa całkowita do lotu (AUW):** **~1,47 kg**.
* **Pojemność baterii 6S2P Li-Ion:** 9,0 Ah przy 21,6V nominalnie = **194,4 Wh**.
* **Średni pobór mocy w locie patrolowym (prędkość 35–45 km/h):** ok. **260 – 280 W**.
* **Kalkulacja czasu lotu:**
  $$t = \frac{194,4\text{ Wh} \times 0,85\text{ (rezerwa)}}{270\text{ W}} \approx 0,61\text{ h} \approx \mathbf{36,7\text{ minut}}$$
* **Wariant lżejszy (pakiet 6S1P 4500 mAh, waga drona 1,03 kg):**
  - Czas lotu: **24–28 minut**.
  - Znakomita zwinność, ultra-niska masa.

# BILANS MASOWO-ENERGETYCZNY, DOBÓR NAPĘDU I BOM (BILL OF MATERIALS)
## Dron Rolniczy "Ursus Agro Sentinel" – Quadcopter 850 mm (Long Endurance)

---

### 1. Założenia Projektowe i Profil Misji

* **Cel operacyjny:** Autonomiczny oblot pól (Grid Survey), inspekcja termowizyjna w poszukiwaniu zwierzyny i szkodników, aktywne odstraszanie akustyczno-optyczne.
* **Wymagany czas lotu:** **40 – 45 minut realnego czasu misji** z pełnym obciążeniem (z rezerwą 15% na procedurę awaryjną RTL).
* **Odporność na wiatr:** Zdolność do stabilnego lotu przy wietrze ciągłym do 10 m/s (w porywach do 13–14 m/s).
* **Konstrukcja:** Składany quadcopter klasy 850 mm (ramiona składane parasolowo), transportowany w skrzyni transportowej Peli w bagażniku samochodu terenowego.

---

### 2. Budżet Masowy (Mass Budget Breakdown)

Całkowita masa startowa (MTOW / All-Up Weight) wynosi **~5,05 kg**.

```
+-------------------------------------------------------------+
|              MASA STARTOWA DRONA (AUW): 5050 g              |
+------------------------------+---------------+--------------+
|     1. PŁATOWIEC I AWIONIKA   |  2. PAYLOAD   |  3. BATERIA  |
|            1940 g            |    1250 g     |    1860 g    |
+------------------------------+---------------+--------------+
| • Rama węgiel 850mm : 820g   | • Gimbal Dual | • Pakiet     |
| • 4x Silnik BLDC    : 620g   |   Thermal+RGB |   Li-Ion     |
| • 4x ESC FOC 40A    : 140g   |   640: 520g   |   12S2P      |
| • 4x Śmigła 21"     : 160g   | • Megafon 120dB|  21700      |
| • Autopilot Cube+   :  75g   |   + Stroboskop|  Molicel P45B|
| • GNSS RTK + Lidar  :  85g   |   LED: 360g   |  (388.8 Wh)  |
| • PDB, kable, montaż:  40g   | • Jetson Orin |   1860g      |
|                              |   Nano AI:190g|              |
|                              | • Uchwyty:180g|              |
+------------------------------+---------------+--------------+
```

---

### 3. Obliczenia Aerodynamiczne i Energetyczne

#### 3.1. Zapotrzebowanie na Ciąg (Thrust Calculation)
* Masa całkowita do uniesienia: $m = 5050\text{ g}$.
* Ciąg wymagany do zawisu na 1 silnik:
  $$T_{hover} = \frac{5050\text{ g}}{4} = 1262,5\text{ g / silnik}$$
* Założony współczynnik ciągu do masy (Thrust-to-Weight Ratio - TWR): **2,5 : 1** (optymalny dla stabilności na silnym wietrze przy zachowaniu wysokiej sprawności energetycznej).
* Maksymalny ciąg zespołu napędowego:
  $$T_{max} = 5050\text{ g} \times 2,5 = 12\ 625\text{ g} \implies \sim 3150\text{ g / silnik}$$

#### 3.2. Sprawność Napędu i Zużycie Energii
* Dobór śmigieł: **21 × 7.0 cali** (składane włókno węglowe). Duża powierzchnia dysku zapewnia niskie obciążenie powierzchniowe ($T/A$), gwarantując wyjątkową sprawność w zawisie:
  $$\eta_{prop} \approx 12,0\text{ g/W przy ciągu } 1260\text{ g}$$
* Moc mechaniczna potrzebna do zawisu 4 silników:
  $$P_{mech} = \frac{5050\text{ g}}{12,0\text{ g/W}} \approx 420,8\text{ W}$$
* Pobór mocy przez elektronikę pokładową (Avionics & Payload):
  * Autopilot Cube Orange+, Here4 RTK, Lidar, telemetria: $12\text{ W}$
  * Komputer brzegowy NVIDIA Jetson Orin Nano (model YOLO 15W mode): $15\text{ W}$
  * Głowica Dual Thermal/RGB (stabilizacja gimbal + sensory): $10\text{ W}$
  * Suma elektroniki: $P_{elec} \approx 37\text{ W}$
* **Całkowita średnia moc pobierana w locie:**
  $$P_{total} = P_{mech} + P_{elec} = 420,8\text{ W} + 37\text{ W} \approx 458\text{ W}$$
  *(Podczas strzału megafonem pobór chwilowy wzrasta o 50W na okres 5–10 sekund, co ma pomijalny wpływ na ogólny bilans godzinny).*

#### 3.3. Dobór Baterii i Czas Lotu (Flight Time Calculation)
Tradycyjne pakiety LiPo mają zbyt małą gęstość grawimetryczną (~150 Wh/kg). Zastosowano pakiet zgrzewany z cylindrycznych ogniw **Li-Ion 21700 Molicel INR-21700-P45B** (gęstość ~230 Wh/kg).

* **Architektura pakietu:** **12S2P** (12 ogniw szeregowo, 2 równolegle = 24 ogniwa).
  * Wyższe napięcie 12S (43,2V nom. / 50,4V max) zamiast 6S zmniejsza o połowę prądy robocze ($I_{avg} \approx 10,6\text{ A}$), eliminując straty cieplne $I^2R$ na przewodach i regulatorach ESC.
* **Pojemność nominalna:** $2 \times 4500\text{ mAh} = 9000\text{ mAh}$ ($9,0\text{ Ah}$).
* **Pojemność energetyczna:**
  $$E_{nom} = 43,2\text{ V} \times 9,0\text{ Ah} = 388,8\text{ Wh}$$
* **Użyteczna energia (zostawiając 15% rezerwy bezpieczeństwa RTL):**
  $$E_{usable} = 388,8\text{ Wh} \times 0,85 = 330,5\text{ Wh}$$
* **Kalkulacja realnego czasu misji:**
  $$t_{flight} = \frac{E_{usable}}{P_{total}} = \frac{330,5\text{ Wh}}{458\text{ W}} = 0,7216\text{ h} \approx \mathbf{43,3\text{ minuty}}$$
* **Czas do rozładowania 100% (awaryjny):** $\frac{388,8}{458} = 0,848\text{ h} \approx \mathbf{50,9\text{ minut}}$.

---

### 4. Wymiary i Geometria Płatowca

```
                   Śmigło 21"              Śmigło 21"
                   (533 mm)                (533 mm)
                       \                      /
                     [ M1 ] ────────────── [ M2 ]
                       │  \                /  │
                       │    \   850 mm   /    │
                       │      \  (diag) /     │
                       │        \      /      │
                       │        [ KORPUS ]    │  Szerokość:
                       │        [ AI/BAT ]    │   600 mm
                       │        /      \      │
                       │      /          \    │
                       │    /              \  │
                       │  /                  \│
                     [ M4 ] ────────────── [ M3 ]
                       /                      \
                   Śmigło 21"              Śmigło 21"
```

* **Rozstaw silników po przekątnej (Wheelbase):** **850 mm**.
* **Odległość między sąsiednimi osiami silników:** $601\text{ mm}$.
* **Odstęp między końcami łopat śmigieł (Tip-to-Tip clearance):** $68\text{ mm}$ (zapewnia brak interferencji aerodynamicznych i cichą pracę).
* **Wymiary po złożeniu ramion (Transport):** **$480 \times 410 \times 360\text{ mm}$**.

---

### 5. Zestawienie Komponentów (Specyfikacja BOM)

| Lp. | Podsystem / Część | Rekomendowany Model / Specyfikacja | Rola i Uzasadnienie |
| :--- | :--- | :--- | :--- |
| **1** | **Rama (Airframe)** | Custom/Tarot T850 Folding Carbon 3K (rurki 25mm) | Sztywna, tłumiąca drgania, składana parasolowo do transportu. |
| **2** | **Silniki (4 szt.)** | **T-Motor MN5008 KV170** lub **T-Motor U8 Lite KV150** | Przemysłowe silniki o wysokiej sprawności zoptymalizowane pod zasilanie 12S i śmigła 21". |
| **3** | **Regulatory (4 szt.)**| **T-Motor Flame 45A 12S V2.0 (FOC)** | Wyciszona praca silników, telemetria CAN/RPM, odporność IP55. |
| **4** | **Śmigła (2 pary)** | **T-Motor FA21.0×7.0 Carbon Folding** | Składane łopaty z włókna węglowego; niski profil akustyczny. |
| **5** | **Autopilot (FC)** | **Cube Orange+ (STM32H757)** na płytce korekcyjnej | Potrójna redundancja IMU z amortyzacją, odporność na zakłócenia, obsługa ArduPilot. |
| **6** | **Nawigacja GNSS** | **Here4 GNSS RTK (u-blox F9P)** | Pozycjonowanie z dokładnością do 1,5 cm; obsługa GPS/Galileo/GLONASS/BeiDou. |
| **7** | **Lidar AGL** | **Benewake TF02-Pro (IP65, zasięg 40m)** | Precyzyjne śledzenie rzeźby terenu (Terrain Following) nad łanem uprawy. |
| **8** | **Komputer AI** | **NVIDIA Jetson Orin Nano Developer Kit (8GB)** | 40 TOPS mocy AI; detekcja obiektów YOLOv8 w 30 FPS na żywo. |
| **9** | **Głowica termowizyjna**| **Viewpro / Workswell WIRIS Agro** lub **Topotek Dual 640 LWIR + 4K Zoom** | Matryca niechłodzona 640×512, 13mm, NETD < 30mK + RGB 4K z 10x zoomem hybrydowym na 3-osiowym gimbalu. |
| **10**| **Megafon & Stroboskop**| **CZI MP130 V2 Digital Megaphone** + moduł 2x Cree XHP70 | 120–128 dB SPL, kompozytowa tuba, sterowanie cyfrowe przez UART. |
| **11**| **Bateria (Pakiet)** | **Custom 12S2P Molicel INR-21700-P45B (9Ah, 388Wh)** | Maksymalna gęstość energii 230 Wh/kg, prąd ciągły do 40A, złącze antyiskrowe AS150. |
| **12**| **Stacja Naziemna / Link**| **SIYI MK15 Enterprise** lub **Herelink v1.1 HD** | Zintegrowany kontroler z ekranem 5.5", zasięg transmisji wideo HD i C2 do 15 km. |

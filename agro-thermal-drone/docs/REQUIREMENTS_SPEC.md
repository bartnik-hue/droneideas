# SPECYFIKACJA SKŁADNIKÓW I ARCHITEKTURA SYSTEMU
## Podsystemy bezzałogowego drona rolniczego

System składa się z czterech zintegrowanych modułów:

```
+---------------------------------------------------------------+
|               AGRO-THERMAL-DRONE PLATFORM                     |
+---------------+---------------+---------------+---------------+
| 1. PŁATOWIEC  |  2. AWIONIKA  |  3. GŁOWICA   |  4. SYSTEM    |
|   I NAPĘD     |  NAWIGACYJNA  |   SENSOROWA   |  AI & GCS     |
+---------------+---------------+---------------+---------------+
| • Rama węgiel | • Autopilot   | • Kamera LWIR | • Onboard AI  | • Megafon     |
| • Silniki BLDC|   CubeOrange+ |   640x512     |   (Jetson /   |   120dB SPL   |
| • ESC FOC 6S  | • RTK GNSS    | • Kamera RGB  |    Hailo-8)   | • Stroboskop  |
| • Śmigła ciche| • Lidar AGL   |   4K Zoom     | • QGC Mission |   LED 5000lm  |
| • Li-Ion pack | • Łącze C2/Vid| • Gimbal 3D   | • Auto-Alert  | • Pętla decyzyjna
+---------------+---------------+---------------+---------------+---------------+
```

---

### Moduł 1: Płatowiec i Napęd (Airframe & Propulsion)
* **Układ ramy:** Składany quadcopter klasy 650–750 mm (ramiona z włókna węglowego 3K) dla łatwego transportu w bagażniku samochodu terenowego rolnika.
* **Silniki:** Bezszczotkowe (BLDC) o wysokiej sprawności (np. T-Motor U-Series lub MN-Series, KV 380–400).
* **Regulatory obrotów (ESC):** 40A–60A z kontrolą polową (FOC / telemetry CAN), cicha praca, wysoka efektywność energetyczna.
* **Śmigła:** Składane węglowe 16"–18", zoptymalizowane pod niski poziom hałasu (aby nie płoszyć zwierzyny z dużej odległości).
* **Zasilanie:** Pakiety akumulatorów Li-Ion 6S (np. 6S4P 21700 Molicel P45B, ~18 000 mAh) zapewniające do 40–50 minut realnego czasu lotu z ładunkiem użytecznym.

---

### Moduł 2: Awionika i Autonomia (Avionics & Flight Control)
* **Jednostka centralna (Flight Controller):** Ekosystem otwarty – **Cube Orange+ (STM32H7)** z potrójną redundancją IMU z izolacją wibracyjną lub **Holybro Pixhawk 6X**.
* **Oprogramowanie sterujące:** **ArduPilot (ArduCopter)** – najstabilniejszy na świecie system do automatycznych lotów po siatce polowej, odporny na awarie, obsługujący złożone geofencing i awaryjne lądowania (RTL - Return To Launch).
* **Nawigacja:** Podwójny odbiornik **GNSS RTK** (Here4 / Holybro H-RTK F9P) ze wsparciem GPS L1/L2, GLONASS, Galileo, BeiDou – dokładność pozycjonowania do 1–2 cm, kluczowa przy precyzyjnym nanoszeniu zniszczeń na mapy upraw.
* **Wysokościomierz pomocniczy:** Lidar laserowy (np. Benewake TF02-Pro / TFmini) do ścisłego utrzymywania stałej wysokości nad łanem kukurydzy/zboża (Terrain Following).
* **Łączność:** Radiolink cyfrowy dalekiego zasięgu (zasięg 8–15 km w pasmie 2.4 GHz / 5.8 GHz lub 868 MHz dla telemetrii C2).

---

### Moduł 3: Głowica Sensorowa (Optoelectronics Payload)
* **Gimbal:** 3-osiowy bezszczotkowy ze stabilizacją żyroskopową, enkoderami kątowymi i szybkim obrotem (pitch -90° do +30°, yaw 360° bez limitu lub w zakresie misji).
* **Sensor termowizyjny (LWIR):**
  * Typ: Niechłodzony mikrobolometr VOx.
  * Rozdzielczość: 640 × 512 px.
  * Pasmo: 8–14 µm.
  * NETD: $\le 30\text{ mK}$ przy f/1.0.
  * Optyka: 13 mm (szeroki kąt do szybkiego skanowania powierzchni pola).
  * Palety barwne: White Hot, Black Hot, Ironbow, Agro-HighContrast.
* **Sensor światła widzialnego (RGB):**
  * Matryca: 1/2" lub 1/1.7" CMOS, 48 MPx / 4K UHD.
  * Obiektyw: Hybrydowy zoom optyczny (min. 4x–10x) do zdalnego potwierdzenia, czy wykryty punkt cieplny to dzik, sarna, pies czy nagrzany głaz.
* **Dalmierz laserowy (LRF - opcjonalnie):** Pomiar odległości do celu (5–1200 m) pozwalający automatycznie obliczyć współrzędne GPS wykrytego zwierzęcia bez konieczności wiszenia bezpośrednio nad nim.

---

### Moduł 4: Przetwarzanie Obrazu i Stacja Naziemna (AI & GCS)
* **Przetwarzanie brzegowe (Edge AI):**
  * Moduł obliczeniowy na pokładzie drona (np. NVIDIA Jetson Orin Nano lub dedykowany koprocesor NPU Hailo-8).
  * Zadanie: Analiza strumienia termowizyjnego klatka po klatce w czasie rzeczywistym.
  * Model: **YOLOv8-Thermal / YOLOv11** wytrenowany na zbiorach danych dzikiej zwierzyny (dziki, sarny, jelenie, lisy, ludzie).
* **Interfejs stacji naziemnej (GCS):**
  * Tablet odporny na warunki polowe (IP65) z oprogramowaniem **QGroundControl / Mission Planner**.
  * Dynamiczne generowanie ścieżki koszenia/skanowania (Grid Survey) po zaznaczeniu granic działki rolniczej.
  * System powiadomień: Dźwiękowy alert w słuchawce operatora po wykryciu obiektu, automatyczne zapisanie punktu POI (Point of Interest) z koordynatami GPS na mapie.
  * Raport końcowy: Eksport pliku PDF / GeoJSON ze zliczoną populacją zwierząt na danym polu dla rolnika lub koła łowieckiego.

---

### Moduł 5: Aktywne Odstraszanie i Logika Decyzyjna (Active Deterrence & Threat Engine)
* **Głośnik kierunkowy / megafon:** 120–128 dB SPL @ 1 m, kompozytowa obudowa, masa $\le 350\text{ g}$.
* **Baza dźwięków:** Odgłosy sfory psów myśliwskich, syntetyczne wystrzały, modulowane syreny zniechęcające do adaptacji (anti-habituation).
* **Stroboskop nocny:** Diody wysokiej mocy (Cree XHP70, 5000 lm, 12–18 Hz).
* **Procedura taktyczna:** Autonomiczne zatrzymanie siatki (Pause), zniżenie do 25–30 m AGL, seria odstraszająca, weryfikacja opuszczenia uprawy i powrót do misji.
Pełna specyfikacja: [AUTONOMOUS_DETERRENCE_SYSTEM.md](file:///d:/URSUS/agro-thermal-drone/docs/AUTONOMOUS_DETERRENCE_SYSTEM.md).

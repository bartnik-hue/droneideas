# SPECYFIKACJA PODZESPOŁÓW STACJI BAZOWEJ (DRONE-IN-A-BOX)
## Autonomiczna Stacja Dokująca dla Drona "Ursus Agro-Sentinel 7""

---

### 1. Przegląd i Cel Operacyjny Stacji Bazowej
Stacja bazowa umożliwia pełną bezobsługowość drona na polach uprawnych. Dron stacjonuje w stacji, automatycznie startuje według harmonogramu nocnego (np. co 2 godziny między 21:00 a 04:00 rano), wykonuje zaplanowaną misję patrolową, powraca i ląduje z dokładnością do 1 cm, po czym automatycznie ładuje baterię i zrzuca zebrane dane (wideo 4K, raporty o szkodnikach).

Konstrukcja mechaniczna obudowy (kopuła/klapy) może być dowolna – poniższa specyfikacja skupia się na **niezbędnych podzespołach elektronicznych, nawigacyjnych, zasilających i sensorycznych**.

---

### 2. Architektura Podzespołów (Subsystemy Stacji)

```
+-----------------------------------------------------------------------------------+
|                        STACJA BAZOWA - ARCHITEKTURA SPRZĘTOWA                     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ 1. PRECYZYJNE NAPROWADZANIE ]       [ 2. POGODA I BEZPIECZEŃSTWO ]             |
|  • Baza GNSS RTK: u-blox ZED-F9P       • Ultradźwiękowy anemometr (wiatr)        |
|  • Antena Geodezyjna Multi-Band        • Optyczny czujnik opadów (deszcz/śnieg)   |
|  • Wizualny znacznik ArUco/AprilTag    • Czujnik temp./wilgotności (BME280)       |
|  • Aktywne podświetlenie IR 850nm                                                 |
|                                                                                   |
|  [ 3. SYSTEM ŁADOWANIA ]               [ 4. JEDNOSTKA ZARZĄDZAJĄCA (MÓZG) ]       |
|  • Płyta stykowa (Contact Pad / Pogo)  • Komputer SBC: Raspberry Pi 5 / CM4       |
|  • Mostek autodetekcji polaryzacji     • Oprogramowanie koordynatora misji        |
|  • Ładowarka CC-CV 6S (25.2V / 6-8A)   • Monitor stanu dokowania i baterii        |
|  • Przekaźnik izolacji styków (0V safe)                                           |
|                                                                                   |
|  [ 5. ŁĄCZNOŚĆ I TRANSFER DANYCH ]     [ 6. ZASILANIE STACJI (POWER) ]            |
|  • Wi-Fi 5 GHz (zrzut wideo 4K)        • Opcja 1: Zasilacz buforowy 230V AC       |
|  • Modem LTE 4G/5G (alerty rolnika)    • Opcja 2 (Off-Grid): Panel PV 300W        |
|  • Telemetria LoRa 868 MHz (MAVLink)     + Regulator MPPT + Bateria LiFePO4 100Ah |
+-----------------------------------------------------------------------------------+
```

---

### 3. Szczegółowy Wykaz Podzespołów (BOM Stacji)

#### 3.1. System Precyzyjnego Pozycjonowania i Lądowania (Precision Landing)
Standardowy GPS drona ma błąd 1,5–3,0 m, co uniemożliwia trafienie w małą płytę lądowiska stacji bazowej. Wymagany jest zestaw:
1. **Odbiornik bazowy GNSS RTK:**
   * **Model:** **u-blox ZED-F9P** (Multi-band L1/L2/E5b, RTK Base Station).
   * **Antena:** Zewnętrzna antena geodezyjna wieloczęstotliwościowa (GPS / Galileo / GLONASS / BeiDou) z płaszczyzną masy (Ground Plane).
   * **Rola:** Generuje strumień poprawek kinematycznych w czasie rzeczywistym (**RTCM 3.x**) i wysyła je do drona przez telemetrię/Wi-Fi. Zapewnia dokładność pozycjonowania drona rzędu **1–2 cm**.
2. **Optyczny Znacznik Centrowania (Visual Docking Target):**
   * **Płyta wizualna:** Druk ze wzorem **AprilTag (rodzina tag36h11)** lub **ArUco**, odporny na UV i warunki atmosferyczne.
   * **Podświetlenie nocne IR:** Diody podczerwieni **850 nm / 940 nm** zintegrowane w lądowisku. Umożliwiają dolnej kamerze/sensorowi drona wykrycie geometrycznego środka lądowiska w całkowitych ciemnościach z wysokości 5 m do 0 m bez widocznego światła.
3. **Czujnik Fizycznego Osiadania (Touchdown Sensor):**
   * Zestaw czujników nacisku (tensometry) lub mikroprzełączniki krańcowe pod płytą lądowiska. Natychmiast po dociśnięciu płóz stacja wysyła sygnał *DISARM* i załącza procedurę ładowania.

---

#### 3.2. Podzespoły Autonomicznego Ładowania Baterii (Contact Charging)
System nie wymaga skomplikowanego ramienia wymiany baterii; wykorzystuje wysokoprądowe styki dociskowe.
1. **Płyta Stykowa (Landing Contact Grid):**
   * Układ pierścieni współśrodkowych lub pasków mosiężnych pokrytych niklem/złotem (odporność na korozję polową).
   * Sprężynowe piny stykowe (High-current Pogo Pins) zamontowane na płozach podwozia drona.
2. **Moduł Automatycznego Dopasowania Polaryzacji (Auto-Polarity Rectifier):**
   * Układ oparty na mostku prostowniczym ze sterowanymi tranzystorami MOSFET (Ideal Diode Controller – np. na układach Linear/Analog Devices).
   * Pozwala dronowi usiąść pod dowolnym kątem obrotu (Yaw) – układ stacji sam rozpoznaje, na który styk trafił biegun dodatni, a na który ujemny.
3. **Inteligentny Moduł Ładowania CC-CV (Smart Fast Charger):**
   * Napięcie wyjściowe: **25,2 V DC** (dla pakietu 6S Li-Ion Molicel).
   * Prąd ładowania: **6,0 A – 8,0 A**.
   * Czas ładowania pakietu 9000 mAh od 15% do 85%: **ok. 50–60 minut**.
   * Cyfrowa komunikacja (CAN / I2C / UART) z BMS drona do monitorowania temperatury poszczególnych ogniw.
4. **Izolator Bezpieczeństwa (Safety Contactor / Relay):**
   * Domyślnie styki na płycie lądowiska są odłączone (napięcie **0,0 V**). Napięcie z ładowarki jest podawane dopiero po potwierdzeniu lądowania i identyfikacji drona. Zapobiega to zwarciom przez deszcz, śnieg, rosę, liście czy przypadkowe zwierzęta.

---

#### 3.3. Stacja Meteorologiczna i Czujniki Bezpieczeństwa Lotu
Dron nie może wystartować, a w trakcie lotu musi natychmiast wrócić (RTL), jeśli warunki atmosferyczne zagrażają bezpieczeństwu.
1. **Ultradźwiękowy Anemometr (Sonic Wind Sensor):**
   * Brak części ruchomych (odporny na zanieczyszczenia, zamarzanie, grad).
   * Dokładny pomiar prędkości wiatru ciągłego i porywów (limit operacyjny: wstrzymanie startu powyżej **10–12 m/s**).
2. **Optyczny Czujnik Opadowy (Optical Rain Sensor):**
   * Błyskawiczna detekcja kropel deszczu na powierzchni optycznej na podczerwień (dużo szybsza niż tradycyjne deszczomierze kubełkowe).
   * Wykrycie deszczu natychmiast wysyła komendę przerwania misji do drona.
3. **Cyfrowy Czujnik Środowiskowy (BME280 / SHT35):**
   * Monitorowanie temperatury powietrza, wilgotności względnej i ciśnienia barometrycznego (obliczanie punktu rosy w celu uniknięcia oblodzenia śmigieł w chłodne poranki).

---

#### 3.4. Jednostka Zarządzająca i Łączność (Station Brain & Comms)
1. **Komputer Przemysłowy / SBC (Edge Gateway):**
   * **Raspberry Pi 5 (4GB)** lub moduł przemysłowy **Compute Module 4 (CM4)** w przemysłowej obudowie na szynę DIN.
   * Uruchamia oprogramowanie zarządzające stanami stacji: *IDLE*, *METEO_CHECK*, *PRE_FLIGHT*, *MISSION_MONITOR*, *DOCKING*, *CHARGING*, *DATA_SYNC*.
2. **Modem Przemysłowy 4G LTE / 5G (np. Teltonika RUT241 lub modem na USB/mPCIe):**
   * Niezależne połączenie internetowe z zewnętrznymi antenami dookólnymi LTE.
   * Natychmiastowe przesyłanie alertów (detekcja watahy dzików) ze zdjęciami i współrzędnymi GPS na telefon rolnika (Telegram Bot / SMS / chmura).
   * Zdalny pulpit i zdalna diagnostyka stacji.
3. **Punkt Dostępowy Wi-Fi 5 GHz (802.11ac):**
   * Szybki transfer lokalny (High-Speed Data Offload). Po wylądowaniu w stacji dron automatycznie przerzuca nagrania wideo 4K i pliki telemetryczne na dysk SSD stacji bazowej w czasie krótszym niż 2 minuty.
4. **Radiomodem Telemetrii Dalekiego Zasięgu (LoRa 868 MHz / MAVLink):**
   * Nadajnik telemetryczny o mocy 500–1000 mW.
   * Ciągłe monitorowanie parametrów lotu drona (położenie, stan baterii, wysokość Lidar) w promieniu do 5–10 km niezależnie od zasięgu GSM.

---

#### 3.5. System Zasilania Stacji Bazowej (Power Architecture)
Dostępne są dwa warianty zasilania zależnie od miejsca montażu:

* **Wariant A (Stacjonarny – przy zabudowaniach rolniczych / zasilanie sieciowe):**
  * Zasilacz przemysłowy impulsowy **Mean Well 230V AC $\to$ 27V / 24V DC (350–500W)**.
  * Zasilacz buforowy UPS z małym akumulatorem AGM/LiFePO4 chroniący przed zanikami prądu w sieci wiejskiej.

* **Wariant B (Autonomiczny Off-Grid – montaż na skraju odległego pola):**
  * **Panel fotowoltaiczny (PV):** 1x lub 2x monokrystaliczny panel 200–350W montowany na maszcie.
  * **Kontroler ładowania słonecznego:** Regulator **MPPT 100/30 (np. Victron SmartSolar)** o wysokiej sprawności zimą i przy zachmurzeniu.
  * **Magazyn energii stacji:** Akumulator **LiFePO4 12V lub 24V o pojemności 100 Ah (1,2 – 2,4 kWh)** z wbudowanym systemem grzewczym ogniw do ładowania w temperaturach ujemnych. Taka pojemność wystarcza na całodobowe zasilanie elektroniki stacji oraz wykonanie **5–6 pełnych cykli naładowania drona** bez słońca.

---

### 4. Sekwencja Operacyjna Autonomicznej Misji

1. **Harmonogram:** Komputer stacji bazowej o wyznaczonej godzinie (np. 01:00 w nocy) uruchamia procedurę startu.
2. **Pre-Flight Weather Check:** Stacja meteo sprawdza porywy wiatru (<10 m/s), brak deszczu i temperaturę punktu rosy.
3. **RTK Fix & GPS Lock:** Baza u-blox ZED-F9P wysyła poprawki RTCM do drona. Autopilot drona melduje stan `RTK Fixed` (dokładność centymetrowa).
4. **Start:** Zasilanie styków ładowania jest wyłączone, dron startuje pionowo na pułap 40 m i odlatuje na trasę siatki patrolowej.
5. **Powrót i Podejście:** Po ukończeniu misji dron wraca po współrzędnych RTK dokładnie nad stację bazową.
6. **Precyzyjne Lądowanie (Optyczne + RTK):**
   * Na pułapie 5 m dron przełącza się na śledzenie podświetlonego znacznika **AprilTag IR**.
   * Dron ląduje centrycznie na płycie stykowej.
7. **Detekcja i Zabezpieczenie:** Sensory lądowiska potwierdzają osiadanie. Dron wyłącza silniki (*Disarm*).
8. **Cykl Po-Lotniczy:**
   * Połączenie Wi-Fi zrzuca zdjęcia termiczne i pliki 4K z kamery SIYI A8 mini na dysk stacji.
   * Układ załącza ładowarkę 25,2V 7A.
   * Modem LTE wysyła rolnikowi gotowy raport z nocnego patrolu.

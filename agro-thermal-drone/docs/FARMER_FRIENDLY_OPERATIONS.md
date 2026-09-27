# PROCEDURY PROSTEJ OBSŁUGI DLA ROLNIKA (PLUG-AND-PLAY AGRO OPERATIONS)
## Logistyka misji, autonomia startu, sygnalizacja GPS oraz twardy bilans energii

---

### 1. Filozofia "Zero Skomplikowania" (Farmer-Friendly Architecture)

Dron rolniczy nie może wymagać umiejętności pilotażu FPV ani obsługi skomplikowanego oprogramowania inżynieryjnego. Obsługa drona sprowadza się do 4 prostych kroków:

```
[ Krok 1: Wgranie misji ] ──> [ Krok 2: Ustawienie ] ──> [ Krok 3: Start ] ──> [ Krok 4: Raport ]
Kabel USB-C lub karta SD      W dowolnym miejscu поля     Jeden przycisk       Wyjęcie karty SD z
z gotowym plikiem misji       (droga, miedza, podwórko)   po zielonym LED      gotowym PDF i zdjęciami
```

---

### 2. Wgrywanie misji i pobieranie raportów bez internetu w polu

Rolnik w polu często nie ma stabilnego internetu ani chęci zabierania drogiego laptopa na deszcz.

#### 2.1. Metoda A: Karta Pamięci MicroSD (Plug & Fly)
1. Rolnik w domu w prostej aplikacji zaznacza pole i klika **"Zapisz na kartę SD"**.
2. Na karcie tworzy się czytelny plik `flight_mission.json` zawierający współrzędne trasy, pułap oraz parametry baterii.
3. Rolnik wkłada kartę do slotu w dronie. Po włączeniu zasilania autopilot automatycznie ładuje trasę do pamięci wewnętrznej.

#### 2.2. Metoda B: Szybki kabel USB-C / Mass Storage
* Podłączenie drona kablem USB-C do telefonu/tabletu/komputera powoduje wykrycie drona jako zwykłego pendrive'a (*Mass Storage*).
* Wgrywanie polega na skopiowaniu pliku lub kliknięciu jednego przycisku w aplikacji.

#### 2.3. Pamięć raportów i incydentów
* Na tej samej karcie MicroSD w dedykowanym folderze `/RAPORTY_SZKOD/` dron po każdym locie automatycznie generuje:
  - Gotowy plik **`RAPORT_2026-09-27_POLE_KUKURYDZA.pdf`** z mapą, statystykami i pieczęcią GPS.
  - Kolorowe zdjęcia wysokiej rozdzielczości z kamery RGB w podfolderze `/ZDJECIA_4K/` (oświetlone reflektorem dziki i zniszczone łany).
  - Plik wektorowy `szkody.geojson` do wgrania do systemów e-wniosek ARiMR lub dla rzeczoznawcy kół łowieckich.

---

### 3. Autonomia Startu i Tranzytu: "Start skąd chcesz"

Rolnik nie musi iść na początek wyznaczonej siatki. Może postawić drona na polnej drodze, masce samochodu lub przy bramie gospodarstwa:

1. **Dynamic Home Point:** Miejsce postawienia drona zostaje automatycznie zapisane jako punkt startowy i powrotu (*HOME*).
2. **Pionowy wznios bezpieczeństwa:** Dron pionowo wznosi się na zaprogramowaną bezpieczną wysokość tranzytową (np. **40 m AGL**), powyżej drzew, linii energetycznych i słupów.
3. **Autonomiczny dolot (Transit to Grid):** Dron leci po linii prostej na pułapie 40 m do pierwszego punktu siatki pola (Waypoint #1).
4. **Wykonanie misji:** Oblot siatki, patrol, weryfikacja i ewentualne odstraszanie.
5. **Powrót i lądowanie (Precision RTL):** Po zakończeniu ostatniego rzędu pola dron wraca na pułapie 40 m dokładnie w miejsce startu, zniża się i miękko ląduje.

---

### 4. Sprzętowa blokada startu GPS i Sygnalizacja Wizualna LED

Bezpieczeństwo jest kluczowe – dron **nie może wystartować**, dopóki nawigacja satelitarna nie gwarantuje centymetrowej stabilności (ochrona przed ucieczką drona / *fly-away*).

#### 4.1. Twarda blokada przed uzbrojeniem (Pre-Arm Safety Lock)
Silniki drona pozostają zablokowane fizycznie i programowo, dopóki system nie spełni rygorystycznych warunków:
* Liczba satelitów (GPS + Galileo + GLONASS): $\ge 16$.
* Wskaźnik precyzji HDOP: $\le 1,2$ (doskonała geometria satelitów).
* Status 3D Fix / RTK: **Locked**.
* Spójność kompasu i kalibracji IMU: **OK**.

#### 4.2. Wyraźny wskaźnik świetlny LED (Status Beacon)
Na grzbiecie lub ramionach drona zamontowane są mocne diody RGB, widoczne z odległości kilkudziesięciu metrów:

| Sygnał świetlny LED | Stan systemu | Działanie dla użytkownika |
| :--- | :--- | :--- |
| 🔴 **Czerwony pulsujący** | Szukanie satelitów / Brak gotowości | **START ZABLOKOWANY.** Czekaj ok. 30–60 sekund. |
| 🟡 **Żółty stały** | Łapanie FIX-a, kalibracja sensorów | System finalizuje procedury samotestu. |
| 🟢 **Zielony podwójny błysk** | **GPS LOCKED & MISJA ZAŁADOWANA** | **GOTOWY DO LOTU!** Można wcisnąć START. |
| 🔵 **Niebieski wolny puls** | Autonomiczny lot misyjny w toku | Dron wykonuje zadanie w powietrzu. |
| ⚪ **Biały stroboskop + Syrena** | Aktywna procedura odstraszania dzików | Dron zniżył się i wypłasza szkodnika. |

---

### 5. Inteligentny Kalkulator Baterii w Planerze (Zapas 15% RTL)

Aplikacja planera lotu **wymusza twardy bilans energii** przed wygenerowaniem misji:

$$D_{total} = D_{transit\_in} + D_{grid\_survey} + D_{transit\_out} + D_{reserve\_deterrence}$$

Gdzie:
* $D_{transit\_in}$: Odległość od miejsca startu (np. brama gospodarstwa) do narożnika pola.
* $D_{grid\_survey}$: Całkowita długość zygzaka nad polem.
* $D_{transit\_out}$: Droga powrotna z końca pola do punktu startu.
* $D_{reserve\_deterrence}$: Rezerwa energetyczna na 3–4 podejścia zniżające z oświetleniem LED i syreną.

#### Twarda reguła bezpieczeństwa:
$$\text{Szacowany czas całkowity } T_{total} \le 0,85 \times T_{max\_battery}$$

* **Dla baterii 6S2P (9000 mAh):** Maksymalny dopuszczalny czas misji z dojazdami wynosi **36 minut**.
* **Co jeśli pole jest za duże? (Smart Auto-Split):**  
  Jeśli rolnik zaznaczy pole o powierzchni 80 ha (które wymaga 55 minut lotu), planer **nie pozwoli na lot ryzykowny dla baterii**. Zamiast tego jednym kliknięciem dzieli pole na **Lot 1 (Sektor Północny)** oraz **Lot 2 (Sektor Południowy)** z przerwą na szybką wymianę pakietu.

# ARCHITEKTURA I MATEMATYKA SYSTEMU ROZPOZNAWANIA AI W DRONIE
## W jaki sposób dron autonomicznie przetwarza obraz i podejmuje decyzje?

---

### 1. Dwa podejścia do obliczeń AI: Gdzie fizycznie działa sieć neuronowa?

W zależności od wymagań budżetowych i operacyjnych stosuje się jedno z dwóch rozwiązań:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ WARIANT A: ONBOARD EDGE AI (Pełna autonomia na pokładzie drona)            │
│                                                                             │
│ [Kamera Caddx] ──(MIPI/USB)──> [Miniaturowy NPU] ──(UART)──> [ArduPilot]    │
│                                 (np. Luckfox / RK3588)        │             │
│                                 Model: YOLOv8-Nano (INT8)     ▼             │
│                                                          [Syrena 118dB]     │
│  Zaleta: Działa w 100% autonomicznie nawet po zerwaniu łączności z bazą.    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ WARIANT B: GROUND EDGE AI (Obliczenia na stacji naziemnej rolnika)          │
│                                                                             │
│ [Kamera Caddx] ──(Radio wideo)──> [Laptop / Tablet rolnika]                 │
│                                    (YOLOv8 na GPU / NPU bazy)               │
│                                              │                              │
│                                    Telemetria MAVLink (868 MHz)             │
│                                              ▼                              │
│                                    [Dron włącza syrenę]                     │
│  Zaleta: Dron jest ultra-lekki, tani i nie zużywa baterii na procesor AI.   │
└─────────────────────────────────────────────────────────────────────────────┘
```

Dla wersji komercyjnej **URSUS Agro Sentinel** optymalne jest wdrożenie hybrydowe: lekki akcelerator NPU na pokładzie (Wariant A) dla niezawodności, ze strumieniowaniem wyników na ekran rolnika (Wariant B).

---

### 2. Jak miniaturowy chip na pokładzie drona daje radę obliczać sieć AI?

Kluczem jest **kwantyzacja modelu (Quantization)**. Zamiast ciężkich bibliotek i liczb zmiennoprzecinkowych (FP32), sieć neuronowa zostaje zoptymalizowana do arytmetyki całkowitoliczbowej **INT8** (8-bitowej).

* **Hardware na pokładzie:**
  * Chip: **Rockchip RV1106 / RV1109** (na miniaturowej płytce o wymiarach zaledwie $3 \times 3\text{ cm}$ i wadze **9 gramów**; koszt: ~70–120 zł).
  * Zintegrowany akcelerator: **NPU (Neural Processing Unit) 0.5 – 1.2 TOPS**.
  * Pobór mocy: **poniżej 1,5 W** (znikomy wpływ na baterię drona!).
* **Wydajność:** 
  Model **YOLOv8-Nano INT8** przetwarza obraz termowizyjny o rozdzielczości $384 \times 288$ lub $640 \times 512$ z prędkością **25 – 35 klatek na sekundę (Real-Time FPS)**.

---

### 3. Algorytm rozpoznawania krok po kroku (Pipeline Przetwarzania)

```
[ Klatka termowizyjna z Caddx (VOx) ]
                 │
                 ▼
[ Krok 1: Normalizacja termiczna AGC ]
(Rozciągnięcie histogramu, wycięcie zimnego tła gleby)
                 │
                 ▼
[ Krok 2: Ekstrakcja plam cieplnych (Blobs) ]
(Szybki filtr progowy odcinający obiekty o T < 32°C)
                 │
                 ▼
[ Krok 3: Inferencja konwolucyjna YOLOv8-Nano ]
(Analiza kształtu, proporcji i sygnatury cieplnej)
                 │
                 ├──> [ Klasa: "Dzik" | Pewność: 94% ]
                 ├──> [ Pozycja na matrycy: (u, v) ]
                 │
                 ▼
[ Krok 4: Transformacja geometryczna (Piksel -> GPS) ]
(Korelacja z wysokościomierzem Lidar i IMU drona)
                 │
                 ▼
[ Krok 5: Silnik decyzyjny (Threat Engine) ]
(Sprawdzenie wieloboku uprawy -> Komenda MAVLink -> Syrena ON)
```

#### Krok 1 i 2: Fizyka obrazu termowizyjnego
Obraz z kamery Caddx w nocy to mapa temperatur. Grunt ma temperaturę otoczenia (np. $8^\circ\text{C}$), a ciało ssaka (dzik, sarna) to $38^\circ\text{C}$.  
Przed podaniem do sieci neuronowej algorytm AGC (*Automatic Gain Control*) normalizuje obraz tak, że ciepłe punkty tworzą silnie kontrastujące, jasne plamy na ciemnym tle.

#### Krok 3: Jak sieć neuronowa rozróżnia dzika od sarny czy krowy?
Sieć YOLO nie patrzy tylko na „temperaturę”, lecz na wyuczone wzorce geometryczne:
* **Dzik:** Krępa, niska sylwetka, zwarty obrys ciała, brak wyraźnej długiej szyi, często porusza się w zwartej grupie (wataha: locha + warchlaki).
* **Sarna / Jeleń:** Długie, cienkie kończyny (często chłodniejsze od tułowia), długa szyja, uniesiona głowa, charakterystyczna sylwetka.
* **Koźlę leżące:** Mały, owalny, statyczny punkt cieplny o regularnym kształcie bez wystających kończyn, ukryty w trawie bez ruchu translacyjnego.
* **Bydło / Konie:** Znacznie większa powierzchnia rzutu cieplnego, regularne odstępy na pastwisku.

#### Krok 4: W jaki sposób dron wylicza dokładne współrzędne GPS wykrytego zwierzęcia?
Dron nie musi lecieć idealnie nad zwierzęciem, by znać jego pozycję. Wykorzystywana jest **trygonometria rzutowania przestrzennego (Camera Ray-Casting)**:

1. Dron zna swoją pozycję z GPS RTK: $(X_{drone}, Y_{drone})$.
2. Dron zna dokładną wysokość nad gruntem z lidara laserowego: $H_{AGL}$.
3. Dron zna kąty przestrzenne kamery (kąt pochylenia kamery $\theta$, kurs kompasowy $\psi$, przechył $\phi$).
4. Jeśli obiekt znajduje się w punkcie $(u, v)$ matrycy kamery:
   $$\text{Kąt odchylenia promienia: } \alpha = \arctan\left(\frac{u - u_0}{f}\right)$$
   $$\text{Odległość naziemna do celu: } D = H_{AGL} \times \tan(\theta + \alpha)$$
5. Przeliczenie wektora odległości $D$ i azymutu na współrzędne geograficzne WGS-84 zajmuje ułamek milisekundy.

---

### 4. Co dzieje się w ułamku sekundy po wykryciu?

Gdy algorytm potwierdzi obecność dzika z pewnością $> 75\%$:
1. Moduł AI wysyła po wewnętrznym porcie szeregowym UART do ArduPilota komendę MAVLink:
   `MAV_CMD_DO_PAUSE_CONTINUE` (Dron zatrzymuje przelot i przechodzi w stabilny zawis).
2. Moduł AI wysyła sygnał logiczny HIGH na pin sterujący syreną piezo.
3. Syrena 118 dB i stroboskop LED emitują 5-sekundową serię odstraszającą.
4. Kamera śledzi, czy plama cieplna zmieniła pozycję i zmierza w kierunku granicy pola (ucieczka do lasu).
5. Gdy sektor jest czysty, syrena gaśnie, a dron wznawia automatyczną trasę misji.

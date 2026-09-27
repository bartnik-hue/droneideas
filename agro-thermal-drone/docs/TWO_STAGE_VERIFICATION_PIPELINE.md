# DWUETAPOWY SYSTEM DETEKCJI I WERYFIKACJI (THERMAL CUEING & OPTICAL INTERCEPT)
## Połączenie wstępnego wykrywania termowizyjnego z doświetleniem LED i kamerą RGB

---

### 1. Istota i Geniusz Rozwiązania

Zaproponowana przez Ciebie architektura rozwiązuje największy problem systemów wizyjnych w dronach rolniczych: **fałszywe alarmy (False Positives) i ograniczenia rozdzielczości termowizji**.

W klasycznych systemach próba rozpoznania gatunku z 40 metrów na małej matrycy termowizyjnej bywa zawodna (nagrzany głaz, kretowisko, sterta kompostu mogą wyglądać w termowizji jak leżący dzik lub sarna).

Dzięki zastosowaniu **dwuetapowego protokołu przechwycenia (Two-Stage Cueing & Intercept)**:
1. **Dron nie marnuje energii** na ciągłe świecenie reflektorem ani ciągłe analizowanie ciężkich modeli 4K.
2. **Termowizja działa jak radar wczesnego ostrzegania (Early Warning Radar)** z bezpiecznego, wysokiego pułapu.
3. **Kamera RGB + Reflektor LED działają jak precyzyjny identyfikator taktyczny (Tactical Identifier)**.

---

### 2. Przebieg Procedury Krok po Kroku

```
+─────────────────────────────────────────────────────────────────────────────+
| KROK 1: SZEROKI SKAN TERMICZNY (PASYWNY PATROL)                             |
| Pułap: 40–50 m AGL | Oświetlenie: WYŁĄCZONE (Ciemność) | Kamera: CADDX LWIR |
| • Dron cicho i szybko skanuje pole kukurydzy w podczerwieni.                |
| • Lekki algorytm wykrywa sygnaturę cieplną (>35°C).                         |
+─────────────────────────────────────────────────────────────────────────────+
                                       │
                                       ▼ Wykryto punkt cieplny!
+─────────────────────────────────────────────────────────────────────────────+
| KROK 2: DYNAMICZNE PODEJŚCIE I OŚWIETLENIE CELU (INTERCEPT & ILLUMINATE)    |
| Pułap: Zniżenie na 15–20 m AGL | Reflektor LED: WŁĄCZONY (Strumień 5000 lm)  |
| • Autopilot przerywa siatkę i zniża się dokładnie nad cel.                 |
| • Włącza się potężny dolny reflektor LED (tryb ciągły szperacza).           |
| • Aktywuje się kamera dzienna RGB wysokiej rozdzielczości (Sony Starvis 4K).|
+─────────────────────────────────────────────────────────────────────────────+
                                       │
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
| KROK 3: PRECYZYJNA KLASYFIKACJA AI W ŚWIETLE WIDZIALNYM                      |
| • Model YOLOv8 na obrazie RGB w pełnym świetle widzi fakturę, maść,         |
|   szczecinę dzika, cętki koźlęcia, rogi lub sylwetkę człowieka.             |
| • Pewność rozpoznania wzrasta z 70% do 99%. Wykluczenie nagrzanych kamieni. |
+─────────────────────────────────────────────────────────────────────────────+
                                       │
                     ┌─────────────────┴─────────────────┐
                     ▼                                   ▼
        [ POTWIERDZONY DZIK ]               [ POTWIERDZONE KOŹLĘ / FAWN ]
                     │                                   │
                     ▼                                   ▼
+──────────────────────────────────────+ +───────────────────────────────────+
| KROK 4A: TRYB ODSTRASZANIA           | | KROK 4B: TRYB OCHRONY FAUNY       |
| • LED przechodzi w STROBOSKOP (14 Hz)| | • Reflektor natychmiast GAŚNIE!   |
| • Włącza się syrena piezo 118 dB     | | • Bezwzględna cisza (zakaz syreny)|
| • Dzik ucieka do lasu                | | • Zapis dokładnego GPS dla kosiarza|
| • Powrót do patrolu na 45 m AGL      | | • Powrót do patrolu na 45 m AGL   |
+──────────────────────────────────────+ +───────────────────────────────────+
```

---

### 3. Synergia Sprzętowa: Ten sam komponent, dwie role

Największą zaletą tej koncepcji jest to, że **nie dodajemy do drona ani jednego grama nowej wagi**:
* **Dolny moduł LED (np. 2x Cree XHP70 / 5000 lumenów):**
  1. **Rola 1 (Weryfikacja):** Świeci światłem ciągłym przez 2–3 sekundy, zamieniając noc w dzień na powierzchni ok. $15 \times 15\text{ m}$, aby kamera RGB miała idealne warunki ekspozycji.
  2. **Rola 2 (Odstraszanie):** Jeśli cel to szkodnik, ten sam LED natychmiast przełącza się w tryb stroboskopu o częstotliwości 14 Hz, potęgując efekt paniki u dzików.
* **Podwójny tor kamerowy:**
  * Kamera 1: **Caddx Eclipse (Thermal)** – pracuje stale w locie patrolowym (pobór ~1,2 W).
  * Kamera 2: **Kamera RGB HD (Sony Starvis 4K / Caddx)** – włącza się lub pobiera klatkę wysokiej rozdzielczości tylko w momencie podejścia do celu.

---

### 4. Kluczowe Korzyści Inżynieryjne i Biznesowe

1. **Eliminacja fałszywych alarmów (Zero False Positives):**
   * Nagrzany w dzień kamień lub kretowisko w świetle LED natychmiast okazuje się martwym obiektem – dron nie wszczyna fałszywego alarmu, gasi światło i leci dalej.
2. **Oszczędność baterii:**
   * Silny reflektor 5000 lm pobiera ok. 30W. Gdyby świecił stale, skróciłby czas lotu o połowę. Włączany impulsowo na 3 sekundy do weryfikacji zużywa pomijalną ilość energii (<0,1% baterii).
3. **Niezbity materiał dowodowy dla kół łowieckich i ubezpieczycieli:**
   * Raport PDF zawiera nie tylko niewyraźną plamę z termowizji, ale **kolorowe, ostre zdjęcie oświetlonego dzika lub zniszczonego łanu kukurydzy w jakości 4K z pieczęcią GPS**.

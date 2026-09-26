# OPROGRAMOWANIE STACJI NAZIEMNEJ I ZARZĄDZANIA: "URSUS AGRO-PILOT"
## Dedykowany, autorski system planowania misji i zarządzania pracą drona

---

### 1. Dlaczego własne oprogramowanie (GCS) to klucz do sukcesu?

Standardowe programy (Mission Planner, QGroundControl) zostały stworzone dla inżynierów i hobbystów. Posiadają setki skomplikowanych zakładek, suwaków i parametrów technicznych, które **odstraszają rolników i myśliwych**.

Twój klient (rolnik, agronom, prezes koła łowieckiego) potrzebuje aplikacji o filozofii działania zbliżonej do Ubera czy kosiarki autonomicznej:
1. **Widzi swoje działki** na mapie satelitarnej (import z Geoportalu / ARiMR).
2. **Wybiera tryb pracy:**
   * 🐗 *Patrol Anty-Dzik (Nocny oblot z aktywnym wypłaszaniem)*
   * 🦌 *Ratowanie Koźląt (Przed koszeniem łąki, cichy geolog)*
   * 🌾 *Szacowanie Szkód (Ortomapa i obliczanie zniszczonych hektarów)*
3. **Wciska jeden przycisk: [START PATROLU]**.
4. Dron sam generuje optymalną siatkę lotu, startuje, patroluje, wykrywa zwierzynę, w razie potrzeby ją wypłasza, wraca i ląduje.
5. Aplikacja generuje gotowy **Raport PDF z pieczątką i mapą GPS** dla ubezpieczyciela lub koła łowieckiego.

---

### 2. Architektura Systemu "Ursus Agro-Pilot"

Aplikacja oparta jest na nowoczesnym, modularnym stosie technologicznym:

```
+--------------------------------------------------------------------------+
|                     INTERFEJS UŻYTKOWNIKA (TABLET / WEB)                  |
|  • Intuicyjna mapa pól (MapLibre / Leaflet + warstwy Geoportal / ARiMR)  |
|  • Podgląd na żywo z kamery termowizyjnej Caddx (RTSP / WebRTC)          |
|  • Wyświetlanie ramek detekcji AI: "Dzik (94%)", "Sarna (89%)"           |
|  • Przycisk awaryjny RTL (Return to Launch) i ręczne wyzwolenie syreny   |
+--------------------------------------------------------------------------+
                                    ▲
                                    │ WebSocket / REST API
                                    ▼
+--------------------------------------------------------------------------+
|                     BACKEND I LOGIKA BIZNESOWA (PYTHON)                  |
|                                                                          |
|  1. Grid Generator: Algorytm planowania siatki koszenia wieloboków       |
|  2. MAVLink Bridge: Dwukierunkowa telemetria i upload misji (pymavlink)  |
|  3. AI Inference Worker: Analiza strumienia wideo (YOLOv8-Thermal)       |
|  4. Threat Engine: Ocena strefy, decyzje o odstraszaniu i komendy serwa  |
|  5. PDF Reporter: Automatyczne generowanie protokołów szkód             |
+--------------------------------------------------------------------------+
                                    ▲
                                    │ Łącze radiowe (USB / UDP / Telemetry)
                                    ▼
+--------------------------------------------------------------------------+
|                        DRON (ARDUPILOT / CADDX)                          |
+--------------------------------------------------------------------------+
```

---

### 3. Kluczowe Moduły Własnego Oprogramowania

#### Moduł A: Algorytm Generowania Siatki Lotu (Boustrophedon Grid Planner)
Rolnik klika na mapie rogi swojego pola (lub wczytuje numer działki z bazy ewidencji gruntów). Algorytm:
* Oblicza optymalny kąt lotu wzdłuż najdłuższego boku pola (minimalizacja liczby nawrotów i oszczędność baterii).
* Na podstawie kąta widzenia kamery Caddx Eclipse (FOV) i wybranej wysokości (np. 40 m) wylicza szerokość ścieżki i niezbędną zakładkę (overlap 20–30%).
* Automatycznie generuje punkty nawigacyjne (Waypoints) ze zdefiniowaną prędkością i poleceniami zatrzymania w razie detekcji.

#### Moduł B: MAVLink Bridge (Sterowanie Autopilotem)
* Wgrywa wygenerowaną trasę do pamięci drona w standardzie MAVLink `MISSION_ITEM_INT`.
* Monitoruje stan baterii, sygnał GPS i wysokość AGL z lidaru.
* W razie zagrożenia (np. nagła wataha dzików) wysyła komendę zatrzymania misji (`MAV_CMD_DO_PAUSE_CONTINUE`), nakazuje zniżenie i aktywuje syrenę piezo.

#### Moduł C: Moduł Raportowania Szkód Łowieckich
* Po zakończonym locie aplikacja zlicza:
  - Zlokalizowane zwierzęta z podziałem na gatunki,
  - Dokładne współrzędne GPS każdego incydentu,
  - Szacunkową powierzchnię wygniecionej uprawy (m² / ha).
* Jednym kliknięciem eksportuje dokument PDF zawierający zdjęcia termowizyjne, mapę z pinezkami i datownik, gotowy do złożenia wniosku odszkodowawczego.

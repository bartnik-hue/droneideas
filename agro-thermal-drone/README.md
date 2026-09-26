# AGRO-THERMAL-DRONE (Ursus Agro Sentinel)
## Autonomiczny bezzałogowy system monitoringu pól i detekcji szkodników

### 1. Cel projektu
Projekt dedykowany dla nowoczesnego rolnictwa precyzyjnego oraz kół łowieckich. Głównym zadaniem platformy jest autonomiczny oblot upraw rolnych według zaprogramowanej siatki lotu oraz automatyczna detekcja obecności dzikich zwierząt i szkodników (dziki, sarny, jelenie) za pomocą podwójnego sensora:
* **Sensora termowizyjnego (LWIR)** – wykrywanie sygnatury cieplnej zwierząt ukrytych w wysokich uprawach (kukurydza, rzepak, zboża, łąki).
* **Sensora światła widzialnego (RGB z zoomem)** – wizualna weryfikacja i identyfikacja gatunku w warunkach dziennych.

---

### 2. Kluczowe zastosowania
1. **Ochrona upraw przed szkodami łowieckimi:**
   - Nocne i poranne patrole pól kukurydzy i zbóż.
   - Wczesne wykrywanie żerujących watah dzików zanim wyrządzą zniszczenia.
   - Możliwość integracji z sygnalizatorami odstraszającymi (akustyczne/świetlne).
2. **Ochrona fauny przed pracami polnymi (Fawn Rescue):**
   - Przeszukiwanie łąk przed pierwszym i drugim pokosem traw w celu ratowania młodych koźląt saren i ptaków lęgowych przed kosiarkami.
3. **Dokumentacja i szacowanie szkód łowieckich:**
   - Georeferencyjna mapa zniszczeń i obecności zwierzyny dla kół łowieckich, rolników i ubezpieczycieli.
4. **Agro-diagnostyka (wartość dodana):**
   - Ocena stresu wodnego roślin (anomalie termiczne aparatu szparkowego).
   - Inspekcja instalacji melioracyjnych i nawadniających.

---

### 3. Architektura projektu w repozytorium

```
agro-thermal-drone/
├── docs/                     # Dokumentacja koncepcyjna, analizy i normy prawne
│   ├── FEASIBILITY_STUDY.md  # Ocena zasadności (biznesowa, techniczna, prawna)
│   ├── REQUIREMENTS_SPEC.md  # Specyfikacja wymagań technicznych i operacyjnych
│   └── REGULATORY_BVLOS.md   # Wymogi EASA / ULC (kategoria Specific, STS-02, Dual-Use)
├── hardware/                 # Specyfikacja i dobór podzespołów fizycznych
│   ├── airframe/             # Konstrukcja ramy, aerodynamika, dobór napędu
│   ├── payload/              # Zespół kamer: termowizja + RGB + gimbal
│   ├── avionics/             # Autopilot (PX4/ArduPilot), GNSS RTK, zasilanie
│   └── datalink/             # Radiolinia C2, transmisja wideo HD, telemetria
├── software/                 # Moduły oprogramowania i algorytmy
│   ├── mission-planner/      # Generowanie siatek lotu i planowanie misji
│   ├── thermal-cv-pipeline/  # Detekcja AI/YOLO sygnatur cieplnych zwierzyny
│   └── gcs-interface/        # Integracja ze stacją naziemną (Ground Control Station)
└── README.md                 # Główny opis projektu
```

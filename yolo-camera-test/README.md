# Szybki start: Detekcja YOLO na żywo (PS Eye + OBS Virtual Camera)

Projekt umożliwia uruchomienie najnowocześniejszych modeli detekcji obiektów **YOLO (YOLOv8 / YOLO11)** w czasie rzeczywistym z akceleracją sprzętową **NVIDIA CUDA (GeForce RTX 4070 Ti)** przy wykorzystaniu kamerki **Sony PlayStation Eye (PS Eye)** za pośrednictwem **OBS Virtual Camera**.

---

## Dlaczego OBS nie widział PS Eye?
Sterownik Open Driver z OpenTrack zastępuje klasyczny interfejs DirectShow niskopoziomowym sterownikiem **`libusb / libusbK`**.
Programy takie jak OBS Studio, Skype czy aplikacja Aparat Windows szukają urządzeń DirectShow/MediaFoundation, dlatego w ogóle nie widzą PS Eye w tej konfiguracji.

## Jak rozwiązaliśmy ten problem?
Nasz skrypt łączy się z kamerką PS Eye **bezpośrednio przez bibliotekę `libusb` (pseyepy)** na poziomie sprzętowym:
1. **Wejście:** Bezpośredni odczyt z **PS Eye przez sterownik open-driver (libusb)** z pełną prędkością **60 FPS** (bez żadnych zewnętrznych programów!).
2. **AI:** Inferencja **YOLO (YOLO11 / YOLOv8)** z akceleracją sprzętową **NVIDIA CUDA (RTX 4070 Ti)** w czasie ~6 ms.
3. **Wyjście podglądu:** Płynne okno na pulpicie z naniesionymi ramkami detekcji, nazwami obiektów i licznikiem FPS.
4. **Wirtualna Kamera:** Równoległe nadawanie przetworzonego obrazu AI do **OBS Virtual Camera**! Dzięki temu inne programy (np. Discord, OBS Studio jako źródło kamery wirtualnej) mogą widzieć gotowy obraz z detekcjami YOLO!

---

## Jak uruchomić?

W folderze `d:\URSUS\yolo-camera-test\` po prostu kliknij dwukrotnie:
👉 **`URUCHOM_DETEKCJE.bat`**

*(Lub w konsoli: `.\.venv\Scripts\python.exe detect_yolo.py`)*

Skrypt automatycznie:
- Wykryje kartę **NVIDIA GeForce RTX 4070 Ti**,
- Pobierze i załaduje model **YOLO11n / YOLOv8n**,
- Połączy się ze strumieniem wirtualnej kamery,
- Otworzy płynne okno podglądu z nakładanymi ramkami detekcji, nazwami obiektów i licznikiem FPS.

---

## Sterowanie w oknie podglądu

| Klawisz | Akcja |
| :--- | :--- |
| **`q`** lub **`ESC`** | Zakończenie pracy programu i zwolnienie kamery |
| **`s`** | Zapisanie klatki z detekcjami do folderu `snapshots/` |
| **`+`** / **`-`** | Zwiększenie / zmniejszenie progu pewności wykrywania (*confidence threshold*) |
| **`c`** | Przełączenie na kolejną kamerę (jeśli w systemie jest kilka urządzeń) |

---

## Diagnostyka kamer
Jeśli obraz nie pojawia się w oknie:
1. Uruchom plik **`SPRAWDZ_KAMERY.bat`** – przeskanuje on system i wskaże indeksy wszystkich aktywnych kamer.
2. Upewnij się, że w OBS Studio przycisk kamery wirtualnej jest aktywny (podświetlony na niebiesko / z napisem "Zatrzymaj kamerę wirtualną").

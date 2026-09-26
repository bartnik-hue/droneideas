# Drone Ideas & Open UAV Concepts Repository

> **Repository:** [https://github.com/bartnik-hue/droneideas](https://github.com/bartnik-hue/droneideas)  
> **Interactive Catalog:** [Open `index.html`](index.html) (lub przez GitHub Pages: `https://bartnik-hue.github.io/droneideas/`)

---

## 📖 O Repozytorium

To repozytorium gromadzi **otwarte koncepcje inżynieryjne, specyfikacje sprzętowe oraz oprogramowanie dla wyspecjalizowanych bezzałogowych statków powietrznych (UAV)** dla rolnictwa, ochrony środowiska i inspekcji technicznych.

Wszystkie karty projektowe posiadają **pełne wielojęzyczne tłumaczenia** (Polski, English, Українська, Русский) z wygodnym przełącznikiem języka.

---

## 🗂️ Spis Projektów w Bazie

### 1. [Ursus Agro-Sentinel 7" Thermal](projects/agro-sentinel-7.html) (PROJECT #001)
* **Status:** Specyfikacja gotowa do prototypowania
* **Przeznaczenie:** Autonomiczny nocny i poranny monitoring pól kukurydzy, rzepaku i zbóż; aktywne wypłaszanie dzików i ochrona koźląt saren przed kosiarkami.
* **Kluczowa technologia:**
  * Kompaktowa rama 7" Long-Range (masa 1,47 kg, czas lotu ~37 minut na pakiecie Li-Ion 6S2P),
  * Kamera termowizyjna **Caddx Eclipse VOx**,
  * Pokładowy procesor neuronowy **Rockchip NPU (9g)** z modelem **YOLOv8-Nano INT8**,
  * Podwójna syrena piezoelektryczna **118 dB SPL @ 1m** + stroboskop nocny LED 10W,
  * Koszt podzespołów BOM: zaledwie **~3 700 PLN** (wobec 25 000+ PLN za DJI M3T).
* **Pliki techniczne:**
  * 🌐 [Interaktywna Karta Projektu HTML](projects/agro-sentinel-7.html)
  * 📄 [Karta Produktu Markdown](agro-thermal-drone/docs/PRODUCT_DATA_SHEET.md)
  * 📊 [Bilans Masowo-Energetyczny i BOM](agro-thermal-drone/hardware/SIZING_AND_COMPONENTS_BOM.md)
  * 💡 [Koncepcja Ultra-Kompaktowa 7" Caddx](agro-thermal-drone/hardware/ULTRA_COMPACT_7INCH_CONCEPT.md)
  * 🧠 [Architektura Obliczeniowa AI na Pokładzie](agro-thermal-drone/software/AI_INFERENCE_ARCHITECTURE.md)
  * 💻 [Kod Autorskiego Generatora Misji i Silnika Decyzyjnego](agro-thermal-drone/software/gcs-app/)

---

## 🌐 Przeglądanie w przeglądarce

Aby uruchomić katalog lokalnie:
1. Otwórz plik `index.html` w dowolnej przeglądarce internetowej.
2. Wybierz preferowany język w prawym górnym rogu (🇵🇱 PL | 🇬🇧 EN | 🇺🇦 UK | 🇷🇺 RU).

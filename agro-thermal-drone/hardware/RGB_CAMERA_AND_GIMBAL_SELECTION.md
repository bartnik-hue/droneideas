# DOBÓR KAMERY KOLOROWEJ RGB, GIMBALA I ARCHITEKTURY NAGRYWANIA
## Analiza rynkowa, kąty widzenia dla AI oraz weryfikacja modułów nagrywania

---

### 1. Sprawdzenie kwestii nagrywania przy kamerze analogowej: Czy potrzebny jest moduł?

**TAK, MASZ 100% RACJI.**

Tradycyjna analogowa kamera FPV (np. Caddx Ratel, Foxeer Toothless, RunCam Phoenix):
1. **Wysyła wyłącznie sygnał telewizyjny w czasie rzeczywistym (CVBS / PAL / NTSC)** przez jeden przewód sygnałowy.
2. **NIE POSIADA:**
   * Własnego procesora kodowania wideo (brak kodeka H.264 / H.265),
   * Pamięci podręcznej ani gniazda na kartę pamięci MicroSD.
3. **Konsekwencje próby nagrywania:**
   * Aby nagrać obraz z kamery analogowej na pokładzie drona, **bezwzględnie trzeba dołożyć zewnętrzny moduł rejestratora DVR** (np. *RunCam Mini DVR* lub *Foxeer DVR Board*).
   * **Problem jakościowy:** Nagranie z analogowego DVR jest ograniczone do rozdzielczości telewizyjnej PAL ($720 \times 576$ pikseli). Zawiera szumy, zniekształcenia przetwornika analogowo-cyfrowego i kompresję MJPEG. **Z takiego nagrania nie da się uzyskać ostrego, czytelnego zdjęcia dowodowego w raporcie PDF dla rolnika!**

> **Wniosek inżynieryjny:** Kamera dzienna RGB musi posiadać **wbudowany koder sprzętowy i własny slot MicroSD na pokładzie**, nagrywając w natywnej jakości **4K / 2K** bezpośrednio na kartę w dronie, jednocześnie wyprowadzając sygnał wideo (HDMI / Ethernet / CVBS) do transmisji na ziemię i dla procesora NPU AI.

---

### 2. Dlaczego gimbal i widok pod kątem (30°–60°) są kluczowe dla AI?

Kamera zamontowana na sztywno, patrząca tylko pionowo w dół (*top-down*):
* Widzi zwierzę wyłącznie od strony grzbietu. Z góry dzik, duży pies, leżąca sarna czy zwinięty w kłębek borsuk wyglądają niemal identycznie (jako owalny ciemny/jasny kształt).

Kamera na gimbalu z możliwością pochylenia (*Tilt* $30^\circ - 60^\circ$):
1. **Rozpoznanie anatomiczne sylwetki:** Model AI (YOLO) widzi profil boczny:
   * Kształt pyska dzika (*gwizd*), postawione uszy (*słuchy*), krępe nogi (*biegi*).
   * Długie, szczudłowate nogi sarny, białe lustro pod ogonem, rogi jelenia.
2. **Śledzenie ucieczki (Tracking):** Gdy po włączeniu reflektora i syreny zwierzęta zaczynają uciekać, gimbal może śledzić watahę w kierunku ściany lasu bez konieczności gwałtownego przechylania całego drona.
3. **Elastyczność kątowa:** Gimbal pozwala patrzeć zarówno pionowo w dół (do precyzyjnego pozycjonowania GPS leżącego koźlęcia przed kosiarką), jak i w przód/pod kątem (do taktycznego odstraszania watah dzików).

---

### 3. Zestawienie kamer na rynku pasujących do drona 7" (Masa < 150g)

Przeanalizowano rynek pod kątem: masy, matrycy nocnej (Starlight), zoomu, wbudowanego slotu MicroSD 4K oraz kompatybilności z ArduPilotem:

| Model kamery i producent | Typ sensora i rozdzielczość | Zoom | Typ gimbala i kąty | Masa | Zapis MicroSD | Cena szacunkowa | Ocena do projektu URSUS |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **SIYI A8 mini** *(FAWORYT)* | **1/1.7" Sony Starlight CMOS**, 8 MPx, 4K @ 25fps / 2K @ 30fps | **6X cyfrowy / bezstratny** | **Zintegrowany 3-osiowy bezszczotkowy** (Pitch -135° do +45°, Yaw ±160°) | **95 g** | **TAK (Slot MicroSD 4K/2K)** | **~1 150 – 1 350 PLN** | ⭐⭐⭐⭐⭐ **IDEALNY DO PROJEKTU.** Gotowy moduł z 3-osiowym gimbalem, czujnikiem nocnym Sony, wagą poniżej 100g i sterowaniem MAVLink z ArduPilota. |
| **Caddx Walksnail Moonlight 4K** | **1/1.8" Sony Starlight**, 4K @ 60fps (EIS Gyroflow) | Brak (szeroki kąt) | Wymaga montażu na mikro-gimbalu serwo 1-osiowym (Tilt) | **38 g** (+35g gimbal = **~73 g**) | **TAK (Slot MicroSD 4K 60fps)** | **~850 PLN** (+120 zł gimbal) | ⭐⭐⭐⭐ **BARDZO DOBRY.** Super lekki, świetna czułość w nocy w świetle LED, ale wymaga budowy własnego zawieszenia serwo (tylko oś góra-dół). |
| **RunCam Split 4K V2** | 1/2" Sony CMOS, 4K @ 30fps / 1080p @ 60fps | Brak | Wymaga montażu na mikro-gimbalu serwo 1-osiowym (Tilt) | **22 g** (+35g gimbal = **~57 g**) | **TAK (Slot MicroSD 4K)** | **~450 PLN** (+120 zł gimbal) | ⭐⭐⭐ **BUDŻETOWY.** Tani i bardzo lekki, ale gorsza czułość nocna niż matryce 1/1.7" Sony Starlight w Caddx/SIYI. |
| **SIYI ZR10** | 1/2.8" Sony CMOS, 2K / 4K | **30X (10X optyczny + 3X cyfrowy)** | Zintegrowany 3-osiowy bezszczotkowy | **380 g** | **TAK (MicroSD)** | **~2 400 PLN** | ❌ **ZA CIĘŻKI.** 380 g zabiłoby czas lotu i zwrotność drona 7-calowego (dedykowany do platform 12–15 cali). |

---

### 4. Rekomendacja Sprzętowa: Wybór SIYI A8 mini

**SIYI A8 mini to bezkonkurencyjny lider do naszej specyfikacji:**

1. **Waga zaledwie 95 gramów:** Zintegrowana kamera 4K ze stabilizowanym, bezszczotkowym gimbalem 3-osiowym waży mniej niż mała tabliczka czekolady!
2. **Matryca 1/1.7" Sony Starlight:** W połączeniu z naszym dolnym reflektorem LED 5000 lm daje w nocy obraz o jakości telewizyjnej – widać pojedyncze kępki sierści zwierzęcia.
3. **Zoom 6X:** Dron nie musi zniżać się na 5 metrów nad dziki (co mogłoby skończyć się atakiem lub spłoszeniem w niekontrolowanym kierunku). Może zawisnąć na bezpiecznych 20 metrach i przybliżyć obraz 6-krotnie.
4. **Pełna kontrola kąta (Pitch -135° do +45°):** 
   - W locie patrolowym: patrzy w dół pod kątem $45^\circ$, skanując pole przed dronem.
   - W trybie weryfikacji: autopilot automatycznie nakierowuje kamerę wprost na koordynaty GPS celu.
5. **Autonomiczne nagrywanie na kartę MicroSD:**
   - Rolnik po wylądowaniu wyjmuje kartę z kamery (lub podłącza kabel) i ma krystalicznie czyste nagrania 4K i zdjęcia bez jakichkolwiek zakłóceń radiowych.

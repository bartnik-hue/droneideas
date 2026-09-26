# OCENA ZASADNOŚCI PROJEKTU (FEASIBILITY STUDY)
## Dron Rolniczy z Kamerą Termowizyjną i RGB do Detekcji Zwierzyny i Monitoringu Pól

---

### 1. Synteza wykonawcza (Executive Summary)

Projekt autonomicznego bezzałogowca rolniczego wyposażonego w podwójną głowicę optoelektroniczną (termowizja LWIR + RGB z zoomem) do prewencyjnego wykrywania zwierzyny i monitorowania pól jest **w pełni zasadny pod kątem rynkowym, technicznym i operacyjnym**, pod warunkiem właściwego pozycjonowania technologicznego i cenowego.

* **Zasadność rynkowa:** Bardzo wysoka. Straty w uprawach powodowane przez dziki, sarny i jelenie w Polsce i Europie liczone są w dziesiątkach milionów euro rocznie. Istnieje też rosnący wymóg prawno-etyczny wykrywania młodych koźląt saren na łąkach przed wjazdem wielkich kosiarek (rynek „fawn rescue”).
* **Zasadność techniczna:** Całkowicie wykonalna przy użyciu dojrzałych komponentów COTS (Commercial Off-The-Shelf) oraz otwartej architektury autopilota (PX4 / ArduPilot).
* **Zasadność prawna:** Loty nad polami z dala od skupisk ludzi pozwalają na relatywnie łatwe uzyskanie zgód na loty poza zasięg wzroku (BVLOS) w ramach standardowych scenariuszy EASA STS-02 lub procedury PDRA.

---

### 2. Analiza rynkowa i biznesowa

#### 2.1. Zdefiniowany problem klienta docelowego
1. **Szkody łowieckie w wysokich uprawach (kukurydza, rzepak, pszenżyto):**
   * Zwierzęta (watahy dzików) wchodzą w łan kukurydzy o wysokości 2,5–3 metrów. Z poziomu gruntu ani z ambony myśliwskiej nie sposób ich zlokalizować.
   * Zwierzęta potrafią w ciągu kilku nocy zniszczyć kilkanaście hektarów uprawy.
   * Koła łowieckie płacą rolnikom wysokie odszkodowania, co rodzi ciągłe konflikty na linii rolnik – myśliwy.
2. **Ratowanie koźląt i ptactwa (Fawn Rescue / Rehkitzrettung):**
   * Wiosną (maj–czerwiec) matki saren ukrywają nowonarodzone koźlęta w wysokiej trawie. Instynkt koźlęcia nakazuje mu przywierać do ziemi i nie uciekać.
   * Szybkie kosiarki rotacyjne (szerokość robocza 6–12 m, prędkość 15–25 km/h) masakrują tysiące zwierząt rocznie.
   * W Niemczech, Szwajcarii i Austrii loty dronem termowizyjnym przed koszeniem są już standardem branżowym, wspieranym dotacjami państwowymi. W Polsce trend ten dynamicznie rośnie.
3. **Szacowanie i dokumentacja strat dla ubezpieczycieli:**
   * Tworzenie ortofotomap termicznych i widzialnych z dokładnymi koordynatami GPS pozwala precyzyjnie zmierzyć powierzchnię zniszczonego łanu bez wchodzenia w uprawę.

#### 2.2. Otoczenie konkurencyjne
* **Obecni liderzy:** DJI Mavic 3 Enterprise Thermal (M3T), DJI Matrice 30T, Autel EVO II Dual 640T.
* **Słabe punkty konkurencji:**
  * Wysoki koszt zakupu (25 000 – 60 000 PLN).
  * Zamknięty ekosystem (vendor lock-in), brak możliwości głębokiej integracji z maszynami rolniczymi lub lokalnymi systemami ERP/Agro.
  * Ograniczenia geofencing (strefy No-Fly Zone narzucane przez chińskiego producenta).
  * Obawy dotyczące prywatności danych telemetrycznych i map terenu (coraz częstszy wymóg wykluczania sprzętu chińskiego w sektorach strategicznych).
* **Szansa dla projektu URSUS / Europa:**
  * Europejski łańcuch dostaw (European supply chain / NDAA compliant).
  * Dedykowane oprogramowanie AI szkolone pod kątem polskiej i europejskiej fauny oraz specyfiki upraw.
  * Integracja z ciągnikami i maszynami Ursus (dron jako opcjonalne „oko z powietrza” dla kombajnu lub kosiarki).

---

### 3. Zasadność techniczna i fizyka detekcji

#### 3.1. Dlaczego termowizja (LWIR)?
* Ciepłota ciała ssaka (dzik, sarna, człowiek) wynosi 37,5–39,5°C.
* O świcie (najlepszy moment na loty) lub po zmierzchu grunt, roślinność i ściółka mają temperaturę otoczenia (np. 5–15°C). Różnica $\Delta T$ na poziomie 15–25°C daje drastyczny, bezbłędny kontrast cieplny na matrycy mikrobolometrycznej.
* W ciągu słonecznego dnia detekcja w termowizji jest trudniejsza z powodu nagrzanych kamieni i kęp gleby – wówczas decydującą rolę odgrywa kamera dzienna RGB z zoomem oraz algorytm korelacji termiczno-optycznej.

#### 3.2. Wymogi sprzętowe sensora
* **Rozdzielczość matrycy termowizyjnej:** min. 640 x 512 pikseli (sensory 160x120 lub 320x240 są zbyt słabe do detekcji z pułapu roboczego 40–80 m AGL).
* **Czułość termiczna (NETD):** $\le 40\text{ mK}$ (pozwala odróżnić niewielkie różnice temperatur przez liście).
* **Optyka:** obiektyw 9 mm – 13 mm (szeroki kąt widzenia przy znośnym GSD, co pozwala pokryć duży hektar w jednym przelocie).
* **Kamera RGB:** matryca 4K / 48 MPx z zoomem optycznym/hybrydowym min. 4x–8x do szybkiego potwierdzenia celu bez konieczności zniżania drona.

#### 3.3. Wybór platformy nośnej
| Cecha | Multirotor (Quadcopter 4S/6S) | Hybryda VTOL (Płatowiec pionowzlot) |
| :--- | :--- | :--- |
| **Powierzchnia robocza** | 20 – 60 ha na jednym pakiecie | 200 – 600 ha na jednym locie |
| **Czas lotu** | 35 – 48 minut | 90 – 120 minut |
| **Zawis (Hovering)** | Tak – może wisieć nad celem i obserwować | Nie – musi krążyć wokół celu |
| **Łatwość obsługi** | Bardzo wysoka, start z każdego punktu pola | Średnia, wymaga większej przestrzeni |
| **Koszt wdrożenia** | Niski / średni | Wysoki |
| **Rekomendacja:** | **Faza 1 (MVP)** – dedykowany quadcopter agro | **Faza 2 (Skalowanie)** – VTOL na wielkie areały |

---

### 4. Aspekty formalno-prawne (EASA / ULC)

1. **Loty autonomiczne po ścieżce (Grid Survey):**
   * Wykonywane poza zasięgiem wzroku (BVLOS).
   * W Unii Europejskiej regulowane Rozporządzeniem Wykonawczym Komisji (UE) 2019/947.
   * Dostępne ścieżki certyfikacji:
     - **Scenariusz standardowy STS-02** (loty BVLOS z obserwatorami lub nad kontrolowanym obszarem naziemnym – pola uprawne idealnie spełniają kryterium niskiego ryzyka na ziemi i w powietrzu).
     - **PDRA-S02 / PDRA-G03** (deklaracja predefiniowanej oceny ryzyka SORA).
2. **Kwestia kamer termowizyjnych a „Dual-Use”:**
   * Kamery termowizyjne o odświeżaniu $\ge 9\text{ Hz}$ podlegają przepisom Porozumienia z Wassenaar oraz unijnemu rozporządzeniu o kontroli produktów podwójnego zastosowania (Dual-Use).
   * Zastosowanie wariantu 25/30/50 Hz wymaga zakupu od sprawdzonych dostawców (UE/USA/Korea/Japonia) z jasnym przeznaczeniem końcowym (End-User Statement na cele rolnicze).

---

### 5. Analiza SWOT

| Mocne strony (Strengths) | Słabe strony (Weaknesses) |
| :--- | :--- |
| • Ogromna oszczędność czasu i pieniędzy dla rolników<br>• Sprawdzona fizyka detekcji o świcie i w nocy<br>• Otwarta architektura (PX4/ArduPilot), brak vendor lock-in | • Ograniczenia czasu lotu baterii LiPo/Li-Ion w chłodne poranki<br>• Podatność na wiatr >12 m/s<br>• Zależność od warunków oświetleniowych/termicznych w upalne dni |
| **Szanse (Opportunities)** | **Zagrożenia (Threats)** |
| • Dotacje unijne na rolnictwo 4.0 i technologie precyzyjne<br>• Odwrót Europy od chińskiego sprzętu z kamerami (cyberbezpieczeństwo)<br>• Integracja z ekosystemem maszyn Ursus | • Cenowy dumping chińskich producentów wielkoseryjnych<br>• Zmiany w prawie lotniczym utrudniające autonomiczne loty BVLOS |

---

### 6. Wniosek końcowy

Projekt jest **wysoce uzasadniony i perspektywiczny**. 
Rekomendowane podejście inżynieryjne:
1. Budowa platformy w architekturze **modułowego Quadcoptera o masie startowej (MTOW) poniżej 4 kg** (klasa C2 / C3).
2. Wykorzystanie otwartego autopilota **Pixhawk / ArduPilot** z modułem **GNSS RTK** (precyzja centymetrowa dla powtarzalnych misji).
3. Podwójna głowica optoelektroniczna 640x512 LWIR + RGB 4K na gimbalu 3-osiowym.
4. Oprogramowanie detekcyjne AI bazujące na architekturze YOLO do oznaczania zwierząt w czasie rzeczywistym na ekranie operatora.

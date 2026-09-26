# STRATEGIA OPROGRAMOWANIA I ASPEKTY LICENCYJNE (ARDUPILOT VS PX4 VS WŁASNY KOD)
## Jak legalnie i bezpiecznie budować komercyjnego drona bez pisania autopilota od zera

---

### 1. Kluczowa odpowiedź: Czy można sprzedawać drony z ArduPilotem?

**TAK, w 100% TAK.**
Można legalnie sprzedawać drony z zainstalowanym ArduPilotem i pobierać za nie dowolną cenę. Licencja w żaden sposób nie ogranicza działalności komercyjnej.

Na ArduPilocie bazują wiodące komercyjne firmy dronowe na świecie, m.in.:
* **Wingtra** (profesjonalne drony geodezyjne i rolnicze VTOL za 100 000+ PLN),
* **Watts Innovations** (amerykańskie drony przemysłowe),
* **Blue Robotics** (podwodne pojazdy ROV),
* **Harris Aerial**, **Elistair** i setki innych.

---

### 2. Jak działa licencja ArduPilota (GPLv3) i co wymusza?

ArduPilot jest udostępniany na licencji **GNU GPLv3 (General Public License)**. Jest to licencja typu *Copyleft*. Co to oznacza w praktyce?

1. **Sprzedaż sprzętu:** W pełni dozwolona.
2. **Używanie gotowego firmware'u:** Jeśli wgrywasz oficjalny ArduPilot i konfigurujesz parametry (PID-y, siatki, geofence, serwa) – **nie musisz nikomu pokazywać ani udostępniać swoich ustawień**.
3. **Modyfikacja kodu ArduPilota:** Jeśli zmienisz sam kod źródłowy C++ wewnątrz ArduPilota (np. napiszesz własną odmianę filtra EKF w autopilotcie) i sprzedasz drona klientowi, masz obowiązek przekazać **temu klientowi** kod źródłowy wprowadzonych zmian w ArduPilocie.

---

### 3. Gdzie ukryć i chronić swoje IP (Własność Intelektualną)?

Nie musisz pisać własnego autopilota, aby mieć unikalny, chroniony patentami i prawem autorskim produkt komercyjny. W branży dronowej stosuje się **architekturę dwuwarstwową**:

```
+-------------------------------------------------------------+
|         TWOJA WŁASNOŚĆ INTELEKTUALNA (100% ZAMKNIĘTY KOD)    |
|                                                             |
|  • Model AI detekcji dzików (wagi sieci YOLO)               |
|  • Algorytm logiki decyzyjnej odstraszania (Threat Engine)  |
|  • Aplikacja mobilna / tabletowa dla rolnika (GUI)          |
|  • Moduł generowania raportów szkód (GeoJSON / PDF)        |
+-------------------------------------------------------------+
                              ▲
                              │ Protokół MAVLink
                              │ (Licencja LGPL/MIT - nie zaraża!)
                              ▼
+-------------------------------------------------------------+
|               WARSTWA WYKONAWCZA (OTWARTA)                  |
|                                                             |
|  • ArduPilot / PX4 (stabilizacja lotu, EKF3, silniki, GPS)  |
+-------------------------------------------------------------+
```

Protokół komunikacji **MAVLink** jest na licencji MIT/LGPL. Oznacza to, że Twój zamknięty program na telefonie/laptopie lub komputerze pokładowym komunikuje się z ArduPilotem przez MAVLink, **nie podlegając pod licencję GPL**. Twoje algorytmy, sztuczna inteligencja i aplikacja pozostają w 100% Twoją prywatną tajemnicą przedsiębiorstwa.

---

### 4. Dlaczego pisanie własnego autopilota od zera to błąd biznesowy?

Próba napisania własnego autopilota (firmware sterującego silnikami i lotem) od zera to najczęstsza pułapka początkujących projektów technologicznych (tzw. *reinventing the wheel*):
1. **Czas i koszt:** ArduPilot jest rozwijany od ponad 15 lat przez setki inżynierów i matematyków. Napisanie od podstaw filtrów EKF3 (fuzja żyroskopów, akcelerometrów, GPS RTK, magnetometru i barometru) wymagałoby zespołu 5–8 wyspecjalizowanych inżynierów, 3–4 lat pracy i milionów złotych budżetu.
2. **Bezpieczeństwo i niezawodność:** ArduPilot ma za sobą miliony godzin lotu w powietrzu. Autorski autopilot w pierwszych fazach będzie regularnie rozbijał maszyny o ziemię z powodu błędów w estymacji kątów lub utraty sygnału satelitów.
3. **Brak wsparcia dla osprzętu:** ArduPilot obsługuje tysiące sensorów COTS (lidary, regulatory ESC CAN/DShot, kamery, radia) „out-of-the-box”. Pisząc własny soft, musiałbyś napisać sterowniki do każdego układu scalonego.

---

### 5. Alternatywa: PX4 Autopilot (Licencja BSD – brak Copyleftu)

Jeśli inwestorzy lub partnerzy kategorycznie boją się licencji GPLv3, bezpośrednią alternatywą dla ArduPilota jest **PX4 Autopilot**:
* **Licencja:** **BSD 3-Clause** (skrajnie permisywna).
* **Zasada:** Możesz modyfikować kod źródłowy PX4, zamknąć go całkowicie, nie udostępniać nikomu ani jednej linijki i sprzedawać jako „własny zamknięty system”.
* **Kto na tym bazuje:** Auterion, Skydio, Teal Drones, Freefly Systems.
* Działa na tych samych płytkach kontrolerów lotu (SpeedyBee, Matek, Pixhawk, Cube).

---

### 6. Rekomendacja wdrożeniowa dla projektu URSUS

1. **Na kontrolerze lotu (w dronie):** Użyć czystego **ArduCopter** lub **PX4**.
2. **Konfiguracja:** Zapisać autorski profil parametrów (PID-y dopasowane do ramy, parametry lotu automatycznego).
3. **Twoja unikalna wartość handlowa (Core IP):**
   * Gotowa konstrukcja drona i integracja z kamerą Caddx.
   * Dedykowana aplikacja rolnicza „Ursus Agro Control” (zaprojektowana tak prosto, by rolnik tylko zaznaczył pole na mapie i wcisnął *START*).
   * Wytrenowany model AI rozpoznający dziki, sarny i koźlęta w kukurydzy.
   * Moduł autonomicznego odstraszania.

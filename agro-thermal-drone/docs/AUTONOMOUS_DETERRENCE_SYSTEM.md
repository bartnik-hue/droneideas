# AUTONOMICZNY SYSTEM OCENY ZAGROŻENIA I ODSTRASZANIA AKUSTYCZNEGO
## Moduł: Autonomous Threat Decision & Acoustic Deterrence (ATD-AD)

---

### 1. Koncepcja i Rola Systemu

Wprowadzenie autonomicznego odstraszania zmienia rolę drona z **biernego obserwatora (Passive Scout)** w **aktywnego strażnika upraw (Active Crop Sentinel)**.

Dron podczas rutynowego, automatycznego lotu patrolowego po siatce:
1. Nie wymaga ciągłej uwagi operatora – może pracować w pełni autonomicznie w nocy lub o świcie.
2. W ułamku sekundy wykrywa i identyfikuje intruza.
3. Podejmuje logiczną decyzję: **CZY** i **JAK** odstraszać.
4. Wykonuje ukierunkowany manewr i emituje sygnał akustyczno-optyczny.
5. Weryfikuje skuteczność (czy zwierzyna opuściła pole) i wznawia zaplanowaną misję.

---

### 2. Silnik Decyzyjny AI (Threat Assessment Engine)

Autonomiczne odstraszanie **nie może działać na ślepo** (np. na każdy punkt cieplny). System musi precyzyjnie rozróżniać obiekty, aby nie wywoływać niepożądanych skutków.

```
       [ Detekcja punktu cieplnego LWIR ]
                       │
                       ▼
       [ Klasyfikacja AI (YOLO + RGB) ]
                       │
      ┌────────────────┼────────────────┬────────────────┐
      ▼                ▼                ▼                ▼
[ Dzik / Wataha ]   [ Sarna / Jeleń ]   [ Koźlę w trawie ] [ Człowiek / Bydło ]
      │                │                │                │
      ▼                ▼                ▼                ▼
Czy w strefie?    Czy w strefie?   [ STOP HUK! ]    [ STOP HUK! ]
(Crop Polygon)    (Crop Polygon)   Tylko geolog     Cichy patrol,
      │                │           dla kosiarki     alert do bazy
      ▼                ▼                
 [ ZAGROŻENIE ]   [ ZAGROŻENIE ]
      │                │
      └────────┬───────┘
               ▼
   [ PROCEDURA ODSTRASZANIA ]
   1. Zniżenie na 30m AGL
   2. Emisja dźwięku bioakustycznego
   3. Błysk stroboskopu
   4. Weryfikacja wektora ucieczki
   5. Powrót do siatki lotu
```

#### 2.1. Matryca Decyzyjna
| Wykryty obiekt | Działanie systemu | Uzasadnienie |
| :--- | :--- | :--- |
| **Dzik / Wataha dzików** | **AKTYWNE ODSTRASZANIE (Maksymalna moc)** | Główny szkodnik kukurydzy i zbóż. Szybkie wypłoszenie zapobiega zniszczeniom. |
| **Jeleń / Daniel / Sarna (dorosła)** | **AKTYWNE ODSTRASZANIE (Średnia moc)** | Żerowanie w oziminach i rzepaku. Wypłoszenie w stronę lasu. |
| **Koźlę sarny (młode leżące)** | **BRAK ODSTRASZANIA (Cichy geolog)** | Koźlę nie ucieka, lecz zamiera w bezruchu. Dźwięk wywołałby szok. Zapisujemy GPS dla kosiarki. |
| **Człowiek (rolnik, grzybiarz)** | **BRAK ODSTRASZANIA** | Bezpieczeństwo i przepisy prawne. Wysłanie dyskretnego powiadomienia do aplikacji operatora. |
| **Bydło / Konie na pastwisku** | **BRAK ODSTRASZANIA** | Zapobieganie spłoszeniu stada i przerwaniu ogrodzeń pastwiska (elektrycznego pastucha). |

---

### 3. Architektura Sprzętowa Odstraszania (Hardware Payload)

Aby odstraszanie było skuteczne z pułapu lotu drona, zastosowano dedykowany moduł akustyczno-optyczny zintegrowany z ramą.

#### 3.1. Megafon Kierunkowy (Acoustic Payload)
* **Ciśnienie akustyczne (SPL):** **120 – 128 dB @ 1 m**.
* **Efektywny zasięg na ziemi:** Przy pułapie 30–40 m AGL, poziom dźwięku docierający do gruntu wynosi **85–95 dB**, co jest dla zwierząt bodźcem silnie awersyjnym (próg paniki).
* **Masa:** $\le 350\text{ g}$ (lekka membrana neodymowa + tuba kompozytowa).
* **Zasilanie:** Bezpośrednio z szyny głównej baterii (24V / 6S) przez zabezpieczony przetwornik impulsowy.
* **Sterowanie:** Interfejs UART / PWM wyzwalany z pokładowego komputera Edge AI lub wyjścia AUX autopilota.

#### 3.2. Repertuar Dźwiękowy (Zapobieganie Przyzwyczajeniu - Anti-Habituation)
Zwierzęta szybko uczą się jednostajnego dźwięku (np. ciągłego pisku). System wykorzystuje zmienny generator dźwięków:
1. **Dźwięki bioakustyczne (drapieżniki):** Agresywne szczekanie watahy psów gończych (łajki, ogary polskie) – wywołuje u dzików wrodzony odruch ucieczki.
2. **Dźwięki pirotechniczne:** Zsyntetyzowane odgłosy wystrzałów z broni myśliwskiej i armatek hukowych.
3. **Sygnały syntetyczne o zmiennej częstotliwości (Swept Chirp):** Modulowane tony 1 kHz – 5 kHz o dużej dynamice zmian, uniemożliwiające adaptację słuchową.

#### 3.3. Diodowy Stroboskop Płoszący (Visual Strobe)
* **Emiter:** 2x dioda Cree XHP70 (łączny strumień >5000 lumenów).
* **Tryb pracy:** Błyski stroboskopowe o częstotliwości 12–18 Hz (częstotliwość silnie dezorientująca ssaki nocne).
* **Efekt synergii:** Dźwięk + nagły błysk światła w całkowitych ciemnościach zmusza watahę do natychmiastowego odwrotu w kierunku najbliższej ściany lasu.

---

### 4. Taktyka Manewru w Powietrzu (Tactical Flight Logic)

Gdy algorytm podejmie decyzję o akcji, autopilot wykonuje procedurę **Dynamic Interception & Deterrence**:

1. **Grid Hold:** Autopilot wstrzymuje lot po ścieżce (komenda MAVLink `MAV_CMD_DO_PAUSE_CONTINUE`).
2. **Descend & Vector:** Dron obniża pułap z wysokości patrolowej (np. 60 m) na wysokość operacyjną (np. 25–30 m AGL) i kieruje kamerę oraz megafon pod kątem w stronę zwierzyny.
3. **Burst Fire (Dźwięk + Światło):** Emisja 5-10 sekundowej serii odstraszającej.
4. **Escape Tracking:** Kamera termowizyjna weryfikuje ruch wektora celów:
   * Jeśli zwierzęta uciekają w stronę granicy pola: dron utrzymuje pozycję i asystuje aż do opuszczenia uprawy.
   * Jeśli zwierzęta nie reagują: zmiana profilu dźwiękowego (np. z psów na wystrzały) i zniżenie o kolejne 5 metrów.
5. **Resume & Log:** Po oczyszczeniu sektora dron powraca na pierwotną wysokość i wznawia skanowanie pola od miejsca przerwania. Do bazy wysyłany jest raport zdarzenia (czas, współrzędne GPS, gatunek, liczba sztuk, nagranie wideo 10s).

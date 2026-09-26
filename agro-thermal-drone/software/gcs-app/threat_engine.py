"""
Silnik decyzyjny autonomicznego odstraszania i oceny zagrożenia (Threat Assessment Engine)
Projekt: Ursus Agro Sentinel
"""

import sys
from typing import Dict, List, Tuple, Any

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class ThreatDecisionEngine:
    """
    Klasa odpowiedzialna za analizę obiektów wykrytych przez model AI,
    korelację z granicami uprawy i podejmowanie autonomicznych decyzji o odstraszaniu.
    """

    # Klasy obiektów z modelu YOLOv8-Thermal
    SPECIES_WILD_BOAR = "dzik"
    SPECIES_DEER = "sarna_jelen"
    SPECIES_FAWN = "kozle_lezące"
    SPECIES_HUMAN = "czlowiek"
    SPECIES_CATTLE = "bydlo_konie"

    def __init__(self, field_polygon: List[Tuple[float, float]]):
        """
        :param field_polygon: Lista współrzędnych [(lat, lon), ...] definiująca chronione pole.
        """
        self.field_polygon = field_polygon

    def point_in_polygon(self, lat: float, lon: float) -> bool:
        """
        Algorytm Ray-Casting sprawdzający, czy dany punkt GPS leży wewnątrz wieloboku pola.
        """
        num_vertices = len(self.field_polygon)
        inside = False
        p1_lat, p1_lon = self.field_polygon[0]

        for i in range(1, num_vertices + 1):
            p2_lat, p2_lon = self.field_polygon[i % num_vertices]
            if lon > min(p1_lon, p2_lon):
                if lon <= max(p1_lon, p2_lon):
                    if lat <= max(p1_lat, p2_lat):
                        if p1_lon != p2_lon:
                            lat_inters = (lon - p1_lon) * (p2_lat - p1_lat) / (p2_lon - p1_lon) + p1_lat
                        if p1_lat == p2_lat or lat <= lat_inters:
                            inside = not inside
            p1_lat, p1_lon = p2_lat, p2_lon

        return inside

    def evaluate_threat(self, detection: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ocena pojedynczej detekcji AI i wyznaczenie akcji systemu.
        
        :param detection: Słownik zawierający:
               - "species": nazwa wykrytego gatunku,
               - "confidence": pewność predykcji (0.0 - 1.0),
               - "target_lat": oszacowana szerokość geograficzna celu,
               - "target_lon": oszacowana długość geograficzna celu
        :return: Słownik z decyzją taktyczną.
        """
        species = detection.get("species", "").lower()
        confidence = detection.get("confidence", 0.0)
        target_lat = detection.get("target_lat", 0.0)
        target_lon = detection.get("target_lon", 0.0)

        # 1. Filtr zaufania AI
        if confidence < 0.65:
            return {
                "action": "IGNORE_LOW_CONFIDENCE",
                "species": species,
                "confidence": confidence,
                "siren_active": False,
                "reason": "Zbyt niska pewność detekcji AI (<65%)"
            }

        # 2. Sprawdzenie, czy intruz znajduje się wewnątrz chronionej uprawy
        is_in_crop = self.point_in_polygon(target_lat, target_lon)
        if not is_in_crop:
            return {
                "action": "LOG_OUTSIDE_FIELD",
                "species": species,
                "confidence": confidence,
                "siren_active": False,
                "reason": "Zwierzę przebywa poza granicami pola (np. w lesie/na drodze)"
            }

        # 3. Logika decyzyjna w zależności od gatunku
        if species == self.SPECIES_WILD_BOAR:
            return {
                "action": "TRIGGER_DETERRENCE_MAX",
                "species": species,
                "confidence": confidence,
                "siren_active": True,
                "strobe_active": True,
                "sound_profile": "DOGS_AND_PYRO",
                "descend_target_agl": 22.0,
                "reason": "ZAGROŻENIE KRYTYCZNE: Dzik w uprawie. Natychmiastowe wypłaszanie."
            }

        elif species == self.SPECIES_DEER:
            return {
                "action": "TRIGGER_DETERRENCE_MODERATE",
                "species": species,
                "confidence": confidence,
                "siren_active": True,
                "strobe_active": True,
                "sound_profile": "SYNTH_CHIRP",
                "descend_target_agl": 25.0,
                "reason": "ZAGROŻENIE ŚREDNIE: Żerująca zwierzyna płowa. Wypłaszanie umiarkowane."
            }

        elif species == self.SPECIES_FAWN:
            return {
                "action": "FAWN_RESCUE_MARKER",
                "species": species,
                "confidence": confidence,
                "siren_active": False,
                "strobe_active": False,
                "sound_profile": None,
                "descend_target_agl": None,
                "reason": "OCHRONA KOŹLĘCIA: Bezwzględny zakaz hałasu. Zapisano współrzędne GPS dla kosiarki."
            }

        elif species == self.SPECIES_HUMAN:
            return {
                "action": "ALERT_OPERATOR_HUMAN_DETECTED",
                "species": species,
                "confidence": confidence,
                "siren_active": False,
                "strobe_active": False,
                "reason": "BEZPIECZEŃSTWO: Wykryto człowieka w uprawie. Przekazano podgląd do operatora."
            }

        else:
            return {
                "action": "LOG_UNKNOWN",
                "species": species,
                "confidence": confidence,
                "siren_active": False,
                "reason": "Nieznana sygnatura cieplna."
            }


if __name__ == "__main__":
    # Test działania silnika decyzyjnego
    test_field = [
        (51.2400, 22.6100),
        (51.2400, 22.6200),
        (51.2500, 22.6200),
        (51.2500, 22.6100)
    ]
    engine = ThreatDecisionEngine(test_field)

    scenarios = [
        {"species": "dzik", "confidence": 0.92, "target_lat": 51.2450, "target_lon": 22.6150},
        {"species": "kozle_lezące", "confidence": 0.88, "target_lat": 51.2420, "target_lon": 22.6120},
        {"species": "dzik", "confidence": 0.94, "target_lat": 51.2600, "target_lon": 22.6150}, # Poza polem
        {"species": "czlowiek", "confidence": 0.85, "target_lat": 51.2430, "target_lon": 22.6140}
    ]

    print("--- WYNIKI TESTU SILNIKA DECYZYJNEGO URSUS AGRO ---")
    for s in scenarios:
        res = engine.evaluate_threat(s)
        print(f"Gatunek: {s['species']:15} | Akcja: {res['action']:25} | Syrena: {res['siren_active']} | Powód: {res['reason']}")

"""
Moduł weryfikacji bilansu energii, tranzytu ze startu i wymuszania 15% rezerwy bezpieczeństwa
Projekt: Ursus Agro Sentinel / Agro-Thermal-Drone
"""

import math
import sys
from typing import List, Tuple, Dict, Any

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def haversine_distance_m(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Oblicza odległość w metrach między dwoma punktami GPS (lat, lon) metodą Haversine."""
    lat1, lon1 = p1
    lat2, lon2 = p2
    R = 6371000.0 # Promień Ziemi w metrach

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return R * c


class BatterySafetyValidator:
    """
    Kalkulator i walidator bezpieczeństwa energetycznego misji z uwzględnieniem
    odległości od punktu startu (Home) do pola i twardej 15% rezerwy na powrót.
    """

    def __init__(
        self,
        battery_wh: float = 194.4,     # Pakiet 6S2P 9000mAh Molicel P45B
        cruise_power_w: float = 270.0, # Średni pobór mocy w locie
        survey_speed_mps: float = 8.0, # Prędkość patrolowa nad polem (~29 km/h)
        transit_speed_mps: float = 12.0 # Prędkość tranzytu dolot/powrót (~43 km/h)
    ):
        self.battery_wh = battery_wh
        self.cruise_power_w = cruise_power_w
        self.survey_speed = survey_speed_mps
        self.transit_speed = transit_speed_mps

        # Twarda rezerwa bezpieczeństwa: 15% energii pozostaje nienaruszone na powrót i wiatr
        self.safety_reserve_pct = 0.15
        self.usable_wh = self.battery_wh * (1.0 - self.safety_reserve_pct)
        self.max_usable_time_s = (self.usable_wh / self.cruise_power_w) * 3600.0

    def validate_mission(
        self,
        home_pos: Tuple[float, float],
        waypoints: List[Dict[str, Any]],
        estimated_deterrence_actions: int = 3
    ) -> Dict[str, Any]:
        """
        Walidacja misji: sprawdza czy suma (dolot + siatka + powrót + akcje odstraszania)
        mieści się w 85% pojemności pakietu.
        """
        if not waypoints:
            raise ValueError("Brak waypointów do analizy!")

        first_wp = (waypoints[1]["lat"], waypoints[1]["lon"])
        last_wp = (waypoints[-2]["lat"], waypoints[-2]["lon"])

        # 1. Dystans dolotu z miejsca startu do początku pola
        transit_in_dist_m = haversine_distance_m(home_pos, first_wp)
        transit_in_time_s = transit_in_dist_m / self.transit_speed

        # 2. Dystans powrotu z końca pola do miejsca startu
        transit_out_dist_m = haversine_distance_m(last_wp, home_pos)
        transit_out_time_s = transit_out_dist_m / self.transit_speed

        # 3. Dystans przelotu nad siatką pola
        grid_dist_m = 0.0
        for i in range(1, len(waypoints) - 2):
            p_a = (waypoints[i]["lat"], waypoints[i]["lon"])
            p_b = (waypoints[i+1]["lat"], waypoints[i+1]["lon"])
            grid_dist_m += haversine_distance_m(p_a, p_b)
        grid_time_s = grid_dist_m / self.survey_speed

        # 4. Rezerwa czasu i energii na manewry zniżenia, oświetlenia LED i odstraszania
        # (Założenie: 45s na każdą akcję weryfikacji z podwyższonym poborem LED)
        deterrence_time_s = estimated_deterrence_actions * 45.0

        total_time_s = transit_in_time_s + grid_time_s + transit_out_time_s + deterrence_time_s
        total_dist_m = transit_in_dist_m + grid_dist_m + transit_out_dist_m

        energy_consumed_wh = (total_time_s / 3600.0) * self.cruise_power_w
        battery_used_pct = (energy_consumed_wh / self.battery_wh) * 100.0
        remaining_battery_pct = 100.0 - battery_used_pct

        # Twardy warunek: pozostała bateria musi wynosić co najmniej 15%
        is_safe = remaining_battery_pct >= (self.safety_reserve_pct * 100.0)

        result = {
            "is_safe": is_safe,
            "total_time_min": round(total_time_s / 60.0, 1),
            "total_dist_km": round(total_dist_m / 1000.0, 2),
            "transit_in_km": round(transit_in_dist_m / 1000.0, 2),
            "transit_out_km": round(transit_out_dist_m / 1000.0, 2),
            "grid_dist_km": round(grid_dist_m / 1000.0, 2),
            "battery_used_pct": round(battery_used_pct, 1),
            "remaining_battery_pct": round(remaining_battery_pct, 1),
            "safety_reserve_pct": self.safety_reserve_pct * 100.0,
            "max_allowed_time_min": round(self.max_usable_time_s / 60.0, 1),
            "recommendation": "PLAN ZAAKCEPTOWANY: Bezpieczny zapas baterii." if is_safe else
                              "UWAGA: Przekroczono 85% baterii! Planer automatycznie dzieli pole na 2 loty."
        }
        return result


if __name__ == "__main__":
    from mission_generator import AgroMissionPlanner

    print("--- TEST KALKULATORA BEZPIECZEŃSTWA ENERGETYCZNEGO I STARTU ---")
    
    # Miejsce startu: Brama gospodarstwa rolnika
    home = (51.2350, 22.6050)
    
    # Pole kukurydzy oddalone o ~800 metrów od gospodarstwa
    field_polygon = [
        (51.2401, 22.6102),
        (51.2403, 22.6180),
        (51.2465, 22.6185),
        (51.2462, 22.6100)
    ]

    planner = AgroMissionPlanner(camera_hfov_deg=50.0)
    waypoints = planner.generate_grid_for_polygon(field_polygon, altitude_m=35.0, speed_mps=8.0)

    validator = BatterySafetyValidator(battery_wh=194.4, cruise_power_w=270.0)
    audit = validator.validate_mission(home, waypoints, estimated_deterrence_actions=3)

    print(f"Lokalizacja startu (Home): {home}")
    print(f"Dolot do pola: {audit['transit_in_km']} km | Powrót do bazy: {audit['transit_out_km']} km")
    print(f"Trasa siatki nad polem: {audit['grid_dist_km']} km")
    print(f"Łączny dystans misji: {audit['total_dist_km']} km")
    print(f"Szacowany czas całkowity: {audit['total_time_min']} min (Maksimum bezpieczne: {audit['max_allowed_time_min']} min)")
    print(f"Zużycie baterii: {audit['battery_used_pct']}% | Pozostanie w baterii: {audit['remaining_battery_pct']}%")
    print(f"Weryfikacja 15% rezerwy: {'[POZYTYWNA]' if audit['is_safe'] else '[NEGATYWNA - WYMAGANY PODZIAŁ]'}")
    print(f"Komunikat: {audit['recommendation']}")

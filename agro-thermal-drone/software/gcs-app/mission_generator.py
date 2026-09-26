"""
Moduł generowania optymalnych siatek lotu patrolowego dla rolnictwa (Boustrophedon Grid Generator)
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

class AgroMissionPlanner:
    """
    Kalkulator i generator autonomicznych ścieżek patrolowych nad polami uprawnymi.
    Dopasowany pod parametry optyki kamer Caddx Eclipse.
    """

    def __init__(self, camera_hfov_deg: float = 50.0, camera_aspect: float = 4/3):
        """
        :param camera_hfov_deg: Poziomy kąt widzenia kamery (dla Caddx Eclipse 640 ~50 st.)
        :param camera_aspect: Proporcje sensora (zazwyczaj 4:3)
        """
        self.camera_hfov = math.radians(camera_hfov_deg)
        self.camera_aspect = camera_aspect

    def calculate_footprint(self, altitude_m: float) -> Tuple[float, float]:
        """
        Oblicza wymiary obszaru terenu objętego pojedynczą klatką kamery (Footprint na ziemi)
        przy danej wysokości lotu AGL.
        """
        ground_width = 2 * altitude_m * math.tan(self.camera_hfov / 2)
        ground_height = ground_width / self.camera_aspect
        return ground_width, ground_height

    def calculate_line_spacing(self, altitude_m: float, side_overlap_pct: float = 0.25) -> float:
        """
        Oblicza odległość między sąsiednimi liniami przelotu z uwzględnieniem zakładki bocznej.
        """
        width, _ = self.calculate_footprint(altitude_m)
        spacing = width * (1.0 - side_overlap_pct)
        return max(5.0, spacing)

    def generate_grid_for_polygon(
        self,
        polygon_coords: List[Tuple[float, float]],
        altitude_m: float = 35.0,
        speed_mps: float = 8.0,
        side_overlap_pct: float = 0.25
    ) -> List[Dict[str, Any]]:
        """
        Generuje listę waypointów w układzie WGS-84 (lat, lon, alt) pokrywających wielobok pola.
        
        :param polygon_coords: Lista krotek [(lat, lon), (lat, lon), ...]
        :param altitude_m: Wysokość robocza nad gruntem (AGL)
        :param speed_mps: Prędkość patrolowa w m/s (np. 8 m/s = ~29 km/h)
        :param side_overlap_pct: Wymagana zakładka klatek (domyślnie 25%)
        :return: Lista słowników z definicjami waypointów MAVLink
        """
        if len(polygon_coords) < 3:
            raise ValueError("Wielobok pola musi posiadać co najmniej 3 wierzchołki!")

        spacing_m = self.calculate_line_spacing(altitude_m, side_overlap_pct)
        
        # Przybliżenie: 1 stopień szerokości geograficznej ~ 111 320 m
        meters_per_deg_lat = 111320.0
        center_lat = sum(p[0] for p in polygon_coords) / len(polygon_coords)
        meters_per_deg_lon = 111320.0 * math.cos(math.radians(center_lat))

        # Wyznaczenie Bounding Boxa
        min_lat = min(p[0] for p in polygon_coords)
        max_lat = max(p[0] for p in polygon_coords)
        min_lon = min(p[1] for p in polygon_coords)
        max_lon = max(p[1] for p in polygon_coords)

        # Odległość północ-południe i wschód-zachód
        delta_lat_m = (max_lat - min_lat) * meters_per_deg_lat
        delta_lon_m = (max_lon - min_lon) * meters_per_deg_lon

        num_lines = max(2, int(delta_lon_m / spacing_m) + 1)
        lon_step_deg = (spacing_m / meters_per_deg_lon)

        waypoints = []
        
        # 1. Punkt START / TAKEOFF
        waypoints.append({
            "seq": 0,
            "command": "TAKEOFF",
            "lat": polygon_coords[0][0],
            "lon": polygon_coords[0][1],
            "alt": altitude_m,
            "speed": speed_mps
        })

        # 2. Generowanie zygzaka (Boustrophedon)
        reverse = False
        current_lon = min_lon
        seq = 1

        for _ in range(num_lines):
            if current_lon > max_lon:
                current_lon = max_lon

            if not reverse:
                # Linia z południa na północ
                waypoints.append({
                    "seq": seq, "command": "WAYPOINT",
                    "lat": min_lat, "lon": current_lon, "alt": altitude_m, "speed": speed_mps
                })
                seq += 1
                waypoints.append({
                    "seq": seq, "command": "WAYPOINT",
                    "lat": max_lat, "lon": current_lon, "alt": altitude_m, "speed": speed_mps
                })
                seq += 1
            else:
                # Linia z północy na południe
                waypoints.append({
                    "seq": seq, "command": "WAYPOINT",
                    "lat": max_lat, "lon": current_lon, "alt": altitude_m, "speed": speed_mps
                })
                seq += 1
                waypoints.append({
                    "seq": seq, "command": "WAYPOINT",
                    "lat": min_lat, "lon": current_lon, "alt": altitude_m, "speed": speed_mps
                })
                seq += 1

            current_lon += lon_step_deg
            reverse = not reverse

        # 3. Zakończenie misji: Powrót do bazy (RTL)
        waypoints.append({
            "seq": seq,
            "command": "RTL",
            "lat": 0.0,
            "lon": 0.0,
            "alt": altitude_m,
            "speed": speed_mps
        })

        return waypoints


if __name__ == "__main__":
    # Test działania generatora siatki dla przykładowej działki rolnej (np. kukurydza 15 ha)
    planner = AgroMissionPlanner(camera_hfov_deg=50.0)
    
    # Koordynaty przykładowego pola w Lubelskiem
    field_coords = [
        (51.2401, 22.6102),
        (51.2403, 22.6180),
        (51.2465, 22.6185),
        (51.2462, 22.6100)
    ]
    
    w, h = planner.calculate_footprint(altitude_m=35.0)
    spacing = planner.calculate_line_spacing(altitude_m=35.0, side_overlap_pct=0.25)
    print(f"Kamera Caddx Eclipse @ 35m AGL -> Pokrycie klatki: {w:.1f}m x {h:.1f}m")
    print(f"Rozstaw linii przelotu z 25% zakładką: {spacing:.1f} m")

    mission = planner.generate_grid_for_polygon(field_coords, altitude_m=35.0, speed_mps=8.0)
    print(f"\nWygenerowano misję składającą się z {len(mission)} punktów nawigacyjnych.")
    for wp in mission[:5]:
        print(f"  WP #{wp['seq']}: {wp['command']} -> Lat: {wp['lat']:.5f}, Lon: {wp['lon']:.5f}, Alt: {wp['alt']}m")
    print("  ...")
    print(f"  WP #{mission[-1]['seq']}: {mission[-1]['command']}")

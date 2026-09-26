"""
Moduł dwukierunkowej komunikacji MAVLink z dronem (MAVLink Bridge)
Projekt: Ursus Agro Sentinel
Wymagania: pymavlink (pip install pymavlink)
"""

import sys
import time
from typing import List, Dict, Any, Optional

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from pymavlink import mavutil
    PYMAVLINK_AVAILABLE = True
except ImportError:
    PYMAVLINK_AVAILABLE = False


class AgroMavlinkBridge:
    """
    Most komunikacyjny łączący autorską stację GCS z autopilotem ArduPilot na pokładzie drona.
    """

    def __init__(self, connection_string: str = "udpin:localhost:14550", baud: int = 57600):
        """
        :param connection_string: Ścieżka połączenia (np. 'COM3', '/dev/ttyUSB0', 'udpin:0.0.0.0:14550')
        :param baud: Prędkość transmisji dla portu szeregowego
        """
        self.connection_string = connection_string
        self.baud = baud
        self.master = None
        self.is_connected = False

    def connect(self) -> bool:
        """Nawiązanie połączenia i oczekiwanie na Heartbeat z drona."""
        if not PYMAVLINK_AVAILABLE:
            print("[MAVLink] BŁĄD: Biblioteka 'pymavlink' nie jest zainstalowana w systemie.")
            return False

        try:
            print(f"[MAVLink] Łączenie z dronem przez {self.connection_string}...")
            self.master = mavutil.mavlink_connection(self.connection_string, baud=self.baud)
            self.master.wait_heartbeat(timeout=5)
            self.is_connected = True
            print(f"[MAVLink] Połączono pomyślnie! System ID: {self.master.target_system}, Component ID: {self.master.target_component}")
            return True
        except Exception as e:
            print(f"[MAVLink] Nie udało się połączyć: {e}")
            self.is_connected = False
            return False

    def upload_mission(self, waypoints: List[Dict[str, Any]]) -> bool:
        """
        Wgrywa wygenerowaną listę punktów nawigacyjnych (misję polową) do pamięci ArduPilota.
        """
        if not self.is_connected or not self.master:
            print("[MAVLink] Brak aktywnego połączenia z dronem!")
            return False

        print(f"[MAVLink] Wgrywanie misji agro ({len(waypoints)} punktów)...")
        # Wyczyszczenie starej misji
        self.master.waypoint_clear_all_send()

        # Deklaracja liczby punktów
        self.master.waypoint_count_send(len(waypoints))

        for wp in waypoints:
            # Oczekiwanie na zapytanie o konkretny numer punktu
            msg = self.master.recv_match(type=['MISSION_REQUEST'], blocking=True, timeout=3)
            if not msg:
                print(f"[MAVLink] Timeout podczas oczekiwania na MISSION_REQUEST dla punktu #{wp['seq']}")
                return False

            cmd_type = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
            if wp["command"] == "TAKEOFF":
                cmd_type = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
            elif wp["command"] == "RTL":
                cmd_type = mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH

            self.master.mav.mission_item_int_send(
                self.master.target_system,
                self.master.target_component,
                wp["seq"],
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
                cmd_type,
                0, 1, # current, autocontinue
                0, 0, 0, 0, # param 1-4
                int(wp["lat"] * 1e7),
                int(wp["lon"] * 1e7),
                float(wp["alt"])
            )

        # Oczekiwanie na potwierdzenie przyjęcia całej misji (MISSION_ACK)
        ack = self.master.recv_match(type=['MISSION_ACK'], blocking=True, timeout=5)
        if ack and ack.type == mavutil.mavlink.MAV_MISSION_ACCEPTED:
            print("[MAVLink] Misja wgrana i zaakceptowana przez drona!")
            return True
        else:
            print(f"[MAVLink] Błąd zapisu misji: {ack}")
            return False

    def trigger_deterrence_siren(self, activate: bool = True) -> bool:
        """
        Włącza lub wyłącza syrenę piezoelektryczną i stroboskop LED przez wyjście przekaźnika/serwa AUX.
        """
        if not self.is_connected or not self.master:
            print(f"[SYMULACJA MAVLink] Komenda syreny: {'ON (118dB)' if activate else 'OFF'}")
            return True

        pwm_value = 2000 if activate else 1000
        # Ustawienie wyjścia serwa nr 9 (AUX 1 na kontrolerze lotu)
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0,
            9, # Numer serwa (AUX 1)
            pwm_value,
            0, 0, 0, 0, 0
        )
        print(f"[MAVLink] Przesłano sygnał sterujący do syreny: PWM={pwm_value}")
        return True

    def pause_mission(self, pause: bool = True) -> bool:
        """
        Wstrzymuje (zawis w miejscu) lub wznawia lot po siatce polowej.
        """
        if not self.is_connected or not self.master:
            print(f"[SYMULACJA MAVLink] Misja: {'PAUSED (Zawis nad celem)' if pause else 'RESUMED (Wznowienie)'}")
            return True

        param2 = 0 if pause else 1 # 0 = pause, 1 = resume
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_DO_PAUSE_CONTINUE,
            0,
            0, param2, 0, 0, 0, 0, 0
        )
        return True

    def return_to_launch(self) -> bool:
        """Awaryjny powrót drona do miejsca startu i lądowanie (RTL)."""
        if not self.is_connected or not self.master:
            print("[SYMULACJA MAVLink] Awaryjna procedura: RETURN TO LAUNCH (RTL)!")
            return True

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        return True


if __name__ == "__main__":
    bridge = AgroMavlinkBridge()
    print("Test działania modułu AgroMavlinkBridge:")
    # Demonstracja symulacyjna bez fizycznego podłączenia drona
    bridge.trigger_deterrence_siren(True)
    time.sleep(1)
    bridge.trigger_deterrence_siren(False)
    bridge.pause_mission(True)
    bridge.return_to_launch()

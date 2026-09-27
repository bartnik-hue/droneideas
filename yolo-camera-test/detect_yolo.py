"""
URSUS AI - Detekcja YOLO na żywo z wyborem kamery przy starcie (PS Eye / OBS Virtual Camera).
Obsługa akceleracji sprzętowej NVIDIA CUDA (GeForce RTX 4070 Ti).
"""
import sys
import os
import time
from pathlib import Path
import cv2
import torch
from ultralytics import YOLO

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Wyciszenie ostrzeżeń backendu OpenCV przy skanowaniu
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
try:
    cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_SILENT)
except Exception:
    pass

def try_open_pseyepy():
    """Próba bezpośredniego otwarcia kamery PS Eye przez sterownik open-driver (libusb)."""
    try:
        import pseyepy
        cam = pseyepy.Camera(resolution=pseyepy.Camera.RES_LARGE, fps=60)
        frame, _ = cam.read()
        if frame is not None and frame.size > 0:
            return cam
        cam.end()
    except Exception as e:
        print(f"[INFO] pseyepy niedostępny lub błąd: {e}")
    return None

def select_camera_source():
    """Menu wyboru źródła wideo przy starcie programu."""
    # 1. Sprawdzenie czy użytkownik podał kamerę w argumentach CLI (np. --cam 4 lub --cam pseye)
    for i, arg in enumerate(sys.argv):
        if arg in ["--cam", "-c"] and i + 1 < len(sys.argv):
            target = sys.argv[i + 1].lower()
            if target in ["pseye", "ps3eye", "usb", "open"]:
                c = try_open_pseyepy()
                if c:
                    return "pseyepy", c, "Sony PS Eye USB (Open Driver libusb - 60 FPS)"
            else:
                try:
                    idx = int(target)
                    cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                    if cap.isOpened():
                        return "dshow", cap, f"Kamera DirectShow ID {idx}"
                except ValueError:
                    pass

    print("\n" + "=" * 70)
    print("                     WYBÓR ŹRÓDŁA WIDEO / KAMERY")
    print("=" * 70)

    available = []

    # Skanowanie PS Eye (Open Driver libusb)
    pseye_ok = False
    try:
        import pseyepy
        c = pseyepy.Camera(resolution=pseyepy.Camera.RES_LARGE, fps=60)
        c.end()
        pseye_ok = True
    except Exception:
        pass

    if pseye_ok:
        available.append({
            "type": "pseyepy",
            "name": "Sony PS Eye USB (Open Driver libusb - 60 FPS)",
            "id": "pseye"
        })

    # Skanowanie kamer DirectShow
    for idx in range(8):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w = frame.shape[:2]
                cam_label = "OBS Virtual Camera" if idx == 4 else f"Kamera ID {idx}"
                available.append({
                    "type": "dshow",
                    "name": f"{cam_label} (DirectShow - {w}x{h})",
                    "id": idx
                })
            cap.release()

    if not available:
        print("[OSTRZEŻENIE] Nie wykryto automatycznie żadnej aktywnej kamery.")
        manual_id = 0
        try:
            val = input("Wpisz numer ID kamery do otwarcia (np. 0 lub 4) [domyślnie 4]: ").strip()
            manual_id = int(val) if val else 4
        except ValueError:
            manual_id = 4
        cap = cv2.VideoCapture(manual_id, cv2.CAP_DSHOW)
        return "dshow", cap, f"Kamera ID {manual_id}"

    # Wyświetlenie ponumerowanej listy
    for num, item in enumerate(available, 1):
        rec = " (Domyślna)" if num == 1 else ""
        print(f"  [{num}] {item['name']}{rec}")

    manual_opt = len(available) + 1
    print(f"  [{manual_opt}] Wpisz inny indeks kamery ręcznie...")
    print("=" * 70)

    # Pobranie wyboru
    chosen = available[0]
    try:
        prompt = f"Wybierz numer kamery [1-{manual_opt}] (Enter = 1): "
        user_input = input(prompt).strip()
        if user_input:
            num = int(user_input)
            if 1 <= num <= len(available):
                chosen = available[num - 1]
            elif num == manual_opt:
                man_val = input("Podaj numer indeksu kamery DirectShow (np. 0, 1, 2...): ").strip()
                mid = int(man_val) if man_val else 0
                cap = cv2.VideoCapture(mid, cv2.CAP_DSHOW)
                if not cap.isOpened():
                    cap = cv2.VideoCapture(mid)
                return "dshow", cap, f"Kamera DirectShow ID {mid}"
    except (ValueError, EOFError, KeyboardInterrupt):
        chosen = available[0]

    print(f"\n[URUCHAMIANIE] Wybrano źródło: {chosen['name']}\n")

    if chosen["type"] == "pseyepy":
        c = try_open_pseyepy()
        return "pseyepy", c, chosen["name"]
    else:
        cap = cv2.VideoCapture(chosen["id"], cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(chosen["id"])
        return "dshow", cap, chosen["name"]

def main():
    print("=" * 70)
    print("          URSUS AI - DETEKCJA YOLO Z KAMERKI NA ŻYWO")
    print("=" * 70)

    # 1. Sprawdzenie sprzętu (GPU / CUDA)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    if device.startswith("cuda"):
        gpu_name = torch.cuda.get_device_name(0)
        print(f"[SPRZĘT] Akceleracja GPU aktywna: {gpu_name} (CUDA)")
    else:
        print("[SPRZĘT] Obliczenia na procesorze (CPU)")

    # 2. Załadowanie modelu YOLO
    model_name = "yolo11n.pt"
    # Sprawdzenie czy podano model w argumentach lub czy istnieje wytrenowany best.pt
    for arg in sys.argv[1:]:
        if arg.endswith(".pt") or arg.endswith(".onnx"):
            model_name = arg
            break
    else:
        custom_weights = Path("runs_custom/animal_detector/weights/best.pt")
        if custom_weights.exists():
            print(f"[MODEL] Wykryto własny wytrenowany model: {custom_weights}")
            model_name = str(custom_weights)

    print(f"[MODEL] Ładowanie modelu {model_name}...")
    try:
        model = YOLO(model_name)
    except Exception:
        model_name = "yolov8n.pt"
        model = YOLO(model_name)
    print(f"[MODEL] Model {model_name} załadowany pomyślnie.")

    # 3. Interaktywny wybór kamery przy starcie
    cam_type, cap_obj, cam_source_name = select_camera_source()

    if cap_obj is None or (cam_type == "dshow" and not cap_obj.isOpened()):
        print("\n[BŁĄD] Nie udało się otworzyć wybranej kamery!")
        input("Naciśnij Enter, aby zamknąć...")
        return

    # 4. Inicjalizacja Wirtualnej Kamery (pyvirtualcam -> OBS Virtual Camera)
    vcam = None
    try:
        import pyvirtualcam
        vcam = pyvirtualcam.Camera(width=640, height=480, fps=60, fmt=pyvirtualcam.PixelFormat.BGR)
        print(f"[WIRTUALNA KAMERA] Nadawanie aktywne: {vcam.device} (gotowe do odbioru np. w Discord/OBS)")
    except Exception as e:
        print(f"[WIRTUALNA KAMERA] Brak aktywnej wirtualnej kamery ({e}). Podgląd będzie dostępny w oknie.")

    # Parametry detekcji
    conf_thresh = 0.40
    snapshots_dir = Path("snapshots")
    snapshots_dir.mkdir(exist_ok=True)

    print("\n" + "-" * 70)
    print("KLAWISZE STERUJĄCE W OKNIE PODGLĄDU:")
    print("  [q] lub [ESC] - Zakończenie działania programu")
    print("  [s]           - Zapisanie zrzutu ekranu do snapshots/")
    print("  [+] / [-]     - Zwiększenie / zmniejszenie progu pewności detekcji (conf)")
    print("-" * 70 + "\n")

    window_name = f"URSUS AI - Detekcja na żywo [{device}]"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 960, 720)

    fps = 0.0
    prev_time = time.time()

    try:
        while True:
            # Pobranie klatki w zależności od typu kamery
            if cam_type == "pseyepy":
                frame, _ = cap_obj.read()
            else:
                ret, frame = cap_obj.read()
                if not ret:
                    time.sleep(0.01)
                    continue

            if frame is None or frame.size == 0:
                continue

            # Obliczenie FPS
            curr_time = time.time()
            time_diff = curr_time - prev_time
            if time_diff > 0:
                fps = 0.9 * fps + 0.1 * (1.0 / time_diff) if fps > 0 else (1.0 / time_diff)
            prev_time = curr_time

            # Inferencja YOLO z akceleracją GPU
            results = model.predict(
                source=frame,
                device=device,
                conf=conf_thresh,
                verbose=False
            )

            # Rysowanie detekcji na klatce
            annotated_frame = results[0].plot()

            # Zliczanie wykrytych obiektów
            boxes = results[0].boxes
            detections_count = len(boxes) if boxes is not None else 0

            # Przesyłanie do Wirtualnej Kamery (jeśli aktywna)
            if vcam is not None:
                try:
                    vcam.send(annotated_frame)
                except Exception:
                    pass

            # Nakładka OSD na podgląd
            overlay = annotated_frame.copy()
            cv2.rectangle(overlay, (10, 10), (450, 110), (15, 15, 15), -1)
            cv2.addWeighted(overlay, 0.75, annotated_frame, 0.25, 0, annotated_frame)

            cv2.putText(annotated_frame, f"FPS: {fps:5.1f} | Model: {model_name}", (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"GPU: {gpu_name if 'cuda' in device else 'CPU'} (CUDA)", (20, 58),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(annotated_frame, f"Prog conf: {conf_thresh:.2f} (+/-) | Wykryto: {detections_count}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 255), 1)
            cv2.putText(annotated_frame, f"Zrodlo: {cam_source_name[:35]}", (20, 102),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

            cv2.imshow(window_name, annotated_frame)

            # Sprawdzenie zamknięcia okna krzyżykiem
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

            # Obsługa klawiszy
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q'), 27]:
                break
            elif key == ord('s'):
                snap_path = snapshots_dir / f"detection_{int(time.time())}.jpg"
                cv2.imwrite(str(snap_path), annotated_frame)
                print(f"[ZAPISANO] Zrzut ekranu: {snap_path}")
            elif key in [ord('+'), ord('=')]:
                conf_thresh = min(0.95, conf_thresh + 0.05)
                print(f"[USTAWIENIE] Próg pewności: {conf_thresh:.2f}")
            elif key in [ord('-'), ord('_')]:
                conf_thresh = max(0.05, conf_thresh - 0.05)
                print(f"[USTAWIENIE] Próg pewności: {conf_thresh:.2f}")

    except KeyboardInterrupt:
        print("\n[ZATRZYMANO] Przerwano przez użytkownika.")
    finally:
        if cam_type == "pseyepy" and cap_obj is not None:
            try:
                cap_obj.end()
            except Exception:
                pass
        elif cap_obj is not None:
            cap_obj.release()
        if vcam is not None:
            try:
                vcam.close()
            except Exception:
                pass
        cv2.destroyAllWindows()
        print("[KONIEC] Zwolniono zasoby i zakończono działanie.")

if __name__ == "__main__":
    main()

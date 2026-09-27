"""
Narzędzie do skanowania i testowania dostępnych kamer w systemie Windows.
"""
import sys
import cv2

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def scan_cameras(max_tested=10):
    print("=" * 60)
    print("Skanowanie dostępnych kamer (DirectShow & Domyślne)...")
    print("=" * 60)
    
    found = []
    
    for idx in range(max_tested):
        # Najpierw sprawdzamy DirectShow (najczęstszy dla kamer wirtualnych i USB)
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w, c = frame.shape
                fps = cap.get(cv2.CAP_PROP_FPS)
                print(f"[OK] Kamera ID {idx} (CAP_DSHOW): {w}x{h} @ {fps:.1f} FPS")
                found.append((idx, "CAP_DSHOW", w, h))
            cap.release()
            continue
            
        # Alternatywnie domyślny backend
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w, c = frame.shape
                fps = cap.get(cv2.CAP_PROP_FPS)
                print(f"[OK] Kamera ID {idx} (DEFAULT): {w}x{h} @ {fps:.1f} FPS")
                found.append((idx, "DEFAULT", w, h))
            cap.release()

    print("=" * 60)
    if not found:
        print("Nie znaleziono żadnej aktywnej kamery.")
        print("Wskazówka: Jeśli używasz OBS Virtual Camera, upewnij się, że w OBS Studio kliknięto 'Uruchom kamerę wirtualną'.")
    else:
        print(f"Znaleziono łącznie kamer: {len(found)}")
    print("=" * 60)
    return found

if __name__ == "__main__":
    scan_cameras()

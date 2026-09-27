"""
URSUS AI - Skrypt do trenowania własnego modelu YOLO (np. rozpoznawanie zwierząt).
Wykorzystuje kartę graficzną NVIDIA GeForce RTX 4070 Ti (CUDA).
"""
import sys
from pathlib import Path
import torch
from ultralytics import YOLO

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def train():
    print("=" * 70)
    print("        URSUS AI - TRENING WŁASNEGO MODELU YOLO")
    print("=" * 70)

    # 1. Sprawdzenie akceleracji GPU
    if not torch.cuda.is_available():
        print("[OSTRZEŻENIE] Brak aktywnego CUDA! Trening na CPU będzie bardzo powolny.")
        device = "cpu"
    else:
        gpu_name = torch.cuda.get_device_name(0)
        print(f"[SPRZĘT] Karta graficzna do treningu: {gpu_name} (CUDA 0)")
        device = 0

    # 2. Ścieżka do konfiguracji zbioru danych
    data_yaml = Path("dataset/data.yaml")
    if not data_yaml.exists():
        print(f"\n[BŁĄD] Nie znaleziono pliku: {data_yaml.resolve()}")
        print("\nAby rozpocząć trening, przygotuj zbiór danych:")
        print(" 1. Utwórz folder 'dataset' z podziałem na train/ oraz val/.")
        print(" 2. Przygotuj plik 'dataset/data.yaml' (zobacz szablon data.yaml.template).")
        print(" 3. Wyeksportuj oznaczone zdjęcia np. z Roboflow lub CVAT w formacie YOLOv8/YOLO11.")
        return

    # 3. Wybór modelu bazowego (Transfer Learning)
    # yolo11n (nano) - najszybszy, idealny na początek
    # yolo11s (small) - dokładniejszy, bez problemu mieści się w 12GB VRAM RTX 4070 Ti
    base_model = "yolo11n.pt"
    print(f"\n[START] Ładowanie wag bazowych: {base_model}...")
    model = YOLO(base_model)

    # 4. Parametry treningu
    epochs = 50       # 50-100 epok zazwyczaj w zupełności wystarcza
    imgsz = 640       # Standardowa rozdzielczość wejściowa sieci
    batch_size = 16   # Rozmiar partii (RTX 4070 Ti bez trudu udźwignie 16 lub 32)

    print(f"[TRENING] Rozpoczynanie treningu: {epochs} epok, batch={batch_size}, imgsz={imgsz}...")

    results = model.train(
        data=str(data_yaml.resolve()),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch_size,
        device=device,
        project="runs_custom",
        name="animal_detector",
        save=True,
        plots=True,
        workers=4
    )

    print("\n" + "=" * 70)
    print("TRENING ZAKOŃCZONY SUKCESEM!")
    print("Wytrenowany model został zapisany w:")
    print("  runs_custom/animal_detector/weights/best.pt")
    print("\nAby uruchomić detekcję na żywo z Twoim nowym modelem:")
    print("  python detect_yolo.py runs_custom/animal_detector/weights/best.pt")
    print("=" * 70)

if __name__ == "__main__":
    train()

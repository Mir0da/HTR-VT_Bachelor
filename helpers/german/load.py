from datasets import load_dataset
from pathlib import Path

# Zielordner
output_path = Path("C:/Users/SRLab-ML1/Documents/GitHub/HTR-VT_Bachelor/data/german/lines")
output_path.mkdir(parents=True, exist_ok=True)

# Lade und mische Datensatz
dataset = load_dataset("fhswf/german_handwriting", split="train").shuffle(seed=42)

skipped = 0

for idx, sample in enumerate(dataset):
    image = sample["image"]
    text = sample["text"]

    if text is None or not text.strip():
        skipped += 1
        continue

    image_id = f"{idx:05d}"

    image.save(output_path / f"{image_id}.png")
    with open(output_path / f"{image_id}.txt", "w", encoding="utf-8") as f:
        f.write(text.strip())

print(f"✅ {len(dataset) - skipped} Beispiele gespeichert, {skipped} übersprungen (leerer Text).")

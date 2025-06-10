from pathlib import Path
import pandas as pd
import shutil

# 🔁 Anpassen:
CSV_PATH = Path("C:/Users/User/Documents/GitHub/HTR-VT_Bachelor/data/iam/ascii/iam_linesUNI2.csv")  # deine CSV mit Bildpfad + Text
DEST_FOLDER = Path("/data/iam/lines")  # hierhin sollen die Bilder kopiert werden

DEST_FOLDER.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV_PATH)

for _, row in df.iterrows():
    source_path = Path(row["path"])
    if not source_path.is_file():
        print(f"⚠️ Bild nicht gefunden: {source_path}")
        continue

    dest_file = DEST_FOLDER / source_path.name
    shutil.copy2(source_path, dest_file)

print("✅ Alle Bilder kopiert.")


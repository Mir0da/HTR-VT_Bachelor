from pathlib import Path
import pandas as pd

# 🔁 Anpassen:
CSV_PATH = Path("C:/Users/User/Documents/GitHub/HTR-VT_Bachelor/data/iam/ascii/iam_linesUNI2.csv")
TXT_FOLDER = Path("/data/iam/lines")  # gleiche wie für die Bilder

TXT_FOLDER.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV_PATH)

for _, row in df.iterrows():
    image_path = Path(row["path"])
    image_name = image_path.stem  # z. B. a01-000u-00
    text = str(row["text"])

    txt_file = TXT_FOLDER / f"{image_name}.txt"
    with txt_file.open("w", encoding="utf-8") as f:
        f.write(text)

print("✅ Alle .txt-Dateien erstellt.")

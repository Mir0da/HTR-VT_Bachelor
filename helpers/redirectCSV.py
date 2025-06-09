from pathlib import Path
import pandas as pd

# 🔁 Anpassen:
OLD_ROOT = "C:\\Users\\SRLab-ML1\\Documents\\BACHERLOR_zach\\GitHub\\HTR-VT\\data\\iam\\lines\\"
NEW_ROOT = "C:\\Users\\sophi\\Documents\\GitHub\\HTR-VT_Bachelor\\data\\iam\\lines\\"  # → dein aktueller lines-Ordner
CSV_PATH = Path("C:/Users/sophi/Documents/GitHub/HTR-VT_Bachelor/data/iam/ascii/iam_linesUNI.csv")

df = pd.read_csv(CSV_PATH)

# Ersetze nur den Root-Pfad
df["path"] = df["path"].str.replace(OLD_ROOT, NEW_ROOT, regex=False)

# Neue Datei speichern (optional)
UPDATED_CSV = CSV_PATH.parent / "iam_lines_updated.csv"
df.to_csv(UPDATED_CSV, index=False)

print(f"✅ CSV mit neuen Pfaden gespeichert: {UPDATED_CSV}")

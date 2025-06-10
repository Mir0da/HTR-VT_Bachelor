from pathlib import Path
import random

# 🔁 Anpassen:
lines_dir = Path("C:/Users/User/Documents/GitHub/HTR-VT_Bachelor/data/german/lines")
output_dir = lines_dir.parent  # schreibt .ln-Dateien nach /german/

# Alle PNG-Dateien sammeln
all_images = list(lines_dir.glob("*.png"))
random.shuffle(all_images)

# Aufteilen
n_total = len(all_images)
n_val = int(n_total * 0.1)
n_test = int(n_total * 0.1)

val = all_images[:n_val]
test = all_images[n_val:n_val + n_test]
train = all_images[n_val + n_test:]

# Schreibe .ln-Dateien
def write_ln_file(name, entries):
    with open(output_dir / f"{name}.ln", "w", encoding="utf-8") as f:
        for path in entries:
            f.write(path.name + "\n")

write_ln_file("train", train)
write_ln_file("val", val)
write_ln_file("test", test)

print(f"✅ Split abgeschlossen: {len(train)} train, {len(val)} val, {len(test)} test")

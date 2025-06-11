from pathlib import Path
all_chars = set()

for txt in Path("C:/Users/SRLab-ML1/Documents/GitHub/HTR-VT_Bachelor/data/german/lines").glob("*.txt"):
    text = txt.read_text(encoding="utf-8")
    all_chars.update(text)

charset = sorted(all_chars)
print("✅ Charset ({} Zeichen):".format(len(charset)))
print("".join(charset))
print("Länge:",len(charset))

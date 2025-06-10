from pathlib import Path
all_chars = set()

for txt in Path("C:/Users/sophi/PycharmProjects/prepareGermanDataset/data/lines").glob("*.txt"):
    text = txt.read_text(encoding="utf-8")
    all_chars.update(text)

charset = sorted(all_chars)
print("✅ Charset ({} Zeichen):".format(len(charset)))
print("".join(charset))

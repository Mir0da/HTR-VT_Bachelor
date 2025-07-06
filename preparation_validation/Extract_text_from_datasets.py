import os
import shutil
from datasets import load_dataset
import pandas as pd

os.environ['HF_DATASETS_CACHE'] = os.path.abspath("./cache/hf_datasets")

cache_path = os.path.abspath("./cache/hf_datasets")
if os.path.exists(cache_path):
    shutil.rmtree(cache_path)
    print("Local HF-Datasets-Cache deleted.")

# load Dataset
dataset = load_dataset('fhswf/german_handwriting', split='train', cache_dir='./cache/hf_datasets', download_mode='force_redownload')


# extract transkriptions
texts = []
for entry in dataset:
    if 'text' in entry and isinstance(entry['text'], str):
        texts.append(entry['text'])

# ensure save Path
save_path = 'output/german_handwriting_transcriptions.txt'
os.makedirs(os.path.dirname(save_path), exist_ok=True)


# save texts
with open(save_path, 'w', encoding='utf-8') as f:
    for line in texts:
        f.write(line.strip() + '\n')

print(f"{len(texts)} transkriptions from fhswf/german_handwriting saved in '{save_path}'")



# # IAM Handwriting Dataset

file_path = "../data/iam/ascii/words.txt"


words = []
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) >= 9 and parts[1] == 'ok':
            word = parts[-1]
            words.append(word)


print(f"Total extracted words from IAM: {len(words)}")

# save transcriptions
output_path = "output/iam_handwriting_transcriptions.txt"
with open(output_path, "w", encoding="utf-8") as out_file:
    for word in words:
        out_file.write(word.strip() + "\n")

print(f"Transcriptions saved in '{output_path}'.")


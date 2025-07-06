import pandas as pd
import ast
from collections import Counter

def load_ngram_dict(csv_path):
    df = pd.read_csv(csv_path)
    return {row["ngram"]: row["category"] for _, row in df.iterrows()}

def extract_ngrams_around_diffs(truth, diffs, n, ngram_dict):
    error_ngrams = set()
    for diff in diffs:
        _, _, _, truth_start, truth_end = diff
        for pos in range(truth_start - n + 1, truth_end):
            if 0 <= pos <= len(truth) - n:
                ngram = truth[pos:pos+n]
                if ngram in ngram_dict:
                    error_ngrams.add((ngram, ngram_dict[ngram]))
    return list(error_ngrams)

def tag_ngrams(aligned_csv_path, ngram_dict, n=2):
    df = pd.read_csv(aligned_csv_path)
    tagged = []

    for _, row in df.iterrows():
        truth = str(row["ground_truth"])
        pred = str(row["prediction"])
        diffs = ast.literal_eval(row["diff_ops"])  # Liste mit ('replace', i1, i2, j1, j2)

        found_ngrams = []

        for op, i1, i2, j1, j2 in diffs:
            for start in range(max(0, i1 - n + 1), min(len(truth) - n + 1, i2)):
                ngram = truth[start:start + n]
                if ngram in ngram_dict:
                    found_ngrams.append((ngram, ngram_dict[ngram]))

        # Optional: eindeutige Treffer extrahieren (nicht doppelt zählen)
        found_ngrams = list(Counter(found_ngrams).items())

        tagged.append({
            "prediction": pred,
            "ground_truth": truth,
            "diff_ops": row["diff_ops"],
            "error_ngrams": found_ngrams
        })

    return pd.DataFrame(tagged)

if __name__ == "__main__":
    aligned_path = "output/aligned_predictions.csv"
    ngram_csv = "../../preparation_validation/output/ngram_analysis_2gram.csv"
    output_path = "output/tagged_bigram_errors.csv"

    ngram_dict = load_ngram_dict(ngram_csv)
    tagged_df = tag_ngrams(aligned_path, ngram_dict, n=2) #carefull to also change n!
    tagged_df.to_csv(output_path, index=False)
    print(f"✔ Tagged n-gram errors saved to: {output_path}")


"""
* Calculate CER and WER (locally via editdistance)

* Aggregate results in two tables:

* Absolute error rates

* Difference between languages

* Visualize comparison results with bar charts

* Save as a PNG file
"""

import pandas as pd
import matplotlib.pyplot as plt
import editdistance
import os

# ===  Datapaths ===
csv_files = {
    "english on english": "../saved_models/english/predictions_vs_groundtruth_EoE.csv",
    "english on german": "../saved_models/english/predictions_vs_groundtruth_EoG.csv",
    "german on german": "../saved_models/german/predictions_vs_groundtruth_GoG.csv",
    "german on english": "../saved_models/german/predictions_vs_groundtruth_GoE.csv",
    "english_fullset on english": "../saved_models/english_fullset/predictions_vs_groundtruth_EFoE.csv",
    "english_fullset on german": "../saved_models/english_fullset/predictions_vs_groundtruth_EFoG.csv"
}

# === CER- und WER-Calculation ===
def compute_error_rates(df):
    total_char_errors = 0
    total_chars = 0
    total_word_errors = 0
    total_words = 0

    for _, row in df.iterrows():
        gt = str(row["ground_truth"]).strip()
        pred = str(row["prediction"]).strip()

        # CER
        total_char_errors += editdistance.eval(gt, pred)
        total_chars += len(gt)

        # WER
        gt_words = gt.split()
        pred_words = pred.split()
        total_word_errors += editdistance.eval(gt_words, pred_words)
        total_words += len(gt_words)

    cer = total_char_errors / total_chars if total_chars > 0 else float("nan")
    wer = total_word_errors / total_words if total_words > 0 else float("nan")
    return round(cer, 4), round(wer, 4)

# === Evaluate all results ===
results = {}
for label, path in csv_files.items():
    if not os.path.exists(path):
        print(f"⚠️  File not found: {path}")
        continue
    df = pd.read_csv(path)
    cer, wer = compute_error_rates(df)
    results[label] = {"CER": cer, "WER": wer}

# === Table: Absolute values ===
df_results = pd.DataFrame(results).T
df_results.index.name = "Evaluation"
print("\n📊 Absolute error values:")
print(df_results)

# === Table: Difference between language ===
diff_table = pd.DataFrame({
    "Δ CER": {
        "english": df_results.loc["english on german", "CER"] - df_results.loc["english on english", "CER"],
        "german": df_results.loc["german on english", "CER"] - df_results.loc["german on german", "CER"],
        "english_fullset": df_results.loc["english_fullset on german", "CER"] - df_results.loc["english_fullset on english", "CER"]
    },
    "Δ WER": {
        "english": df_results.loc["english on german", "WER"] - df_results.loc["english on english", "WER"],
        "german": df_results.loc["german on english", "WER"] - df_results.loc["german on german", "WER"],
        "english_fullset": df_results.loc["english_fullset on german", "WER"] - df_results.loc["english_fullset on english", "WER"]
    }
})
print("\n📉 Performance losses when changing languages:")
print(diff_table)

# === Plot ===
plt.figure(figsize=(10, 6))
df_results[["CER", "WER"]].plot.bar(rot=30)
plt.title("Evaluation of HTR Models on In- and Cross-Language Test Sets")
plt.ylabel("Error Rate")
plt.ylim(0, 1)
plt.tight_layout()
plt.grid(True, axis="y", linestyle="--", linewidth=0.5)
plt.savefig("htr_model_comparison.png")


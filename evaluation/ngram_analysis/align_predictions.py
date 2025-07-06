# align_predictions.py
import pandas as pd
import difflib
import os

def compute_diff_ops(prediction, ground_truth):
    sm = difflib.SequenceMatcher(None, prediction, ground_truth)
    ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
    return ops

def align_predictions(csv_path, output_path):
    df = pd.read_csv(csv_path)
    rows = []

    for _, row in df.iterrows():
        pred = str(row["prediction"])
        truth = str(row["ground_truth"])
        diff_ops = compute_diff_ops(pred, truth)

        rows.append({
            "prediction": pred,
            "ground_truth": truth,
            "diff_ops": diff_ops
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    input_path = "example_predictions_vs_groundtruth.csv"  # Path to example file
    output_path = "output/aligned_predictions.csv"
    os.makedirs("output", exist_ok=True)

    align_predictions(input_path, output_path)
    print(f"✔ Aligned predictions saved to: {output_path}")


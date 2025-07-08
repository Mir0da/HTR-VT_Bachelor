import pandas as pd
from collections import Counter, defaultdict
import ast


def summarize_ngram_errors(tagged_csv_path, output_csv_path=None):
    df = pd.read_csv(tagged_csv_path)

    total_samples = len(df)
    error_counts = defaultdict(int)
    sample_counts = defaultdict(int)

    for _, row in df.iterrows():
        try:
            tagged = ast.literal_eval(row["error_ngrams"])
        except Exception:
            tagged = []

        seen_categories = set()

        for (ngram, category), count in tagged:
            error_counts[category] += count
            seen_categories.add(category)

        for category in seen_categories:
            sample_counts[category] += 1

    total_errors = sum(error_counts.values())
    summary = []

    for category in sorted(set(list(error_counts.keys()) + list(sample_counts.keys()))):
        errors = error_counts[category]
        samples = sample_counts[category]
        freq = (errors / total_errors * 100) if total_errors > 0 else 0
        summary.append({
            "category": category,
            "total_errors": errors,
            "affected_samples": samples,
            "relative_frequency (%)": round(freq, 2)
        })

    summary_df = pd.DataFrame(summary)
    if output_csv_path:
        summary_df.to_csv(output_csv_path, index=False)

    return summary_df


if __name__ == "__main__":
    input_path = "output/tagged_trigram_errors_GoE.csv"
    output_path = "output/summary_trigram_errors_GoE.csv"

    summary_df = summarize_ngram_errors(input_path, output_path)
    print(summary_df)

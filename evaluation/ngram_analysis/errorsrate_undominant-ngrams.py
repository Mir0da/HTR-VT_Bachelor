import pandas as pd
import ast
from collections import Counter

def compute_ngram_error_rate_with_ground_truth(
    error_csv_path: str,
    ngram_category_path: str,
    n: int = 2,
    output_path: str = None
) -> pd.DataFrame:
    """
    Calculates the error rate for n-grams based on:
    - a CSV file with previously tagged errors (e.g., output of tag_ngram_errors.py)
    - a complete category scheme from the n-gram frequency analysis

    Args:
    error_csv_path (str): Path to the CSV file with columns 'ground_truth' and 'error_ngrams'
    ngram_category_path (str): CSV file with columns 'ngram' and 'category'
    n (int): N-gram length (e.g., 2 or 3)
    output_path (str, optional): Optional path to save as CSV

    Returns:
    pd.DataFrame: Table with ngram, category, total_count, error_count, error_rate
    """

    # Lade die benötigten Dateien
    df = pd.read_csv(error_csv_path)
    cat_df = pd.read_csv(ngram_category_path)
    ngram_to_cat = dict(zip(cat_df["ngram"], cat_df["category"]))

    # Fehlerhafte N-Gramme extrahieren und zählen
    error_counter = Counter()
    for entry in df["error_ngrams"].dropna():
        try:
            parsed = ast.literal_eval(entry)
            for (ngram, category), _ in parsed:
                error_counter[ngram] += 1
        except Exception:
            continue

    # Alle N-Gramme im Ground Truth extrahieren
    total_counter = Counter()
    for gt in df["ground_truth"].dropna():
        text = str(gt)
        for i in range(len(text) - n + 1):
            ngram = text[i:i + n]
            if ngram in ngram_to_cat:
                total_counter[ngram] += 1

    # Zusammenführen und Fehlerrate berechnen
    rows = []
    for ngram, total_count in total_counter.items():
        error_count = error_counter.get(ngram, 0)
        error_rate = error_count / total_count if total_count > 0 else 0
        category = ngram_to_cat.get(ngram, "unknown")
        rows.append({
            "ngram": ngram,
            "category": category,
            "total_count": total_count,
            "error_count": error_count,
            "error_rate": round(error_rate, 4)
        })

    result_df = pd.DataFrame(rows).sort_values(by="error_rate", ascending=False)

    if output_path:
        result_df.to_csv(output_path, index=False)
        print(f"Wrote {output_path}")

    return result_df

def summarize_error_rates_by_category(ngram_stats_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates average and median error rates per category.

    Arguments:
    ngram_stats_df(pd.DataFrame): DataFrame with columns: ngram, category, error_rate

    Returns:
    pd.DataFrame: Category statistics with mean_error_rate and median_error_rate
    """
    summary = ngram_stats_df.groupby("category")["error_rate"].agg(
        mean_error_rate="mean",
        median_error_rate="median",
        number_of_ngrams="count"
    ).reset_index()

    return summary.sort_values(by="mean_error_rate", ascending=False)


df_stats = compute_ngram_error_rate_with_ground_truth("./output/tagged_trigram_errors_EoG.csv", "../../preparation_validation/output/ngram_analysis_3gram.csv", n=3, output_path="./output/errorrate_trigram_EoG.csv")
df_summary = summarize_error_rates_by_category(df_stats)
df_summary.to_csv("./output/errorrate_summary_trigram_EoG.csv", index=False)
print(df_summary)



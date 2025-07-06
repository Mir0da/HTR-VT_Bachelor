import csv

def load_ngram_frequencies(filepath, sep="\t"):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    freq_dict = {}
    for line in lines:
        parts = line.strip().split(sep)
        if len(parts) != 2:
            continue
        ngram = parts[0].lower()
        try:
            freq = int(parts[1])
            freq_dict[ngram] = freq
        except ValueError:
            continue
    return freq_dict

def compute_ranks(freq_dict):
    # Sort descending by frequency and assign rank
    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    return {ngram: rank + 1 for rank, (ngram, _) in enumerate(sorted_items)}

def load_reference_frequencies(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    freq_dict = {}
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        ngram = parts[0].lower()
        try:
            freq = int(parts[1])
            freq_dict[ngram] = freq
        except ValueError:
            continue
    return freq_dict

def compare_ngram_ranks(your_file, reference_file, output_csv, sep="\t"):
    your_freqs = load_ngram_frequencies(your_file, sep=sep)
    ref_freqs = load_reference_frequencies(reference_file)

    your_ranks = compute_ranks(your_freqs)
    ref_ranks = compute_ranks(ref_freqs)

    results = []

    for ngram in list(your_ranks.keys())[:100]:  # only top 100 of your file
        your_rank = your_ranks[ngram]
        ref_rank = ref_ranks.get(ngram)
        if ref_rank is not None:
            diff = your_rank - ref_rank
            results.append([ngram, your_rank, ref_rank, diff])
        else:
            results.append([ngram, your_rank, "n/a", "–"])


    # Export to CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ngram", "your_rank", "ref_rank", "rank_diff"])
        writer.writerows(results)

    print(f"\nCSV exported to: {output_csv}")


#bigram german
compare_ngram_ranks(
    your_file="output/top100_bigrams_de.txt",
    reference_file="practicalCryptographyData/german_bigrams.txt",
    output_csv="output/ranking_bigramm_diff_de.csv"
)

#trigram german
compare_ngram_ranks(
    your_file="output/top100_trigrams_de.txt",
    reference_file="practicalCryptographyData/german_trigrams.txt",
    output_csv="output/ranking_trigramm_diff_de.csv"
)

#bigram english
compare_ngram_ranks(
    your_file="output/top100_bigrams_en.txt",
    reference_file="practicalCryptographyData/english_bigrams.txt",
    output_csv="output/ranking_bigramm_diff_en.csv"
)

#trigram english
compare_ngram_ranks(
    your_file="output/top100_trigrams_en.txt",
    reference_file="practicalCryptographyData/english_trigrams.txt",
    output_csv="output/ranking_trigramm_diff_en.csv"
)
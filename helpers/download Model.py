from huggingface_hub import hf_hub_download

# Beispiel für best_CER.pth
hf_hub_download(
    repo_id="Mir0da/HTR-VT-german",
    filename="best_CER.pth",
    local_dir="saved_models/german",
    repo_type="model"
)

# Beispiel für best_WER.pth
hf_hub_download(
    repo_id="Mir0da/HTR-VT-german",
    filename="best_WER.pth",
    local_dir="saved_models/german",
    repo_type="model"
)

from huggingface_hub import hf_hub_download, list_repo_files

# Liste aller Dateien im Repo anzeigen
repo_id = "Mir0da/HTR-VT-german"
local_dir = "../saved_models/german"
repo_type = "model"

# Alle gewünschten Dateien gezielt herunterladen
files_to_download = [
    "best_CER.pth",
    "best_WER.pth",
    "run.log",
]

# Herunterladen der direkt benannten Dateien
for filename in files_to_download:
    hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=local_dir,
        repo_type=repo_type
    )

# Dynamische Suche nach TensorBoard event-Dateien
all_files = list_repo_files(repo_id=repo_id, repo_type=repo_type)
event_files = [f for f in all_files if f.startswith("events.out.tfevents.")]

# Herunterladen aller gefundenen event-Dateien
for event_file in event_files:
    hf_hub_download(
        repo_id=repo_id,
        filename=event_file,
        local_dir=local_dir,
        repo_type=repo_type
    )


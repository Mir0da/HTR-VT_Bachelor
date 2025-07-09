# 📙 HTR-VT - Bachelor

### Introduction
This is the corresponding GitHub of the bachelor thesis "Comparison of language-specific HTR models" by Sophie Zach, Media Systems, HAW Hamburg

The code is based on the work of Li et al.(2024) ["HTR-VT: Handwritten text recognition with vision transformer"](https://arxiv.org/pdf/2409.08573), to be found at this GitHub: https://github.com/YutingLi0606/HTR-VT.


## Table of Content
* [1. Installation](#3-installation)
* [2. Quick Start](#4-quick-start)



## 3. Installation

### 3.1. Environment

This model can be learnt on a **single GPU RTX-4090 24G**
```bash
python -m venv venv
venv\Scripts\activate    	# Windows
source venv/bin/activate   # Linux/macOS

pip install -r requirements_uni.txt --extra-index-url https://download.pytorch.org/whl/cu118
```


### 3.2. Datasets

* Using **IAM, fhswf/german_handwriting** for handwritten text recognition.
  <details>
   <summary>
   IAM
   </summary>

        Register at the FKI's webpage :https://fki.tic.heia-fr.ch/databases/iam-handwriting-database
    
        Download the dataset from here :https://fki.tic.heia-fr.ch/databases/download-the-iam-handwriting-database
    </details>
    <details>
     <summary>
     fhswf/german_handwriting
     </summary>

    Download the dataset from here: https://huggingface.co/datasets/fhswf/german_handwriting using:

        from datasets import load_dataset

        dataset = load_dataset('fhswf/german_handwriting')
  </details>
  
* Download datasets to ./data/.
Take IAM for an example:
The structure of the file should be:

```
./data/iam/
├── train.ln
├── val.ln
├── test.ln
└── lines
      ├──a01-000u-00.png
      ├──a01-000u-00.txt
      ├──a01-000u-01.png
      ├──a01-000u-01.txt
      ...
```


## 4. Quick Start
* The commands used for training are available in ./run/ to train and test on different datasets to help researchers reproducing the results of the paper.

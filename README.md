# Regex Text Preprocessing

![Logo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTF-ufT8Iv0WrSGuzR_JOId0cqGpUrnZ6m4pg&s)

This repository provides a robust, configurable, and extensible text preprocessing engine built in Python. It is tailored for NLP applications, including sentiment analysis, emotion detection, and general dataset cleaning. The library uses advanced regular expressions to deliver fast, reliable, and comprehensive text normalization for machine learning workflows.

<br/>

## ✨ Features
* 18 Preprocessing Steps - Comprehensive text cleaning pipeline
  * URL replacement and preservation
  * Email address handling
  * Date/time normalization
  * Currency and monetary value processing
  * Social media entity expansion (@mentions, #hashtags, $cashtags)
  * HTML tag removal
  * Slang word replacement
  * Contraction expansion
  * Stopword removal (with negation preservation)
  * Title removal (Mr., Dr., etc.)
  * Number and punctuation cleaning
  * Repeated character normalization
* Flexible Configuration - Enable/disable any preprocessing step
* Protection Mechanism - Preserves important entities (URLs, emails) from deletion
* Pre-compiled Regex - Optimized patterns for fast processing
* Batch Processing - Efficiently handles multiple CSV files
* Dictionary Export - Saves replaced entities for reverse mapping

<br/>

## 📚 Documentation

[English Documentation](documents/Preprocessing_Document_English.pdf) \
[Persian Documentation](documents/Preprocessing_Document_Persian.pdf)

<br/>

## 📁 Project Structure
```
📦 Project Root
│
├── 📂 data
│    ├── 📂 processed                      # Output cleaned files
│    │    ├── 📂 maps                      # Saved dictionaries (.pkl files)
│    │    │    ├── 📄 money_dictionary.pkl
│    │    │    ├── 📄 time_dictionary.pkl
│    │    │    └── 📄 urls_dictionary.pkl
│    │    │
│    │    ├── 📜 test_clean.csv
│    │    └── 📜 train_clean.csv
│    │
│    └── 📂 raw                           # Input CSV files
│         ├── 📜 test.csv
│         └── 📜 train.csv
│
├── 📂 documents
│    ├── 📚 Preprocessing_Document - English.pdf
│    └── 📚 Preprocessing_Document - Persian.pdf
│
├── 📂 resources
│    ├── 📊 English_Contractions.json
│    ├── 📊 English_Slang_Dict.json
│    └── 📄 English_Stopwords_without_negatives.txt
│
├── 📂 src
│    ├── 📓 __init__.py
│    ├── 📓 config.py                        # Configuration class
│    └── 📓 preprocessor.py                  # Main preprocessing logic
│
├── 📓 main.py                               # Entry point script
├── 📄 requirements.txt                   # Python dependencies
└── 📄 README.md
```

<br/>

## 🚀 Installation

Prerequisites
* Python 3.7 or higher
* pip package manager

Open your terminal (Command Prompt, PowerShell, or Terminal), navigate to your project folder:

Clone the Repository:
```bash
git clone `this repository`
cd text-preprocessing-regex
```


Install Dependencies (do this once):

```bash
  pip install -r requirements.txt
```

Run the Program:
```bash
  python main.py
```

<br/>

## Required Packages
```bash
pandas>=1.3.0
regex>=2021.8.3
```

<br/>

## 📖 Citation
If you use this project in your research, please cite:
```
@inproceedings{tareh-etal-2025-iasbs,
    title = "{IASBS} at {S}em{E}val-2025 Task 11: Ensembling Transformers for Bridging the Gap in Text-Based Emotion Detection",
    author = "Tareh, Mehrzad  and
      Mohammadzadeh, Erfan  and
      Mohandesi, Aydin  and
      Ansari, Ebrahim",
    editor = "Rosenthal, Sara  and
      Ros{\'a}, Aiala  and
      Ghosh, Debanjan  and
      Zampieri, Marcos",
    booktitle = "Proceedings of the 19th International Workshop on Semantic Evaluation (SemEval-2025)",
    month = jul,
    year = "2025",
    address = "Vienna, Austria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.semeval-1.96/",
    pages = "695--702",
    ISBN = "979-8-89176-273-2",
    abstract = "In this paper, we address the challenges of text-based emotion detection, focusing on multi-label classification, emotion intensity prediction, and cross-lingual emotion detection across various languages. We explore the use of advanced machine learning models, particularly transformers, in three tracks: emotion detection, emotion intensity prediction, and cross-lingual emotion detection. Our approach utilizes pre-trained transformer models, such as Gemini, DeBERTa, M-BERT, and M-DistilBERT, combined with techniques like majority voting and average ensemble voting (AEV) to enhance performance. We also incorporate multilingual strategies and prompt engineering to effectively handle the complexities of emotion detection across diverse linguistic and cultural contexts. Our findings demonstrate the success of ensemble methods and multilingual models in improving the accuracy and generalization of emotion detection, particularly for low-resource languages."
}
```

<br/>

## 📧 Contact
* Erfan Mohammadzadeh
* GitHub: [@e-mohammadzadeh](https://github.com/e-mohammadzadeh)
* LinkedIn: [erfan-mohammadzadeh](https://www.linkedin.com/in/erfan-mohammadzadeh/)

---

⭐ Star this repository if you find it helpful!
Pull requests are welcome!
If you would like to add preprocessing steps, optimize regular expression speed, or enhance documentation, please feel free to open an issue.
Made with ❤️ by Erfan Mohammadzadeh

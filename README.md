# Regex Text Preprocessing

![Logo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTF-ufT8Iv0WrSGuzR_JOId0cqGpUrnZ6m4pg&s)

Text preprocessing pipeline using Regex patterns for NLP data cleaning. Features: stopword removal, contraction expansion, entity replacement, and multilingual support. Complete with documentation and Python implementation.





## Documentation

[English Documentation](documents/Preprocessing_Document_English.pdf) \
[Persian Documentation](documents/Preprocessing_Document_Persian.pdf)




## 📂 Project Structure
```
📦 Project Root
│
├── 📂 data
│    ├── 📂 processed
│    │    ├── 📂 maps
│    │    │    ├── 📄 money_dictionary.pkl
│    │    │    ├── 📄 time_dictionary.pkl
│    │    │    └── 📄 urls_dictionary.pkl
│    │    │
│    │    ├── 📜 test_clean.csv
│    │    └── 📜 train_clean.csv
│    │
│    └── 📂 raw
│         ├── 📜 test.csv
│         └── 📜 train.csv
│
├── 📂 documents
│    ├── 📓 Preprocessing_Document - English.pdf
│    └── 📓 Preprocessing_Document - Persian.pdf
│
├── 📂 resources
│    ├── 📊 English_Contractions.json
│    ├── 📊 English_Slang_Dict.json
│    └── 📄 English_Stopwords_without_negatives.txt
│
├── 📂 src
│    ├── __init__.py
│    ├── config.py
│    └── preprocessor.py
│
├── main.py
├── 📄 requirements.txt
└── 📄 README.md
```


## Installation

Open your terminal (Command Prompt, PowerShell, or Terminal), navigate to your project folder:

Install Dependencies (do this once):

```bash
  pip install -r requirements.txt
```

Run the Program:
```bash
  python main.py
```




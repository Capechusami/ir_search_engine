# 🔍 IR Search Engine

An academic-level Information Retrieval (IR) Search Engine built in Python, designed to retrieve the most relevant documents based on a user's query. This project leverages **TF-IDF** (Term Frequency–Inverse Document Frequency) and **Cosine Similarity** to compute document relevance scores and rank search results accordingly.

---

## 📘 Table of Contents

- [Overview](#-overview)
- [How It Works](#-how-it-works)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Examples](#-examples)
- [Dependencies](#-dependencies)
- [Future Improvements](#-future-improvements)
- [Credits](#-credits)
- [License](#-license)

---

## 📖 Overview

This project simulates a basic information retrieval system similar to a search engine. It indexes a set of documents and allows users to search for relevant documents based on natural language queries. The documents are preprocessed, vectorized using TF-IDF, and compared to the query using cosine similarity.

---

## 🧠 How It Works

### 🔹 TF-IDF (Term Frequency–Inverse Document Frequency)
- **Term Frequency (TF)**: Measures how often a term appears in a document.
- **Inverse Document Frequency (IDF)**: Measures how important or rare a term is across all documents.
- **TF-IDF**: A product of TF and IDF. It increases with term frequency but is offset by the frequency of the term in the corpus.

### 🔹 Cosine Similarity
Cosine similarity calculates the cosine angle between the TF-IDF vectors of the query and the documents. A higher cosine score indicates a closer match.

---

## ✨ Features

- Clean and modular Python code
- Customizable document corpus (supports `.txt` files)
- Query-based ranking using TF-IDF and cosine similarity
- Command-line interface for quick testing
- Easy to extend (e.g., support for stemming, GUI)

---

## 📁 Project Structure

ir_search_system/
│
├── dataset/ # Folder containing the corpus of documents (text files)
├── main.py # Main script to run the search engine
├── tfidf_engine.py # Module for TF-IDF vectorization
├── similarity.py # Module for computing cosine similarity
├── preprocessing.py # Module for text cleaning and tokenization
├── requirements.txt # Project dependencies
└── README.md # Project documentation


---

## 🛠 Installation

### 1. Clone the Repository


git clone https://github.com/Capechusami/ir_search_engine.git
cd ir_search_engine
2. Set Up a Virtual Environment (optional but recommended)
python -m venv .venv
# Activate the virtual environment:
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
▶️ Usage
1. Prepare the Documents
Put your .txt files inside the dataset/ folder. Each file represents one document.

2. Run the Search Engine
python main.py
You’ll be prompted to enter a search query. The engine will return a ranked list of documents based on their similarity to the query.

📦 Dependencies
scikit-learn: TF-IDF Vectorizer

nltk: Tokenization and optional stopword removal

numpy: Efficient array computations

Install them using:
pip install scikit-learn nltk numpy
🚧 Future Improvements
Add stemming or lemmatization using NLTK or spaCy

Add a Flask-based web interface

Save TF-IDF model using joblib for faster queries

Implement support for more file formats (e.g., PDF, DOCX)

Add performance evaluation: Precision, Recall, F1-score

🙋‍♂️ Credits
Developed by Samuel Tesfachew (Cap)
📧 Email: sami.bachiti@gmail.com
🔗 GitHub: Capechusami
🎓 Adama Science and Technology University
🧠 3rd Year Computer Science and Engineering Student


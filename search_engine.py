import re
import os
import math
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Optional stemming with NLTK
try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("english")
except ImportError:
    stemmer = None  # Fallback: no stemming

class IRSystem:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.documents = {}
        self.headers = {}  # doc_id -> brief_title
        self.index = defaultdict(lambda: defaultdict(list))  # term -> doc_id -> positions
        self.doc_lengths = {}  # doc_id -> number of terms
        self.tf = defaultdict(lambda: defaultdict(int))  # term -> doc_id -> frequency
        self.df = defaultdict(int)  # term -> document frequency
        self.cf = defaultdict(int)  # term -> collection frequency
        self.vocab = set()
        self.stop_words = ENGLISH_STOP_WORDS

        self.load_documents_from_folder()
        self.build_index()

    def parse_clinical_trials_xml(self, filepath):
        doc_dict = {}
        title_dict = {}
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            if root.tag == 'clinical_study':
                studies = [root]
            else:
                studies = root.findall("clinical_study")

            for i, study in enumerate(studies):
                doc_id = study.findtext("id_info/nct_id", default=f"doc_{i}").strip()
                title = study.findtext("brief_title", "").strip()
                summary = study.findtext("brief_summary/textblock", "")
                description = study.findtext("detailed_description/textblock", "")
                eligibility = study.findtext("eligibility/criteria/textblock", "")
                content = "\n".join([title, summary, description, eligibility])

                doc_dict[doc_id] = content
                title_dict[doc_id] = title if title else "Untitled Study"

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")

        return doc_dict, title_dict

    def preprocess(self, text):
        text = text.lower()
        tokens = re.findall(r'\b[a-z]{2,}\b', text)
        tokens = [t for t in tokens if t not in self.stop_words]
        if stemmer:
            tokens = [stemmer.stem(t) for t in tokens]
        return tokens

    def load_documents_from_folder(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".xml"):
                full_path = os.path.join(self.folder_path, filename)
                docs, titles = self.parse_clinical_trials_xml(full_path)
                for doc_id, text in docs.items():
                    self.documents[doc_id] = text
                    self.headers[doc_id] = titles[doc_id]

    def build_index(self):
        for doc_id, content in self.documents.items():
            tokens = self.preprocess(content)
            self.doc_lengths[doc_id] = len(tokens)
            term_counts = Counter(tokens)

            for i, token in enumerate(tokens):
                self.index[token][doc_id].append(i)
                self.cf[token] += 1

            for term, freq in term_counts.items():
                self.tf[term][doc_id] = freq
                self.df[term] += 1
                self.vocab.add(term)

    def compute_tfidf(self, filtered_terms):
        N = len(self.documents)
        tfidf = defaultdict(lambda: defaultdict(float))
        idf_values = {}

        for term in filtered_terms:
            if term in self.df:
                idf = math.log((N + 1) / (self.df[term] + 1)) + 1
                idf_values[term] = idf
                for doc in self.tf[term]:
                    tfidf[doc][term] = self.tf[term][doc] * idf

        return tfidf, idf_values

    def search(self, query):
        query_tokens = self.preprocess(query)
        query_counter = Counter(query_tokens)

        tfidf, idf_values = self.compute_tfidf(query_counter.keys())
        doc_scores = defaultdict(float)
        doc_norms = defaultdict(float)
        query_norm = 0.0

        for term, qtf in query_counter.items():
            if term not in idf_values:
                continue
            idf = idf_values[term]
            query_weight = qtf * idf
            query_norm += query_weight ** 2

            for doc in tfidf:
                if term in tfidf[doc]:
                    doc_scores[doc] += query_weight * tfidf[doc][term]
                    doc_norms[doc] += tfidf[doc][term] ** 2

        query_norm = math.sqrt(query_norm)
        for doc in doc_scores:
            doc_norms[doc] = math.sqrt(doc_norms[doc])
            if doc_norms[doc] != 0 and query_norm != 0:
                doc_scores[doc] /= (doc_norms[doc] * query_norm)
            else:
                doc_scores[doc] = 0.0

        ranked = dict(sorted(doc_scores.items(), key=lambda item: item[1], reverse=True))

        snippets = {}
        for doc in ranked:
            content = self.documents[doc]
            content_lower = content.lower()
            snippet = content[:300].replace('\n', ' ') + "..."
            for term in query_tokens:
                idx = content_lower.find(term)
                if idx != -1:
                    start = max(0, idx - 50)
                    end = min(len(content), idx + 150)
                    snippet = content[start:end].replace('\n', ' ') + "..."
                    break
            snippets[doc] = snippet

        query_tf = dict(query_counter)
        query_tfidf = {term: tf * idf_values[term] for term, tf in query_tf.items() if term in idf_values}

        # ⬇️ Final statistics payload (fully Jinja-friendly)
        stats = {
            "query_terms": list(query_tokens),
            "TF": {doc: {term: self.tf[term][doc] for term in query_tokens if doc in self.tf[term]} for doc in ranked},
            "IDF": {term: idf_values.get(term, 0.0) for term in query_tokens},
            "TFIDF": {doc: {term: tfidf[doc][term] for term in query_tokens if term in tfidf[doc]} for doc in ranked},
            "doc_lengths": self.doc_lengths,
            "query_TF": query_tf,
            "query_TFIDF": query_tfidf,
            "cosine_similarities": ranked
        }

        return ranked, snippets, doc_scores, stats
    def get_documents(self):
        return self.documents

    def get_headers(self):
        return self.headers

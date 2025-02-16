from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import pdfplumber

tfidf = TfidfVectorizer() # default
vectorizer = TfidfVectorizer()

# reading in data
import pandas as pd
data = pd.read_csv('UpdatedResumeDataSet.csv')

# drop duplicates
data.drop_duplicates(keep='first', inplace=True)

# natural language tooklit for NLP
import nltk

nltk.download('stopwords')
nltk.download("punkt_tab")

# to find stems of words
from nltk.stem import PorterStemmer
ps = PorterStemmer()

# transform text into keywords
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    # keep only alpha numeric
    text = [word for word in text if word.isalnum()]
    stopwords = nltk.corpus.stopwords.words('english')
    # remove unimportant stop words like "the" or "to"
    text = [word for word in text if word not in stopwords]
    # only get the stem "eating" -> eat
    text = [ps.stem(word) for word in text]
    text = ' '.join(text)
    return text

data['Transformed Resume'] = data['Resume'].apply(transform_text)

X = data["Transformed Resume"]

from sklearn.metrics.pairwise import cosine_similarity

if __name__ == "__main__":
    resume = sys.argv[1]
    job = sys.argv[2]
    with pdfplumber.open(resume) as pdf:
        resume_text = pdf.pages[0].extract_text()
    with pdfplumber.open(job) as pdf:
        job_text = pdf.pages[0].extract_text()
    vectorizer.fit(X)

    resume_vec = vectorizer.transform([resume_text])
    job_vec = vectorizer.transform([job_text])

    print(cosine_similarity(resume_vec, job_vec))
# some useful regex
import re
text = "http://mystuff hello there        w \n          é, à, ö, ñ 漢 (Chinese), こんにちは (Japanese), به متنی(Persian)"

# clean links
text = re.sub(r"http\S+", " ", text)
# remove all non ascii
text = re.sub(r"[^\x00-\x7f]", " ", text)
# remove extra whitespace
text = re.sub(r"\s+", " ", text)

# reading in data
import pandas as pd
data = pd.read_csv('UpdatedResumeDataSet.csv')

# Make a new Labels category
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['Label'] = le.fit_transform(data['Category'])

# drop duplicated values
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

# make a new transformed text column for resumes
data['Transformed Resume'] = data['Resume'].apply(transform_text)

# model building
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer() # default

X = data["Transformed Resume"]
y = data["Label"]

vectorizer = TfidfVectorizer()
vectorizer.fit(X)
features = vectorizer.transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    features,
    y,
    test_size=0.2,
    shuffle=True,
    random_state=2024,
)

# choose highest freq label in neighbors
model = KNeighborsClassifier()
model.fit(X_train, y_train)
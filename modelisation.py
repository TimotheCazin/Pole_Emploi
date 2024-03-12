import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import requests
import re
from unidecode import unidecode
import string
from nltk.stem.snowball import FrenchStemmer
from gensim.models import Phrases

df_model = pd.read_csv('df_model.csv',index_col=0)
vectorizer = joblib.load('vectorizer_bigram.pkl')

k = 15
# Vectorisation des descriptions
X_bigram = vectorizer.fit_transform(df_model['description_bigram'])
# Calcul des similarités avec la nouvelle description

def prediction_bigram(description_bigram):
    new_vector = vectorizer.transform([description_bigram])
    similarities = cosine_similarity(X_bigram, new_vector)

    df_temp = df_model.copy()
    df_temp['similarities'] = similarities
    df_temp = df_temp.sort_values('similarities',ascending=False).head(k)

    return (df_temp['salaires_final'] * df_temp['similarities']).sum()/df_temp['similarities'].sum()

def get_access_token():
    url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"

    client_id = "PAR_projetdatacentralemar_3627c1021bcb3d57c22720ecf47d16084fe0179161a399fdee6cbca4a79ffa56"
    client_secret = "04239bc539bfe414825bc8519433e061350dd781ce20966f44660d9d4f0eafc2"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    body = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }

    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"La requête a échoué avec le code de réponse {response.status_code}")

def get_description(string,access_token):
    id = string[-7:]
    url = f"https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/{id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return requests.get(url,headers=headers).json()['description']

def clean_description(text):
    # Retirer les urls et les retours lignes
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)
    text = re.sub(r'\n', '', text)
    # Retirer les chiffres
    text= "".join([i for i in text if not i.isdigit()])
    # Retirer la ponctuation et les accents
    table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    text = text.translate(table)
    text = unidecode(text)

    output = text.lower().split()

    with open("stop_words_french.txt", "r", encoding="utf-8") as file:
        stopwords = [ligne.strip() for ligne in file]
    output = [i for i in output if i not in stopwords]

    stemmer = FrenchStemmer()
    output = [stemmer.stem(i) for i in output]
    return output

def create_bigrams(clean_desc):
    bigram_mod = Phrases.load('bigram_mod.pkl')
    return " ".join(bigram_mod[clean_desc])

def main(url_or_id):
    access_token = get_access_token()
    desc = get_description(url_or_id,access_token)
    desc_cleaned = clean_description(desc)
    desc_bigrams = create_bigrams(desc_cleaned)
    return prediction_bigram(desc_bigrams)
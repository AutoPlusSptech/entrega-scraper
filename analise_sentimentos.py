from textblob import TextBlob
#from googletrans import Translator
from deep_translator import GoogleTranslator as Translator
import csv
import json

def analisar_sentimento(texto):
    tradutor = Translator(source= "pt", target= "en")
    texto_en = tradutor.translate(texto)
    blob = TextBlob(texto_en)
    return blob.sentiment.polarity


def read_json(file):
    with open(file) as f:
        return json.load(f)

def main():
    json_file = read_json('tweets.json')

    with open('sentimentos.csv', 'w',) as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['usuario', 'tweet', 'sentimento'])

    print('Analisando sentimento dos tweets...')

    for tweet in json_file:
        usuario = tweet['usuario']
        mensagem = tweet['tweet']
        sentimento = float(analisar_sentimento(mensagem))

        with open('sentimentos.csv', 'a') as f:
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL)
            writer.writerow([f"{usuario}", f"{mensagem}", f"{sentimento}"])

    print('\nArquivo de sentimento gerado com sucesso!')
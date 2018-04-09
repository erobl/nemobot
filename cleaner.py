from nltk.tokenize import RegexpTokenizer                                       
from stop_words import get_stop_words                                           
from nltk.stem import SnowballStemmer                                           
from unidecode import unidecode              
from gensim import corpora
import re

class Cleaner:
    __tokenizer = RegexpTokenizer("r\w")
    __stop_words = get_stop_words("es")
    __stemmer = SnowballStemmer("spanish")

    def limpiar(self, texto):
        if texto is None:
            return []
        if type(texto) == type(0.1):
            return []
        texto = texto.lower()
        texto = unidecode(texto)
        texto = re.sub(r'http\S+', '', texto)
        tokens = self.__tokenizer.tokenize(texto)
        tokens = [i for i in tokens if not i in self.__stop_words]
        tokens = [self.__stemmer.stem(i) for i in tokens] 
        return tokens

    def docs2bow(self, docset, prune_at=5000):
        texts = [self.limpiar(i) for i in docset]
        dictionary = corpora.Dictionary(texts, prune_at=prune_at)
        corpus = [dictionary.doc2bow(text) for text in texts]
        return (dictionary, corpus)

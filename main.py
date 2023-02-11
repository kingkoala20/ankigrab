import csv
from datetime import datetime as dt

from jisho_api.sentence import Sentence
from jisho_api.word import Word

from anki_csv_importer import *
import os


class Vocab:
    """Holds the word info such as reading, meaning and sentences"""
    
    def __init__(self, word) -> None:
        self.word = word
        self.reading = []
        self.meaning = []
        self.sentences = []
        self.fetch_fields()
        
    def fetch_fields(self):
        
        #-- Fetching Meaning and Reading
        
        resp = Word.request(self.word)
        if resp.meta.status != 200:
            print("Word not found!")
            del self
            return
        else:
            data = resp.data
            for e in data:
                if e.slug == self.word:
                    for r in e.japanese:
                        self.reading.append(r.reading)
                    for m in e.senses:
                        self.meaning.extend(m.english_definitions)
        
        #-- Fetching Sentences
        
        resp = Sentence.request(self.word)
        if resp.meta.status != 200:
            print("No Found Sentences")
            self.sentences = []
        else:
            data = resp.data
            for a in data[:4]:
                self.sentences.append(a.japanese)
                
        #NOTE I can't add the furigana properly even with the Japanese Support anki plugin
        # so I am removing furigana scraping in jisho-api for now - kingkoala
        
    def _anki_repr(self):
        return "。<br>".join(self.sentences)

            
class CSVGen:
    
    # -- Initial Config --
    
    deckname = "語句" #Target Deck
    note_type = "Def Card" #Target Note Type
    note_type_fields = ['Expression','Reading','Meaning','Sentences']
    
    def __init__(self):
        current = dt.now().strftime("%m-%d")
        self.filepath = f'.\csvs\{current} words.csv'
        if os.path.isfile(self.filepath) == False:
            with open(self.filepath, "w", encoding='utf-8', newline='') as f:
                csv_write = csv.writer(f, delimiter=';')
                csv_write.writerow(self.note_type_fields)
        
    def add_word(self, vocab):
        with open(self.filepath, "a+", encoding="utf-8", newline='') as f:
            csv_append = csv.writer(f, delimiter=';')
            csv_append.writerow([vocab.word, ', '.join(vocab.reading), ', '.join(vocab.meaning), vocab._anki_repr()])
        print("Word Added!")
        
    def import_to_anki(self):
        send_to_anki_connect(self.filepath, self.deckname, self.note_type)
        
        
class MSTodo:
    
    #--Initial Config--
    
    live_user = os.environ.get("LIVE_USER")
    live_pass = os.environ.get("LIVE_PASS")
    
    @staticmethod
    def fetch_anki_list(list_name):
        pass
    
    @staticmethod
    def add_list_to_csv(words, csv_filepath):
        pass
        
if __name__ == "__main__":
    myword = Vocab("手伝い")
    mycsv = CSVGen()
    mycsv.add_word(myword)
    mycsv.import_to_anki()
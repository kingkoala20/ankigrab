import csv
from datetime import datetime as dt

from jisho_api.sentence import Sentence
from jisho_api.word import Word

#-- Internal Imports --
from anki_csv_importer import *
from todo import MSTodo
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
        
        # TODO Fix exception not catching all attribute errors in case of an invalid word
        
        resp = Word.request(self.word)
        try:    
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
        except Exception:
            print("Word not found!")
        
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
        
    def _anki_repr_sentences(self):
        return "。<br>".join(self.sentences)

            
class CSVGen:
    """CSV generator object
        NOTE: You can either edit the class object in the source code or pass your own parameters.
         
        param deckname: str
            the target deckname of the anki deck
        param note_type: str
            the target note type's name
        param note_fields: list
            contains the fields of the target note type
            
        For more information please visit the ankiweb documentation: "https://docs.ankiweb.net/"
    """
    
    
    # -- Initial Config --
    
    deckname = "語句" #Target Deck
    note_type = "Def Card" #Target Note Type
    note_fields = ['Expression','Reading','Meaning','Sentences']
    
    def __init__(self, deckname=deckname, note_type=note_type, note_fields=note_fields):
        
        # -- Reinitializing config if user wants to build a custom instance
        self.deckname = deckname
        self.note_type = note_type
        self.note_fields = note_fields
        
        assert type(self.deckname) == str
        assert type(self.note_type) == str
        assert type(self.note_fields) == list
        
        # -- Fetching time on instantiation as filepath name
        
        current = dt.now().strftime("%m-%d")
        self.filepath = f'.\csvs\{current} words.csv'
        
        # -- Create a new csv file upon instantiation (if it doesn't already exist)
        
        if os.path.isfile(self.filepath) == False:
            with open(self.filepath, "w", encoding='utf-8', newline='') as f:
                csv_write = csv.writer(f, delimiter=';')
                csv_write.writerow(self.note_fields)
        
    def add_word(self, vocab):
        """Adds a entry to the generated csv file using the Vocab object"""
        
        with open(self.filepath, "a+", encoding="utf-8", newline='') as f:
            csv_append = csv.writer(f, delimiter=';')
            csv_append.writerow([vocab.word, ', '.join(vocab.reading), ', '.join(vocab.meaning), vocab._anki_repr_sentences()])
        print(f"Word {vocab} Added!")
        
    def import_to_anki(self):
        """anki csv importer wrapper"""
        send_to_anki_connect(self.filepath, self.deckname, self.note_type)
        
    def mass_import_to_anki(self, vocabs):
        """mass import on csv"""
        for v in vocabs:
            self.import_to_anki(v)
            
    def import_mstodo(self, mstodo):
        for word in mstodo.list:
            vocab = Vocab(word)
            self.add_word(vocab)                
        
        
        
if __name__ == "__main__":
    """fetcher = MSTodo()
    fetcher.fetch_anki_list()
    mycsv = CSVGen()
    mycsv.import_mstodo(fetcher)"""
    
    mycsv = CSVGen()
    print(mycsv.deckname)
    mycsv.deckname = "test"
    print(mycsv.deckname)
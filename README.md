# Ankigrab

[日本語はこちらへ](#日本語)

## Usage
- Scrapes data from jisho.org via [jisho-api](https://github.com/pedroallenrevez/jisho-api) by pedroallenrevez which includes a word's reading, meaning and sample sentences.
- Data is then saved into a csv file that is ready to be imported into anki via [AnkiConnect](https://foosoft.net/projects/anki-connect/) plugin by FooSoft Productions.
- Beta Function: Integrates with MSTodo Tasks to jot words on your phone, the moment you hear or read them (very useful for lazy people who hates bringing pen and notebook).

## Intended Use Case
```python

mycsv = CSVGen() #initialize csv generator object
myword = Vocab(word) #initialize vocab object that scrapes meaning, reading and sample sentences
mycsv.add_word("私") #writes the fetched data on the csv
mycsv.import_to_anki() #imports the csv file into anki. Note: Make sure that ankiconnect plugin is installed and the local anki software is open.

#-- Beta Function MSTODO --
todo = MSTodo()
todo.fetch_anki_list()
mycsv.import_mstodo(todo)

```

## Preliminary Steps
1. I'm assuming you already use the ankiweb service, so you only need to install the Ankiconnect plugin, steps [HERE](https://foosoft.net/projects/anki-connect/) (Installation Section)
2. Clone this repository if you haven't already, and install the requirements.txt (pip install -r requirements.txt)
3. Depending on your use case, you can use this as package or by itself by running main.py

## Contributions
If you are interested in this project, please let me know! Let's make learning japanese much easier for everyone!

## Future Plan
- Build Desktop GUI
- Build WebApp

## 日本語
こちらのモジュールはANKIという復習ソフトの補助アプリケーションです。要点は語句の意味、読み方と例文を自動的に収集してそのデータをCSVに記録し、直接にANKIにインポートすることが出来るアプリケーションです。更に
MICROSOFTのTODOサービスにも連携も可能で語句が聞き取りや読み取り時点でスマホで安易に記録することが出来ます。外国人として復習に対して非常に役立てるものだと思われます。

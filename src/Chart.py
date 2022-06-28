import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import langdetect
from filtern import *


class Chart:

    databaseObject = ''
    table = ''

    """
    Die Klasse Chart erstellt Diagramme
    :param databaseObject: Das Objekt, das auf die aktuelle User-Datenbank referenziert
    :param table: die Tabelle, aus der die Daten für dei Diagramme kommen
    """

    def __init__(self, databaseObject, table):
       self.databaseObject = databaseObject
       self.table = table

    def makeBarChart(self, xAchse:list, yAchse:list):
        """
        :param xAchse: wird für die x-Achse des Diagramms benutzt
        :param yAchse: wird für die y-Achse des Diagramms benutzt

        die Methode erstellt ein Balkendiagramm aus den übergebenen Daten
        Die Tabelle wird gruppiert nach xAchse, damit nicht unendlich viele Balken entstehen
        Das Plot wird als png in static gespeichert, damit detailseite.html das Bild aufrufen und anzeigen kann
        """
        command = "SELECT * FROM " + self.table + " GROUP BY " + xAchse
        df = pd.read_sql_query(command, self.databaseObject.connection)
        ax = df.plot(kind='bar', x=xAchse, y=yAchse).get_figure()  # erstellt plot mit x- und y-Achse
        ax.savefig('static/name.png')  # speichert Bild zwischen, damit es angezeigt werden kann


    def makePieChart(self, xAchse:list, yAchse:list):
        """
        :param xAchse: wird für dei Berechnung der %-Zahlen der Kuchenstücke benutzt
        :param yAchse: die Daten, zu denen xAchse ins Verhältnis gesetzt wird

        die Methode erstellt ein pie chart aus den beiden übergebenen Daten
        die Daten der x-Achse-Variable werden gruppiert, und dann wird angegeben wie viel % die Werte der y-Achse-Variable der x-Achse einnehmen
        Beispiel:
        Eine Tabelle mit Teams und Punkten, Team A: 25Punkte, Team B: 20 Punkte, Team C: 10 Punkte
        Team ist yAchse, und Punkte is xAchse ->  Kuchenstück von A hat 46%, Kuchenstück von B hat 37%, Kuchenstück von C hat 17%
        Das Plot wird als png in static gespeichert, damit detailseite.html das Bild aufrufen und anzeigen kann
        """
        command = "SELECT * FROM " + self.table
        df = pd.read_sql_query(command, self.databaseObject.connection)
        ax = df.groupby([xAchse]).sum().plot(kind='pie', y=yAchse, autopct='%1.0f%%').get_figure()
        ax.savefig('static/name.png')


    def makeLineChart(self, xAchse:list, yAchse:list):
        """
        :param xAchse: wird für die x-Achse des Diagramms benutzt
        :param yAchse: wird für die y-Achse des Diagramms benutzt

        die Methode erstellt ein Liniendiagramm aus den übergebenen Daten
        Die Tabelle wird gruppiert nach xAchse, damit nicht unendlich viele Balken entstehen
        Das Plot wird als png in static gespeichert, damit detailseite.html das Bild aufrufen und anzeigen kann
        """
        command = "SELECT * FROM " + self.table + " GROUP BY " + xAchse
        df = pd.read_sql_query(command, self.databaseObject.connection)
        ax = df.plot(kind='line', x=xAchse, y=yAchse).get_figure()
        ax.savefig('static/name.png')


    def makeWordCloud(self):
        """
        Dies Methode erstellt eine WordCloud aus einem Ihr übergebenen DataFrame
        :param df: zu bearbeitendes DataFrame
        """
        try:
            command = "SELECT * FROM " + self.table
            df = pd.read_sql_query(command, self.databaseObject.connection)
            text = df.to_string(header=False, index=False)
            wordcloud = WordCloud(background_color="white", width=1920, height=1080, ).generate(text)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.savefig('static/name.png')
        except Exception as e:
            print("Oopsidupsi!", e.__class__, "ist aufgetreten.")

    def genauerBeschreibungDerWortarten(self):
        """
        Unter zu hilfe nahme dieser Funktion wird die genauere Beschreibung und
        Definition der Wortarten angezeigt
        """
        try:
            nltk.help.upenn_tagset()
        except Exception as e:
            print("Oopsidupsi!", e.__class__, "ist aufgetreten.")


    def makeWortartenAnalyse(self):
        """
        !!!
        Um mit diese Funktion arbeiten zu können benötigt das Programm zusätzliche Dateien.
        Diese können mit Hilfe von nltk.download() heruntergeladen werden.
        Hierzu muss nltk.download() in den Code eingefügt werden und dann einmalig ausgeführt werden.
        Wenn dies geschiet wird ein Fenster geöffnet.
        In diesem Fenster muss  nur der Download Button betätigt werden
        und der Download der benötigten Dateien beginnt automatisch.
        Nachdem der Download erfolgt ist kann das Fenster geschlossen werden.
        Nach der Installation der benötigten Daten kann nltk.download() aus dem Code gelöscht werden.
        !!!

        Mit hilfe dieser Funktion kann der Inhalt eines Dataframes eier Wordartenanalyse unterzogen werden.
        Die Sprache des übergebenen DataFrames wird automatisch ermittelt.
        Falls der Inhalt des DataFrames zu klein oder nicht aussagekräftig ist, wird Englisch als Standartwert angenommen.
        :param df: Zu übergebendes DataFrame

        """
        try:
            command = "SELECT * FROM " + self.table
            df = pd.read_sql_query(command, self.databaseObject.connection)
            # Dataframe wird in String umgewandlt
            text = df.to_string(header=False, index=False)
            # print(text)
            try:
                if langdetect.detect(text) == 'de':
                    einzelneWoerter = nltk.word_tokenize(text, language='german')
                else:
                    einzelneWoerter = nltk.word_tokenize(text, language='english')

            except Exception as e:
                einzelneWoerter = nltk.word_tokenize(text, language='english')

            # Text wird in Wörter zerteilt und die Tokens werden zugeordnet
            woerterMitTokenslistOfLists = nltk.pos_tag(einzelneWoerter)

            # die List of Lists wird zu einer einfachen Liste umgewandelt
            woerterMitTokensEinfacheListe = [x for xs in woerterMitTokenslistOfLists for x in xs]

            # Die verschiedenen Wordarten werden gezählt
            dollar = int(woerterMitTokensEinfacheListe.count('$') / 2.0)
            quotationMark = woerterMitTokensEinfacheListe.count("''")
            openingParenthesis = woerterMitTokensEinfacheListe.count('(')
            closingParenthesis = woerterMitTokensEinfacheListe.count(')')
            comma = woerterMitTokensEinfacheListe.count(',')
            dash = woerterMitTokensEinfacheListe.count('--')
            sentenceTerminator = woerterMitTokensEinfacheListe.count('.')
            colon = woerterMitTokensEinfacheListe.count(':')
            conjunction = woerterMitTokensEinfacheListe.count('CC')
            numeral = woerterMitTokensEinfacheListe.count('CD')
            determiner = woerterMitTokensEinfacheListe.count('DT')
            existentialThere = woerterMitTokensEinfacheListe.count('EX')
            foreignWord = woerterMitTokensEinfacheListe.count('FW')
            prepositionOrConjunction = woerterMitTokensEinfacheListe.count('IN')
            adjektivOrdinal = woerterMitTokensEinfacheListe.count('JJ')
            adjektivComperativ = woerterMitTokensEinfacheListe.count('JJR')
            adjectiveSuperlative = woerterMitTokensEinfacheListe.count('JJS')
            listItemMarker = woerterMitTokensEinfacheListe.count('LS')
            modalAuxiliary = woerterMitTokensEinfacheListe.count('MD')
            nounCommonSingular = woerterMitTokensEinfacheListe.count('NN')
            noundProperSingular = woerterMitTokensEinfacheListe.count('NNP')
            nounProperPlural = woerterMitTokensEinfacheListe.count('NNPS')
            nounCommonPlural = woerterMitTokensEinfacheListe.count('NNS')
            preDeterminer = woerterMitTokensEinfacheListe.count('PDT')
            genitiveMarker = woerterMitTokensEinfacheListe.count('POS')
            pronounPersonal = woerterMitTokensEinfacheListe.count('PRP')
            pronounPossesive = woerterMitTokensEinfacheListe.count('PRP$')
            adverb = woerterMitTokensEinfacheListe.count('RB')
            adverbComperative = woerterMitTokensEinfacheListe.count('RBR')
            adverbSuperlative = woerterMitTokensEinfacheListe.count('RBS')
            particle = woerterMitTokensEinfacheListe.count('RP')
            symbol = woerterMitTokensEinfacheListe.count('SYM')
            to = woerterMitTokensEinfacheListe.count('TO')
            interjenction = woerterMitTokensEinfacheListe.count('UH')
            verbBaseForm = woerterMitTokensEinfacheListe.count('VB')
            verbPastTense = woerterMitTokensEinfacheListe.count('VBD')
            verbPresentParticipleOrGerund = woerterMitTokensEinfacheListe.count('VBG')
            verbPastParticiple = woerterMitTokensEinfacheListe.count('VBN')
            verbPastTenseNotThirdPersonSingular = woerterMitTokensEinfacheListe.count('VBP')
            verbPresentTense = woerterMitTokensEinfacheListe.count('VBZ')
            whDeterminer = woerterMitTokensEinfacheListe.count('WDT')
            whPronun = woerterMitTokensEinfacheListe.count('WP')
            whPronunPossesive = woerterMitTokensEinfacheListe.count('WP$')
            whAdverb = woerterMitTokensEinfacheListe.count('WRB')
            openingQuotationMark = woerterMitTokensEinfacheListe.count('``')

            # Aus den obrigen Daten wird nun ein DataFrame erstellt und danach zurückgegeben
            wortArten = {'Wortarten:': ['Dollarzeichen', 'öffnende Klammer', 'schließende Klammer',
                                        'Komma', 'Bindestrich', 'Punkt/Ausrufezeichen/Fragezeichen', 'Doppelpunkt',
                                        'Konjunktion',
                                        'Ziffer', 'Determinator', 'existentialThere', 'Wort aus fremder Sprache',
                                        'Präposition oder Konjunktion', 'adjektivOrdinal', 'adjektivComperativ',
                                        'adjectiveSuperlative', 'listItemMarker', 'modales Hilfsmittel',
                                        'SubstantivCommonSingular', 'SubstantivProperSingular',
                                        'SubstantivProperPlural',
                                        'SubstantivCommonPlural', 'preDeterminer', 'Genitiv Marker',
                                        'Personalpronomen', 'Possessivpronomen', 'Adverb', 'Adverb Comperative',
                                        'Adverb Superlative', 'Partikel', 'Symbol', 'to', 'Interjenction',
                                        'Verb Basis Form', 'Verb Vergangenheitsform',
                                        'Verb Präsens Partizip oder Gerundium',
                                        'Verb Partizip Perfekt', 'Verb Präsens', 'wh Determiner', 'wh Pronomen',
                                        'wh Adverb', 'öffnendes Anführungszeichen',
                                        'Verb Vergangenheitsform nicht dritte Person Singular',
                                        'wh Possessivpronomen', 'Anführungszeichen'],
                         'Werte_Wortarten:': [dollar, openingParenthesis, closingParenthesis,
                                              comma, dash, sentenceTerminator, colon, conjunction,
                                              numeral, determiner, existentialThere, foreignWord,
                                              prepositionOrConjunction, adjektivOrdinal, adjektivComperativ,
                                              adjectiveSuperlative, listItemMarker, modalAuxiliary,
                                              nounCommonSingular, noundProperSingular, nounProperPlural,
                                              nounCommonPlural, preDeterminer, genitiveMarker,
                                              pronounPersonal, pronounPossesive, adverb, adverbComperative,
                                              adverbSuperlative, particle, symbol, to, interjenction,
                                              verbBaseForm, verbPastTense, verbPresentParticipleOrGerund,
                                              verbPastParticiple, verbPresentTense, whDeterminer, whPronun,
                                              whAdverb, openingQuotationMark, verbPastTenseNotThirdPersonSingular,
                                              whPronunPossesive, quotationMark]}

            wortArten_df = pd.DataFrame(wortArten)

            wortArten_df_nur_zeilen_mit_wert_uerber_null = zeilenFiltern(wortArten_df, 'Werte_Wortarten:', 0, '>')

            # Das Dataframe wird in eine Grafik umgewandelt
            wortArten_df_nur_zeilen_mit_wert_uerber_null.head()

            sns.set(rc={'figure.figsize': (16, 12)})
            ax = sns.barplot(y='Wortarten:', x='Werte_Wortarten:',
                             data=wortArten_df_nur_zeilen_mit_wert_uerber_null, palette='rocket')

            initialx = 0
            for p in ax.patches:
                ax.text(p.get_width(), initialx + p.get_height() / 8, '{:1.0f}'.format(p.get_width()))

                initialx += 1

            plt.savefig('static/name.png')
            plt.show()


        except Exception as e:
            print("Oopsidupsi! ", e.__class__, "ist aufgetreten.")




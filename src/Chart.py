import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import langdetect
import seaborn as sns
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
        try:
            plt.clf()
            plt.cla()
            plt.close()
            command = "SELECT * FROM " + self.table + " GROUP BY " + xAchse
            df = pd.read_sql_query(command, self.databaseObject.connection)

            #ax = df.plot(kind='bar', x=xAchse, y=yAchse).get_figure()  # erstellt plot mit x- und y-Achse

            # erstellt plot mit x- und y-Achse
            ax = sns.barplot(y=yAchse, x=xAchse, data=df, palette='rocket').get_figure()


            ax.savefig('static/balkendiagramm.png')  # speichert Bild zwischen, damit es angezeigt werden kann



        except Exception as e:
            print("Oopsidupsi!", e.__class__, "ist aufgetreten.")



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

        try:
            plt.clf()
            plt.cla()
            plt.close()
            command = "SELECT * FROM " + self.table
            df = pd.read_sql_query(command, self.databaseObject.connection)


            ax = df.groupby([xAchse]).sum().plot(kind='pie', y=yAchse, autopct='%1.0f%%').get_figure()

            #colors = sns.color_palette('rocket')
            #ax = plt.pie(data =df, colors = colors, autopct='%.0f%%')

            ax.savefig('static/piechart.png')


        except Exception as e:
            print("Oopsidupsi!", e.__class__, "ist aufgetreten.")


    def makeLineChart(self, xAchse:list, yAchse:list):
        """
        :param xAchse: wird für die x-Achse des Diagramms benutzt
        :param yAchse: wird für die y-Achse des Diagramms benutzt

        die Methode erstellt ein Liniendiagramm aus den übergebenen Daten
        Die Tabelle wird gruppiert nach xAchse, damit nicht unendlich viele Balken entstehen
        Das Plot wird als png in static gespeichert, damit detailseite.html das Bild aufrufen und anzeigen kann
        """

        try:
            plt.clf()
            plt.cla()
            plt.close()
            command = "SELECT * FROM " + self.table + " GROUP BY " + xAchse
            df = pd.read_sql_query(command, self.databaseObject.connection)

            #ax = df.plot(kind='line', x=xAchse, y=yAchse).get_figure()

            #Auf jeden Fall nochmals überprüfen
            #ab und zu Fehler bei mir
            #wenn dies nicht zu beheben sind einfach die ursrpringliche
            #Version nutzen um das Line Chart zu  erzeugen

            ax = sns.lineplot(x=xAchse, y=yAchse,data=df, palette='rocket').get_figure()

            ax.savefig('static/liniendiagramm.png')


        except Exception as e:
            print("Oopsidupsi!", e.__class__, "ist aufgetreten.")

    def makeWordCloud(self):
        """
        !!!
        bei dieser Funktion können es zu Fehlern auftreten,
        falls die Version 14.0 von c++
        nicht installiert ist.(dies kann vor allem bei älteren Windows PCs der Fall sein).
        Diese Version kann sehr einfach über den Visual Studio Installer herunter geladen werden.
        !!!

        Dies Methode erstellt eine WordCloud aus einem Ihr übergebenen DataFrame
        Das Plot wird als png in static gespeichert,
        damit detailseite.html das Bild aufrufen und anzeigen kann
        :param df: zu bearbeitendes DataFrame
        """
        try:
            plt.clf()
            plt.cla()
            plt.close()
            command = "SELECT * FROM " + self.table
            df = pd.read_sql_query(command, self.databaseObject.connection)
            text = df.to_string(header=False, index=False)
            wordcloud = WordCloud(background_color="white", width=1920, height=1080, ).generate(text)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.savefig('static/wordcloud.png')


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
        Das Plot wird als png in static gespeichert,
        damit detailseite.html das Bild aufrufen und anzeigen kann
        :param df: Zu übergebendes DataFrame

        """
        try:
            plt.clf()
            plt.cla()
            plt.close()
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
            # Falls Textbausteine wie NNP oder JJR im ursprünglischen Text enthalten sind,
            # werden diese subtrahiert


            dollar = woerterMitTokensEinfacheListe.count('$') - einzelneWoerter.count('$')
            quotationMark = woerterMitTokensEinfacheListe.count("''")- einzelneWoerter.count("''")
            openingParenthesis = woerterMitTokensEinfacheListe.count('(')-einzelneWoerter.count('(')
            closingParenthesis = woerterMitTokensEinfacheListe.count(')')-einzelneWoerter.count(')')
            comma = woerterMitTokensEinfacheListe.count(',')-einzelneWoerter.count(',')
            dash = woerterMitTokensEinfacheListe.count('--')-einzelneWoerter.count('--')
            sentenceTerminator = woerterMitTokensEinfacheListe.count('.')-einzelneWoerter.count('.')
            colon = woerterMitTokensEinfacheListe.count(':')-einzelneWoerter.count(':')
            conjunction = woerterMitTokensEinfacheListe.count('CC')-einzelneWoerter.count('CC')
            numeral = woerterMitTokensEinfacheListe.count('CD')-einzelneWoerter.count('CD')
            determiner = woerterMitTokensEinfacheListe.count('DT')- einzelneWoerter.count('DT')
            existentialThere = woerterMitTokensEinfacheListe.count('EX')-einzelneWoerter.count('EX')
            foreignWord = woerterMitTokensEinfacheListe.count('FW')-einzelneWoerter.count('FW')
            prepositionOrConjunction = woerterMitTokensEinfacheListe.count('IN')-einzelneWoerter.count('IN')
            adjektivOrdinal = woerterMitTokensEinfacheListe.count('JJ')-einzelneWoerter.count('JJ')
            adjektivComperativ = woerterMitTokensEinfacheListe.count('JJR')-einzelneWoerter.count('JJR')
            adjectiveSuperlative = woerterMitTokensEinfacheListe.count('JJS')-einzelneWoerter.count('JJS')
            listItemMarker = woerterMitTokensEinfacheListe.count('LS')-einzelneWoerter.count('LS')
            modalAuxiliary = woerterMitTokensEinfacheListe.count('MD')-einzelneWoerter.count('MD')
            nounCommonSingular = woerterMitTokensEinfacheListe.count('NN')-einzelneWoerter.count('NN')
            noundProperSingular = woerterMitTokensEinfacheListe.count('NNP')-einzelneWoerter.count('NNP')
            nounProperPlural = woerterMitTokensEinfacheListe.count('NNPS')-einzelneWoerter.count('NNPS')
            nounCommonPlural = woerterMitTokensEinfacheListe.count('NNS')-einzelneWoerter.count('NNS')
            preDeterminer = woerterMitTokensEinfacheListe.count('PDT')-einzelneWoerter.count('PDT')
            genitiveMarker = woerterMitTokensEinfacheListe.count('POS')-einzelneWoerter.count('POS')
            pronounPersonal = woerterMitTokensEinfacheListe.count('PRP')-einzelneWoerter.count('PRP')
            pronounPossesive = woerterMitTokensEinfacheListe.count('PRP$')-einzelneWoerter.count('PRP$')
            adverb = woerterMitTokensEinfacheListe.count('RB')-einzelneWoerter.count('RB')
            adverbComperative = woerterMitTokensEinfacheListe.count('RBR')-einzelneWoerter.count('RBR')
            adverbSuperlative = woerterMitTokensEinfacheListe.count('RBS')-einzelneWoerter.count('RBS')
            particle = woerterMitTokensEinfacheListe.count('RP')-einzelneWoerter.count('RP')
            symbol = woerterMitTokensEinfacheListe.count('SYM')-einzelneWoerter.count('SYM')
            to = woerterMitTokensEinfacheListe.count('TO')-einzelneWoerter.count('TO')
            interjenction = woerterMitTokensEinfacheListe.count('UH')-einzelneWoerter.count('UH')
            verbBaseForm = woerterMitTokensEinfacheListe.count('VB')-einzelneWoerter.count('VB')
            verbPastTense = woerterMitTokensEinfacheListe.count('VBD')-einzelneWoerter.count('VBD')
            verbPresentParticipleOrGerund = woerterMitTokensEinfacheListe.count('VBG')-einzelneWoerter.count('VBG')
            verbPastParticiple = woerterMitTokensEinfacheListe.count('VBN')-einzelneWoerter.count('VBN')
            verbPastTenseNotThirdPersonSingular = woerterMitTokensEinfacheListe.count('VBP')-einzelneWoerter.count('VBP')
            verbPresentTense = woerterMitTokensEinfacheListe.count('VBZ')-einzelneWoerter.count('VBZ')
            whDeterminer = woerterMitTokensEinfacheListe.count('WDT')-einzelneWoerter.count('WDT')
            whPronun = woerterMitTokensEinfacheListe.count('WP')-einzelneWoerter.count('WP')
            whPronunPossesive = woerterMitTokensEinfacheListe.count('WP$')-einzelneWoerter.count('WP$')
            whAdverb = woerterMitTokensEinfacheListe.count('WRB')-einzelneWoerter.count('WRB')
            openingQuotationMark = woerterMitTokensEinfacheListe.count('``')-einzelneWoerter.count('``')

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
            #Die werte werden hinter den Balken angezeigt
            initialx = 0
            for p in ax.patches:
                ax.text(p.get_width(), initialx + p.get_height() / 8, '{:1.0f}'.format(p.get_width()))

                initialx += 1

            #ax.getfigure()
            plt.savefig('static/wortartenanalyse.png')



        except Exception as e:
            print("Oopsidupsi! ", e.__class__, "ist aufgetreten.")





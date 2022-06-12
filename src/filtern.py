import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import langdetect


# nltk.download()
test_df = {'Tiere': ['Maus', 'Affe', 'Huhn','Dollar'],
           'Werte Tiere':[1,2,3,'$']}
test_df = pd.DataFrame(test_df)
test_df_2 ={'Dollar':['$']}
test_df_2 =pd.DataFrame(test_df_2)
# Test Dataframe mit zufälligen Daten
df = pd.read_csv('test_Csv_Datein/Sacramentorealestatetransactions.csv')
#print(df)

def zeilenFiltern(df, spaltenname, wert, operator):
    """
    mit Hilfe der zeilenFiltern Methode können Zeilen ausgegeben werden, wenn sie einem bestimmten
    Spaltenwert entsprechen/größer/kleiner sind

    :param df: das zu bearbeitende DataFrame
    :param spaltenname: Überschrift nach der zu sortierenden Spalte
    :param wert: Spaltenwert nach dem gefiltert werden soll
    :param operator: </>/==
    :return:gibt die gefilterten Zeilen als neues Dataframe aus
    """
    try:
        if operator == '>':
            df_maske = df[spaltenname] > wert
            filtered_df = df[df_maske]
            return filtered_df
        elif operator == '<':
            df_maske = df[spaltenname] < wert
            filtered_df = df[df_maske]
            return filtered_df
        elif operator == '==':
            df_maske = df[spaltenname] == wert
            filtered_df = df[df_maske]
            return filtered_df
        elif operator == '!=':
            df_maske = df[spaltenname] != wert
            filtered_df = df[df_maske]
            return filtered_df
    except Exception as e:
        print("Oopsidupsi!", e.__class__, "ist aufgetreten.")


# mit der Funktion spaltenFiltern können einzelne oder mehrere  Spalten ausgegeben werden
def spaltenFiltern(df, liste):
    """
    mit der Funktion spaltenFiltern können einzelne oder mehere  Spalten ausgegeben werden
    :param df: zu bearbeitendes DataFrame
    :param liste: Liste mit dem Namen der auszuwählenden Spalten
    :return:gibt die ausgewählten Spalten als Dataframe zurück
    """
    spaltenFiltern_df = df[liste]
    return spaltenFiltern_df


def wordcloudErstellen(df):
    """
    Dies Methode erstellt eine WordCloud aus einem Ihr übergebenen DataFrame
    :param df: zu bearbeitendes DataFrame
    """
    try:
        text = df.to_string(header=False, index=False)
        wordcloud = WordCloud(background_color="white", width=1920, height=1080, ).generate(text)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
    except Exception as e:
        print("Oopsidupsi!", e.__class__, "ist aufgetreten.")
    '''
    text = df.to_string(header=False, index=False)
    wordcloud = WordCloud(background_color="white", width=1920, height=1080, ).generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('static/name.png')
    '''

def genauerBeschreibungDerWortarten():
    """
    Unter zu hilfe nahme dieser Funktion wird die genauere Beschreibung und
    Definition der Wortarten angezeigt
    """
    try:
        nltk.help.upenn_tagset()
    except Exception as e:
        print("Oopsidupsi!", e.__class__, "ist aufgetreten.")

def wortartenAnalyse(df):
    """
    Mit hilfe dieser Funktion kann der Inhalt eines Dataframes eier Wordartenanalyse unterzogen werden.
    Die Sprache des übergebenen DataFrames wird automatisch ermittelt.
    Falls der Inhalt des DataFrames zu klein oder nicht aussagekräftig ist, wird Englisch als Standartwert angenommen.
    :param df: Zu übergebendes DataFrame

    """
    try:
        #Dataframe wird in String umgewanderlt
        text = df.to_string(header=False, index=False)
        #print(text)
        try:
            if(langdetect.detect(text)=='de'):
                einzelneWoerter = nltk.word_tokenize(text, language='german')
            else:
                einzelneWoerter = nltk.word_tokenize(text, language='english')

        except Exception as e:
            einzelneWoerter = nltk.word_tokenize(text, language='english')

        # Text wird in Wörter zerteilt und die Tokens werden zugeordnet
        woerterMitTokenslistOfLists = nltk.pos_tag(einzelneWoerter)

        #die List of Lists wird zu einer einfachen Liste umgewandelt
        woerterMitTokensEinfacheListe = [x for xs in woerterMitTokenslistOfLists for x in xs]

        #Die verschiedenen Wordarten werden gezählt
        dollar = int(woerterMitTokensEinfacheListe.count('$')/2.0)
        quotationMark = woerterMitTokensEinfacheListe.count("''")
        openingParenthesis = woerterMitTokensEinfacheListe.count('(')
        closingParenthesis = woerterMitTokensEinfacheListe.count(')')
        comma = woerterMitTokensEinfacheListe.count(',')
        dash= woerterMitTokensEinfacheListe.count('--')
        sentenceTerminator = woerterMitTokensEinfacheListe.count('.')
        colon = woerterMitTokensEinfacheListe.count(':')
        conjunction= woerterMitTokensEinfacheListe.count('CC')
        numeral = woerterMitTokensEinfacheListe.count('CD')
        determiner = woerterMitTokensEinfacheListe.count('DT')
        existentialThere = woerterMitTokensEinfacheListe.count('EX')
        foreignWord= woerterMitTokensEinfacheListe.count('FW')
        prepositionOrConjunction= woerterMitTokensEinfacheListe.count('IN')
        adjektivOrdinal= woerterMitTokensEinfacheListe.count('JJ')
        adjektivComperativ= woerterMitTokensEinfacheListe.count('JJR')
        adjectiveSuperlative= woerterMitTokensEinfacheListe.count('JJS')
        listItemMarker= woerterMitTokensEinfacheListe.count('LS')
        modalAuxiliary= woerterMitTokensEinfacheListe.count('MD')
        nounCommonSingular= woerterMitTokensEinfacheListe.count('NN')
        noundProperSingular= woerterMitTokensEinfacheListe.count('NNP')
        nounProperPlural= woerterMitTokensEinfacheListe.count('NNPS')
        nounCommonPlural= woerterMitTokensEinfacheListe.count('NNS')
        preDeterminer= woerterMitTokensEinfacheListe.count('PDT')
        genitiveMarker= woerterMitTokensEinfacheListe.count('POS')
        pronounPersonal= woerterMitTokensEinfacheListe.count('PRP')
        pronounPossesive= woerterMitTokensEinfacheListe.count('PRP$')
        adverb= woerterMitTokensEinfacheListe.count('RB')
        adverbComperative= woerterMitTokensEinfacheListe.count('RBR')
        adverbSuperlative = woerterMitTokensEinfacheListe.count('RBS')
        particle = woerterMitTokensEinfacheListe.count('RP')
        symbol = woerterMitTokensEinfacheListe.count('SYM')
        to = woerterMitTokensEinfacheListe.count('TO')
        interjenction= woerterMitTokensEinfacheListe.count('UH')
        verbBaseForm= woerterMitTokensEinfacheListe.count('VB')
        verbPastTense= woerterMitTokensEinfacheListe.count('VBD')
        verbPresentParticipleOrGerund= woerterMitTokensEinfacheListe.count('VBG')
        verbPastParticiple= woerterMitTokensEinfacheListe.count('VBN')
        verbPastTenseNotThirdPersonSingular= woerterMitTokensEinfacheListe.count('VBP')
        verbPresentTense= woerterMitTokensEinfacheListe.count('VBZ')
        whDeterminer= woerterMitTokensEinfacheListe.count('WDT')
        whPronun= woerterMitTokensEinfacheListe.count('WP')
        whPronunPossesive= woerterMitTokensEinfacheListe.count('WP$')
        whAdverb= woerterMitTokensEinfacheListe.count('WRB')
        openingQuotationMark= woerterMitTokensEinfacheListe.count('``')

        #Aus den obrigen Daten wird nun ein DataFrame erstellt und danach zurückgegeben
        wortArten = {'Wortarten:':['Dollarzeichen','öffnende Klammer','schließende Klammer',
                                   'Komma','Bindestrich','Punkt/Ausrufezeichen/Fragezeichen','Doppelpunkt','Konjunktion',
                                   'Ziffer','Determinator','existentialThere','Wort aus fremder Sprache',
                                   'Präposition oder Konjunktion','adjektivOrdinal','adjektivComperativ',
                                   'adjectiveSuperlative','listItemMarker','modales Hilfsmittel',
                                   'SubstantivCommonSingular','SubstantivProperSingular','SubstantivProperPlural',
                                   'SubstantivCommonPlural','preDeterminer','Genitiv Marker',
                                   'Personalpronomen','Possessivpronomen','Adverb','Adverb Comperative',
                                    'Adverb Superlative','Partikel','Symbol','to','Interjenction',
                                   'Verb Basis Form','Verb Vergangenheitsform','Verb Präsens Partizip oder Gerundium',
                                   'Verb Partizip Perfekt','Verb Präsens','wh Determiner','wh Pronomen',
                                   'wh Adverb','öffnendes Anführungszeichen','Verb Vergangenheitsform nicht dritte Person Singular',
                                   'wh Possessivpronomen','Anführungszeichen'],
                     'Werte_Wortarten:':[dollar,openingParenthesis,closingParenthesis,
                                         comma,dash,sentenceTerminator,colon,conjunction,
                                         numeral,determiner,existentialThere,foreignWord,
                                         prepositionOrConjunction,adjektivOrdinal,adjektivComperativ,
                                         adjectiveSuperlative,listItemMarker,modalAuxiliary,
                                         nounCommonSingular,noundProperSingular,nounProperPlural,
                                         nounCommonPlural,preDeterminer,genitiveMarker,
                                         pronounPersonal,pronounPossesive,adverb,adverbComperative,
                                         adverbSuperlative,particle,symbol,to,interjenction,
                                         verbBaseForm,verbPastTense,verbPresentParticipleOrGerund,
                                         verbPastParticiple,verbPresentTense,whDeterminer,whPronun,
                                         whAdverb,openingQuotationMark,verbPastTenseNotThirdPersonSingular,
                                         whPronunPossesive,quotationMark]}

        wortArten_df =pd.DataFrame(wortArten)

        wortArten_df_nur_zeilen_mit_wert_uerber_null = zeilenFiltern(wortArten_df,'Werte_Wortarten:',0,'>')

        return wortArten_df_nur_zeilen_mit_wert_uerber_null
    except Exception as e:
        print("Oopsidupsi! ", e.__class__, "ist aufgetreten.")

print(wortartenAnalyse(test_df_2))
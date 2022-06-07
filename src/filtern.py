import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import nltk
import langdetect
import sys


# nltk.download()


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



def genauerBeschreibungDerWortarten():
    """
    Unter zu hilfe nahme dieser Funktion wird die genauer Beschreibung und
    Definition der Wortarten angezeigt
    """
    try:
        nltk.help.upenn_tagset()
    except Exception as e:
        print("Oopsidupsi!", e.__class__, "ist aufgetreten.")

def wordartenAnalyse(df):
    """
    Mit hilfe dieser Funktion kann der Inhalt eines Dataframes eier Wordartenanalyse unterzogen werden.
    Die Sprache des übergebenen DataFrames wird automatisch ermittelt.
    Falls der Inhalt des DataFrames zu klein oder nicht aussagekräftig ist, wird Englisch als Standartwert angenommen.
    :param df: Zu übergebendes DataFrame

    """
    try:
        #Dataframe wird in String umgewanderlt
        text = df.to_string(header=False, index=False)
        if(langdetect.detect(text)=='de'):
            einzelneWoerter = nltk.word_tokenize(text, language='german')
        else:
            einzelneWoerter = nltk.word_tokenize(text, language='english')

        # Text wird in Wörter zerteilt und die Tokens werden zugeordnet
        woerterMitTokenslistOfLists = nltk.pos_tag(einzelneWoerter)

        #die List of Lists wird zu einer einfachen Liste umgewandelt
        woerterMitTokensEinfacheListe = [x for xs in woerterMitTokenslistOfLists for x in xs]

        #Die verschiedenen Wordarten werden gezählt
        dollar = woerterMitTokensEinfacheListe.count('$')
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
        wortArten = {'Wortarten:':['dollar','openingParenthesis','closingParenthesis',
                                   'comma','dash','sentenceTerminator','colon','conjunction',
                                   'numeral','determiner','existentialThere','foreignWord',
                                   'prepositionOrConjunction','adjektivOrdinal','adjektivComperativ',
                                   'adjectiveSuperlative','listItemMarker','modalAuxiliary',
                                   'nounCommonSingular','nounProperSingular','nounProperPlural',
                                   'nounCommonPlural','preDeterminer','genitiveMarker',
                                   'pronounPersonal','pronounPossesive','adverb','adverbComperative',
                                    'adverbSuperlative','particle','symbol','to','interjenction',
                                   'verbBaseForm','verbPastTense','verbPresentParticipleOrGerund',
                                   'verbPastParticiple','verbPresentTense','whDeterminer','whPronun',
                                   'whAdverb','openingQuotationMark','verbPastTenseNotThirdPersonSingular',
                                   'whPronunPossesive','quotationMark'],
                     'Werte Wortarten:':[dollar,openingParenthesis,closingParenthesis,
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
        return wortArten_df
    except Exception as e:
        print("Oopsidupsi!", e.__class__, "ist aufgetreten.")

print(wordartenAnalyse(df))

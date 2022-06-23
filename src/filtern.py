import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import langdetect
import seaborn as sns
import numpy as np

# nltk.download()
test_df = {'Tiere': ['Maus', 'Affe', 'Huhn','Dollar'],
           'Werte Tiere':[1,2,3,'$']}
test_df = pd.DataFrame(test_df)
test_df_2 ={'Dollar':['$']}
test_df_2 =pd.DataFrame(test_df_2)
# Test Dataframe mit zufälligen Daten


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



def zeilenAuswählen(df, range:str):
    return df[int(range.split("-")[0]):int(range.split("-")[1])+1]



# mit der Funktion spaltenFiltern können einzelne oder mehrere  Spalten ausgegeben werden
def spaltenFiltern(df, liste):
    """
    mit der Funktion spaltenFiltern können einzelne oder mehere  Spalten ausgegeben werden
    :param df: zu bearbeitendes DataFrame
    :param liste: Liste mit dem Namen der auszuwählenden Spalten
    :return:gibt die ausgewählten Spalten als Dataframe zurück
    """
    for i in liste:
        type(i)
    spaltenFiltern_df = df[liste]
    return spaltenFiltern_df

def zeilenAuswählen(df, range:str):
    return df[int(range.split("-")[0]):int(range.split("-")[1])+1]


import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import langdetect
import seaborn as sns
import numpy as np
from flask import flash
# nltk.download()



def zeilenFiltern(df, spaltenname, wert, operator):
    """
    mit Hilfe der zeilenFiltern Methode können Zeilen ausgegeben werden, wenn sie einem bestimmten
    Spaltenwert entsprechen/größer/kleiner sind

    :param df: das zu bearbeitende DataFrame
    :param spaltenname: Überschrift nach der zu sortierenden Spalte
    :param wert: Spaltenwert nach dem gefiltert werden soll
    :param operator: </>/==
    :param operator:o.Quartil & u.Quartil  müssen bei werd derzeit einen neutralen Wert 0 eingeben
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
        elif operator == '> median':
            df_maske = df[spaltenname] > df[spaltenname].quantile(q=0.50)
            filtered_df = df[df_maske]
            return filtered_df

        elif operator == '< median':
            df_maske = df[spaltenname] < df[spaltenname].quantile(q=0.50)
            filtered_df = df[df_maske]
            return filtered_df

        elif operator == '> oQuartil':
            df_maske = df[spaltenname] > df[spaltenname].quantile(q=0.75)

            filtered_df = df[df_maske]
            return filtered_df

        elif operator == '< oQuartil':
            df_maske = df[spaltenname] < df[spaltenname].quantile(q=0.75)
            filtered_df = df[df_maske]
            return filtered_df

        elif operator == '> uQuartil':
            df_maske = df[spaltenname] > df[spaltenname].quantile(q=0.25)
            filtered_df = df[df_maske]
            return filtered_df

        elif operator == '< uQuartil':
            df_maske = df[spaltenname] < df[spaltenname].quantile(q=0.25)
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


import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
# Test Dataframe mit zufälligen Daten
df = pd.read_csv('test_Csv_Datein/Sacramentorealestatetransactions.csv')


# mit Hilfe der zeilenFiltern Methode können Zeilen ausgegeben werden, wenn sie einem bestimmten
# Spaltenwert entsprechen/größer/kleiner sind

def zeilenFiltern(df, spaltenname, wert, operator):
    """

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



# mit der Funktion spaltenFiltern können einzelne oder mehere  Spalten ausgegeben werden
def spaltenFiltern(df, liste):
    """

    :param df: zu bearbeitendes DataFrame
    :param liste: Liste mit dem Namen der auszuwählenden Spalten
    :return:gibt die ausgewählten Spalten als Dataframe zurück
    """
    spaltenFiltern_df = df[liste]
    return spaltenFiltern_df



def wordcloudErstellen(df):
    text =df.to_string(header=False,index=False)
    wordcloud = WordCloud(background_color="white", width=1920, height=1080, ).generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

wordcloudErstellen(df)
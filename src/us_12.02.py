import pandas as pd
df = pd.DataFrame({'Name' : ["Peter", "Karla", "Anne", "Nino", "Andrzej"],
                   'Alter': [34, 53, 16, 22, 61],
                   'Nationalität': ["deutsch", "schweizerisch", "deutsch", "italienisch", "polnisch"],
                   'Gehalt': [3400, 4000, 0, 2100, 2300]},
                  index = ['ID-123', 'ID-462', 'ID-111', 'ID-997', 'ID-707'],
                 columns = ['Name', 'Alter', 'Nationalität', 'Gehalt'])




#mit Hilfe der zeilenFiltern Methode können Zeilen ausgegeben werden, wenn sie einem bestimmten
#Spaltenwert entsprechen/größer/kleiner sind

def zeilenFiltern(df,spaltenname,wert,operator):
    """

    :param df: das zu bearbeitende DataFrame
    :param spaltenname: Überschrift nach der zu sortierenden Spalte
    :param wert: Spaltenwert nach dem gefiltert werden soll
    :param operator: </>/==
    :return:
    """
    if(operator=='>'):
        df_maske = df[spaltenname] > wert
        filtered_df = df[df_maske]
        return filtered_df
    elif (operator == '<'):
        df_maske = df[spaltenname] < wert
        filtered_df = df[df_maske]
        return filtered_df
    elif (operator == '=='):
        df_maske = df[spaltenname] == wert
        filtered_df = df[df_maske]
        return filtered_df






spaltenFiltern_df = df[['Name', 'Alter', 'Gehalt']]
print(spaltenFiltern_df, "\n")

#mit der Funktion spaltenFiltern können einzelne Spalten ausgegeben werden
def spaltenFiltern(df,liste):
    """

    :param df: zu bearbeitendes DataFrame
    :param liste: Liste mit dem auszuwählenden Spaltennamen
    :return:
    """
    spaltenFiltern_df = df[liste]
    return spaltenFiltern_df
"""liste =['Name','Alter','Gehalt']
print(spaltenFiltern(df,liste))"""
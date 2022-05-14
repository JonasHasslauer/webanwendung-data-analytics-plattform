import pandas as pd
df = pd.DataFrame({'Name' : ["Peter", "Karla", "Anne", "Nino", "Andrzej"],
                   'Alter': [34, 53, 16, 22, 61],
                   'Nationalität': ["deutsch", "schweizerisch", "deutsch", "italienisch", "polnisch"],
                   'Gehalt': [3400, 4000, 0, 2100, 2300]},
                  index = ['ID-123', 'ID-462', 'ID-111', 'ID-997', 'ID-707'],
                 columns = ['Name', 'Alter', 'Nationalität', 'Gehalt'])

#print(df)
"""
df_mask=df['Alter']>50
filtered_df = df[df_mask]
print(filtered_df)
"""


#mit Hilfe der zeilenFiltern Methode können Zeilen ausgegeben werden, wenn sie einem bestimmten
#Spaltenwert entsprechen/größer/kleiner sind

def zeilenFiltern(df,spaltenname,wert,operator):
    if(operator=='>'):
        df_maske = df['spaltenname'] > wert
        filtered_df = df[df_maske]
        return filtered_df
    elif (operator == '<'):
        df_maske = df['spaltenname'] < wert
        filtered_df = df[df_maske]
        return filtered_df
    elif (operator == '=='):
        df_maske = df['spaltenname'] == wert
        filtered_df = df[df_maske]
        return filtered_df




#print(zeilenFilternGroesserWert(df,Alter,50,>))

spaltenFiltern_df = df[['Name', 'Alter', 'Gehalt']]
print(spaltenFiltern_df, "\n")

def spaltenFiltern(df,liste):
    spaltenFiltern_df = df[liste]
    return spaltenFiltern_df
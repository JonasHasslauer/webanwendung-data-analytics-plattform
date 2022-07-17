import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def initialisierungSeaborn():
    """
    Mit dieser Funktion soll seaborn initialisiert werden
    hierfür wird ein kleines Balkendiagramm mit "zufalligen" Werten erstellt
    Einen weiteren Nutzen hat diese Funktion nicht
    """
    try:
        df = pd.DataFrame({'Stadt':["Diebach","Hammelburg"],
                           'Anzahl Dönerbuden': [222,444]})
        df.head()
        sns.set(rc={'figure.figsize':(10,12)})
        ax = sns.barplot(y='Stadt',x='Anzahl Dönerbuden', data=df,palette='rocket')


        initialx=0
        for p in ax.patches:

            ax.text(p.get_width(),initialx+p.get_height()/8,'{:1.0f}'.format(p.get_width()))

            initialx += 1



        plt.show()

    except Exception as e:
        print("Oopsidupsi! ", e.__class__, "ist aufgetreten.")

initialisierungSeaborn()
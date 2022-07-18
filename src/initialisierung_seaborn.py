import pandas as pd
import seaborn as sns

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np



text_2 ="""
Die Bezeichnung „Wiener Schnitzel“ wurde im 19. Jahrhundert geprägt, sie findet sich bereits in Maria Anna Neudeckers Allerneuestem allgemeinen Kochbuch von 1831 als „Wiener Schnitzel von Kalbfleisch“.[1] In dem damals weit verbreiteten Kochbuch Die Süddeutsche Küche der Grazerin Katharina Prato wird das Gericht noch in der 26. Auflage von 1897 zwar unter den „Kalbsschnitzchen“ aufgeführt, jedoch lediglich als „eingebröselte Schnitzchen“ bezeichnet.[2] In der 34. Auflage von 1903 findet sich der Ausdruck „Wiener Schnitzel“ als nachgestellte alternative Bezeichnung; der oberdeutsche Diminutiv „Schnitzel“ wird, anders als bei Neudecker, auch nur in diesem Namen verwendet, ansonsten ist durchgehend von Schnitzchen die Rede.[3]

Möglicherweise geht das Wiener Schnitzel auf das Cotoletta alla milanese in Oberitalien zurück, das ähnlich aus etwas dickeren Koteletts zubereitet wird und im 14. oder 15. Jahrhundert seinen Weg nach Wien fand. Diese Hypothese ist jedoch nicht belegt.[4]

Einer Legende zufolge soll Feldmarschall Radetzky das Rezept 1857 aus Italien mitgebracht haben. Der Sprachforscher Heinz-Dieter Pohl hat 2007 jedoch schlüssig nachgewiesen, dass diese Geschichte erfunden ist.[5] Radetzky wurde laut Pohl erst im Jahr 1969 in dem italienischen Gastronomieführer Guida gastronomica d'Italia, der 1971 unter dem Titel Italien tafelt auf deutsch erschien, mit dem Schnitzel in Zusammenhang gebracht. Dort wurde behauptet, es handele sich eigentlich um das cotoletta alla milanese; vorher sei davon in Österreich nie die Rede gewesen. Ein Graf Attems, Flügeladjutant des österreichischen Kaisers Franz Joseph, habe einen Bericht von Radetzky über die Lage in der Lombardei weitergegeben und in einer Randnotiz ein köstliches paniertes Kalbskotelett erwähnt. Nach Radetzkys Rückkehr habe der Kaiser ihn persönlich um das Rezept gebeten.[6] Pohl kommentiert diese Anekdote mit den Worten: „Wissenschaftlich ist diese Geschichte belanglos, sie enthält keinerlei Quellenangaben und sie wird in der Literatur von und über Radetzky […] nicht erwähnt. In keinem biografischen Werk über die Monarchie erscheint ein Graf Attems, der dieser Zeit und Position entspräche.“[7] Pohl bezweifelt, dass das Wiener Schnitzel überhaupt aus Italien übernommen wurde und begründet dies damit, dass bei anderen „importierten Speisen“ der österreichischen Küche immer der Originalbegriff beibehalten wurde, wenn auch in eingedeutschter Form, etwa bei Gulasch oder Palatschinken, und das Schnitzel auch in Spezialkochbüchern zur italienischen Küche nicht erwähnt werde.[8] Er verweist überdies darauf, dass es schon vor dem Schnitzel in der Wiener Küche mehrere Speisen gab, die paniert und in Fett schwimmend gebacken wurden, vor allem das bekannte Backhendl, das erstmals 1719 in einem Kochbuch erwähnt wird. Das ebenso zubereitete Schnitzel sei Ende des 19. Jahrhunderts dann analog zum Wiener Backhendl als Wiener Schnitzel bezeichnet worden.[6]

Prato erwähnte bereits 1879 mehrere italienische Gerichte wie Makkaroni, Risi e bisi und Risotto, aber kein Cotoletta.[6] Teilweise wird auch die ebenso unbelegte Variante genannt, dass eine byzantinische Prinzessin das panierte und gebackene Schnitzel an den Babenberger Hof nach Wien gebracht habe. 
"""



text_3 ="test"



def wordcloudErstellen(text):
    """
    Mit dieser Funktion soll seaborn initialisiert werden
    hierfür wird ein kleines Wordclouddiagramm erstellt
    Einen weiteren Nutzen hat diese Funktion nicht
    :param text: text der übergeben wird
    """
    try:
        nichtinteressant = "und von Der das den wir ist die auf im wird"
        liste_der_unerwuenschten_woerter = nichtinteressant.split()

        STOPWORDS.update(liste_der_unerwuenschten_woerter)
        x, y = np.ogrid[:1000, :1000]

        mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 ** 2
        mask = 255 * mask.astype(int)

        wordcloud = WordCloud(background_color="white", width=1920, height=1080, mask=mask).generate(text)
       # plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        #plt.show()
    except Exception as e:
        print("Oopsidupsi! ", e.__class__, "ist aufgetreten.")

#wordcloudErstellen(text_2)
wordcloudErstellen(text_3)

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



        #plt.show()

    except Exception as e:
        print("Oopsidupsi! ", e.__class__, "ist aufgetreten.")

initialisierungSeaborn()
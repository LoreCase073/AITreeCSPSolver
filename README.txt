Nella cartella MapColoring_TreeCSPSolver saranno presenti 
il file main.py con il codice e vari file .csv che contengono 
vari dati raccolti da varie prove.

L'implementazione dell'algoritmo � ispirata all'esempio di pseudocodice 
nel libro Artificial Intelligence a Modern Approach, capitolo 6.5 e per
la creazione del della mappa invece ho seguito l'approccio
del solito libro, nell'esercizio 6.10. Alla risoluzione dei problemi
di intersezione ho invece deciso di seguire un approccio proposto 
dalla pagina web 
https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
con alcuni accorgimenti personali
per far tornare un grafo come desiderato. Lo stesso algoritmo veniva
proposto su un libro di algoritmi, del quale per� non ricordo il nome
(a tal proposito ho proposto il sito internet in cui viene spiegato
con la stessa modalit�).

Per far partire i test basta modificare il range in cui far girare i test
(si consiglia un intervallo tra 10 e 200 non aspettare troppo per la
creazione dei grafi) e modificare la variabile domains all'interno,
con il numero di colori che si vogliono considerare nel problema del map
coloring.
A quel punto verranno fatti partire i vari test e i risultati verranno
salvati su un file di estensione .csv, al quale si pu� modificare
il nome per anche crearne altri, semplicemente modificando
il nome all'interno di with open('nome.csv', mode='a') as dataFile:

Nel caso si scelga un file gi� esistente i dati verranno appesi
a quelli gi� esistenti.

Modificato ci�, basta far partire il main del file main.py.
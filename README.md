# scrape
Network analisys for 500px website.

# Disclaimer
All the analysis, docs and analysis' results are in Italian. Sorry :(

# Todo for the project

 1. Login tramite script al social network -> python, scrapy
 2. Estrapolazione dei dati tramite API o tramite Scraping --> python, scrapy
 3. Inserimento dei dati in un database (es. sqlite o mongodb) --> scrapy, sqlite3 / pymongo, mongod
 4. Creazione del grafo della network (non orientato/orientato/pesato) --> networkx
 5. Salvataggio del grafo in formato .gexf (per poi aprirlo con il software Gephi)
 6. Distribuzione del grado della rete: PDF, CDF, CCDF e visualizzazione dei grafici --> matplotlib

Poi, in base alle caratteristiche della rete che si vogliono analizzare:

 - statistiche puntuali: media, moda, mediana, grado massimo, grado minimo --> numpy
 - Confronto della rete con una rete random Erdos-Renyi --> networkx
 - identificazione degli hub --> numpy
 - reciprocità
 - Misure di centralità:
	 - Degree centrality: degree, in-degree, out-degree
	 - Normalizzazione del grado
	 - Eigenvector centrality
	 - Katz centrality
	 - Page Rank
	 - Betweennees centrality
	 - Closeness centrality
	 - Structural equivalence (Jaccard, Cosine)
 - Identificazione delle componenti 
 - Altro

# Evaluation criteria

 1. Data collection (Raccolta Dati):
	- Base: Utilizzo di un dataset già disponibile
	- Intermedio: Utilizzo di API supportate da moduli Python adeguatamente documentati
	- **Avanzato: Utilizzo di API scarsamente supportate da moduli Python, Raccolta dati utilizzando web scraping e focused crawler**

 2. Analisi:
	- Base: analisi delle proprietà fondamentali di una rete (cfr. articolo su analisi di Twitter o Facebook, escluso ANF ed avearge shortest path)
	- Intermedio: analisi delle proprietà fondamentali di una rete, analisi assortatività per attributo, community detection (intermedio/avanzato)
	- **Avanzato: analisi precedenti + Implementazione di misure/algoritmi non presenti in Networkx, Analisi delle relazioni tra ulteriore oggetti (commenti, elementi testuali, foto, video, informazioni geografiche, informazioni sugli account, etc.. ) e la struttura della rete**

 3. Commenti sul'analisi effettuata:
	- Base: statistiche descrittive e confronto con altre reti simili
	- Intermedio: statistiche descrittive e analisi critica rispetto alle nozioni viste nelle lezioni di teoria
	- **Avanzato: intermedio + discussione originale su alcuni/tutti i risultati ottenuti.**

 4. Dimensione del dataset (valutato in caso di data collection intermedia o avanzata):
	- Numero di nodi, archi del grafo
	- Numero di elementi/oggetti utilizzati nell'analisi intermedia/avanzata
	- Utilizzo di framework per la manipolazione di Big Data (Apache Spark, Hadoop)
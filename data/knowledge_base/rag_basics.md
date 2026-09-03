# RAG basics

Retrieval-Augmented Generation combine deux etapes: rechercher des informations pertinentes dans une base documentaire, puis demander a un modele de langage de produire une reponse a partir de ces informations. Cette approche est utile quand les connaissances changent souvent ou quand l'entreprise possede des documents internes qui ne sont pas dans les donnees d'entrainement du modele.

Une pipeline RAG classique contient l'ingestion des documents, le nettoyage, le chunking, la creation d'index, le retrieval, la construction du prompt, la generation et la citation des sources. Le modele ne doit pas inventer une reponse si le contexte retrouve ne contient pas l'information demandee.

Le principal avantage est la reduction des hallucinations. Un autre avantage est la separation entre la connaissance et le modele: on peut mettre a jour les documents sans reentrainer le LLM.

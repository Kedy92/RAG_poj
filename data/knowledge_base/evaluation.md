# Evaluation RAG

Evaluer un systeme RAG demande de mesurer le retrieval et la generation. Pour le retrieval, on peut utiliser precision@k, recall@k, mean reciprocal rank et taux de couverture des documents attendus. Pour la generation, on mesure la pertinence, la factualite, la groundedness et la presence de citations correctes.

Les erreurs frequentes sont un mauvais chunking, un index incomplet, des documents obsoletes, un prompt trop permissif et l'absence de verification des sources. Une bonne evaluation contient un jeu de questions, des reponses attendues et les passages qui devraient etre retrouves.

Le monitoring en production doit suivre la latence, le cout, les questions sans reponse, les sources utilisees et les retours utilisateurs.

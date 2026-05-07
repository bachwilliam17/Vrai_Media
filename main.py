from get_articles import get_articles, get_description_articles, get_articles_string
from IA_prompts import prompt_IA
from get_points_de_vue import get_points_de_vue

import json

# Recuperer tous les articles
medias_data_json = "flux_rss_medias.json"
articles = get_articles(medias_data_json)

# Recuperer la version textuelle des articles pour le prompt IA
articles_string = get_articles_string(articles)
with open('descriptions_articles.txt', 'w') as f:
    f.write(articles_string)

# Recuperer la liste des sujets majeurs avec l'IA
with open('prompts/prompt_sujets.txt', 'r') as f:
    prompt_sujets = f.read()
sujets = prompt_IA(prompt_sujets, articles_string)
print("\nSujets majeurs recuperes.")
with open("liste_sujets.txt", 'w') as f:
    f.write(sujets)
raise ValueError

# Recuperer la synthese des points de vue pour chaque camp avec l'IA
articles_descriptions = get_description_articles(articles)
with open('prompts/prompt_synthese.txt', 'r') as f:
    prompt_synthese = f.read()
pdv = get_points_de_vue(sujets, articles_descriptions, prompt_synthese)

for sujet in sujets['sujets']:
    print(f"\nSujet {sujet}:")
    print(f"Droite: {pdv[sujet]['droite']}")
    print(f"Gauche: {pdv[sujet]['gauche']}")

print("\nExecution terminee.")
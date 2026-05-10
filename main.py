import sys
sys.path.append("/Users/williambach/Documents/Python Library")

from IA_prompts import prompt_IA
from get_articles import get_articles, get_description_articles, get_articles_string
from get_points_de_vue import get_points_de_vue

import json

# Recuperer tous les articles
medias_data_json = "flux_rss_medias.json"
articles = get_articles(medias_data_json)

# Recuperer la version textuelle des articles pour le prompt IA
#articles_string = get_articles_string(articles)
#with open("outputs/titres_articles.txt", 'w') as f:
#    f.write(articles_string)

# Recuperer la liste des sujets majeurs avec l'IA
#with open('prompts/prompt_sujets.txt', 'r') as f:
#    prompt_sujets = f.read()
#sujets = prompt_IA("gpt-5.4-mini", prompt_sujets, articles_string)
print("\nSujets majeurs recuperes.")

# Enregistrer la liste des sujets
#with open("outputs/liste_sujets.txt", 'w') as f:
#    f.write(sujets)

with open('liste_sujets.txt', 'r') as f:
    sujets = f.read()
sujets_dict = json.loads(sujets)

# Recuperer la synthese des points de vue pour chaque camp avec l'IA
articles_descriptions = get_description_articles(articles)
with open('prompts/prompt_synthese.txt', 'r') as f:
    prompt_synthese = f.read()
pdv = get_points_de_vue(sujets_dict, articles_descriptions, prompt_synthese)

with open("outputs/synthese_sujets.txt", 'w') as f:
    for sujet in sujets_dict['sujets']:
        nom_sujet = sujet['nom_sujet']

        if nom_sujet in pdv:
            f.write(f"\n\nSujet {nom_sujet}:")
            f.write(f"\nDroite: {pdv[nom_sujet]['droite']}")
            f.write(f"\nGauche: {pdv[nom_sujet]['gauche']}")

print("\nExecution terminee.")
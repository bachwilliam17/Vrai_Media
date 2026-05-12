import sys
sys.path.append("/Users/williambach/Documents/Python Library/LLM Requests")
from IA_prompts import prompt_IA


"""
    Recuperer les descriptions des articles a partir de leur ID 
    sous forme de texte
"""
def get_desc_sujet_string(id_articles, desc_articles):
    desc_sujet = ""

    # Parcourir chaque article
    for article in id_articles:
        # Rajouter la description de l'article actuel
        desc = desc_articles.get(article['id_article'])
        if desc is not None:
            desc_sujet += f"\nArticle: "
            desc_sujet += f"{desc}."

    return desc_sujet


"""
    Recuperer le point de vue d'un bord politique grace a une requete LLM
"""
def get_pdv(desc_sujet, prompt_synthese):
        # Recuperer le point de vue general avec une requete LLM
        if "Article" in desc_sujet:
            return prompt_IA(
                "gpt-5.4-mini", 
                prompt_synthese, 
                desc_sujet
            )
        else:
            return None


"""
    Generer une synthese des points de vue de chaque bord politique 
    pour tous les sujets d'actualite
"""
def get_points_de_vue(sujets, desc_articles, prompt_synthese):
    print("\nRecuperation de la synthese des points de vue pour chaque camp ..")
    points_de_vue = {}

    # Parcourir les sujets d'actualite
    for sujet in sujets['sujets']:

        # Verifier qu'il y a au moins 6 descriptions d'articles
        articles_count = len(sujet['droite']) + len(sujet['gauche'])
        if articles_count > 5:
            # Construire un input avec les descriptions d'articles
            desc_articles_string = "## DONNÉES D'ENTRÉE"

            desc_articles_string += "\n\nDROITE"
            desc_articles_string += get_desc_sujet_string(sujet['droite'], desc_articles)

            desc_articles_string += "\n\nGAUCHE"
            desc_articles_string += get_desc_sujet_string(sujet['gauche'], desc_articles)

            # Recuperer le sujet actuel
            nom_sujet = sujet['nom_sujet']
            points_de_vue[nom_sujet] = {}

            # Recuperer le point de vue de la droite
            pdv = get_pdv(desc_articles_string, prompt_synthese)
            points_de_vue[nom_sujet] = pdv
            
            # Recuperer le point de vue de la gauche
            pdv_gauche = get_pdv(sujet['gauche'], desc_articles, prompt_synthese)
            points_de_vue[nom_sujet]['gauche'] = pdv_gauche
    
    print("\nPoints de vue pour chaque camp recuperes.")
    return points_de_vue
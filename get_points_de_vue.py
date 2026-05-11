import sys
sys.path.append("/Users/williambach/Documents/Python Library/LLM Requests")
from IA_prompts import prompt_IA


"""
    Recuperer le point de vue d'un bord politique grace a une requete LLM
"""
def get_pdv(id_articles, desc_articles, prompt_synthese):
    # Construire un input avec les descriptions d'articles
        desc_articles_string = "## DONNÉES D'ENTRÉE"
        n = 1

        for article in id_articles:
            # Rajouter la description de l'article actuel
            desc = desc_articles.get(article['id_article'])
            if desc is not None:
                desc_articles_string += f"\nArticle {n}: "
                desc_articles_string += f"{desc}."
                n += 1

        # Recuperer le point de vue general avec une requete LLM
        if "Article" in desc_articles_string:
            return prompt_IA(
                "gpt-5.4-mini", 
                prompt_synthese, 
                desc_articles_string
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
            # Recuperer le sujet actuel
            nom_sujet = sujet['nom_sujet']
            points_de_vue[nom_sujet] = {}

            # Recuperer le point de vue de la droite
            pdv_droite = get_pdv(sujet['droite'], desc_articles, prompt_synthese)
            points_de_vue[nom_sujet]['droite'] = pdv_droite
            
            # Recuperer le point de vue de la gauche
            pdv_gauche = get_pdv(sujet['gauche'], desc_articles, prompt_synthese)
            points_de_vue[nom_sujet]['gauche'] = pdv_gauche
    
    print("\nPoints de vue pour chaque camp recuperes.")
    return points_de_vue
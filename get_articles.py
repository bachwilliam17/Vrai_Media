import feedparser
import requests
import json

#-------------------------         FLUX RSS         -------------------------

# Config pour API de lecture des flux RSS
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# Recuperer la liste des flux RSS pour chaque media
def get_medias_data(medias_data_json):
    with open(medias_data_json, 'r') as f:
        flux_rss_json = json.load(f)
    return flux_rss_json['medias']



#-----------------------    TRAITEMENT DES ARTICLES    -----------------------

# Recuperer tous les titres d'articles pour chaque media
def get_articles(medias_data_json):
    articles_dict = {}
    articles_dict['medias'] = []
    n = 1

    for media in get_medias_data(medias_data_json):
        # Enregistrer le media actuel
        journal = media['nom_journal']
        journal_dict = {}
        journal_dict['journal'] = journal
        journal_dict['orientation'] = media['orientation']
        journal_dict['articles'] = []

        # Tenter de lire le contenu du flux RSS du media 
        url = media['url']
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue
        response.raise_for_status()

        # Parcourir les articles
        feed = feedparser.parse(response.text)

        if len(feed.entries) > 0:
            for entry in feed.entries:
                # Enregistrer l'article actuel
                article_dict = { 
                    "id": f"{n}", 
                    "titre": f"{entry.title}",
                    "description": f"{entry.description}"
                }

                n += 1
                journal_dict['articles'].append(article_dict)
        
        articles_dict['medias'].append(journal_dict)

    print("\nTitres des articles recuperes pour chaque media.")
    return articles_dict



# Retourne un dict avec les descriptions des articles associees a leur id
def get_description_articles(articles_dict):
    description_articles = {}
    
    # Parcourir les medias
    for media in articles_dict['medias']:
        # Parcourir les articles de chaque media
        for article in media['articles']:
            # Seulement enregistrer l'ID et la description
            if article['description'] != "":
                description_articles[article['id']] = article['description']

    return description_articles



# Retourne une version textuelle des titres des articles de journal
def get_articles_string(articles):
    # Introduction
    articles_string = "## DONNÉES D'ENTRÉE"
    articles_string += "\n\n<titres>"

    for media in articles['medias']:
        # Journal et orientation
        articles_string += "\n\n\n<journal>"
        articles_string += f"\n{media['journal']}"
        articles_string += f"\n{media['orientation']}"

        # Articles invidividuels
        for article in media['articles']:
            articles_string += f"\n{article['id']}. {article['titre']}"

        articles_string += "\n</journal>"
    
    articles_string += "\n\n</titres>"
    print("\nVersion textuelle des articles recuperes.")
    return articles_string
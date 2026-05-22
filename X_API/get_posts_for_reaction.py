import tweepy
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

# X API Setup
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
client = tweepy.Client(bearer_token=BEARER_TOKEN)


### CIBLAGE DES CHAÎNES

GAUCHE = [
    "manonbril", 
    "jeanmassiet", 
    "fibretigre", 
    "clemovitch",
    "TwitchDroitard"
]

DROITE = [
    "JRochedy", 
    "baptistentx", 
    "Shadoune", 
    "papacito021", 
    "Valek", 
    "GWGoldnadel",
    "idrissaberkane",
    "HommesInfluence",
    "lelapindufutur",
    "RaptorVsWild",
    "TwitchGauchiste"
]

TARGET_USERS = DROITE + GAUCHE


### LECTURE DES POSTS

"""
    Get 1 user's list of posts
"""
def get_user_posts(username, start_date, max_results):

    # Get User ID from poster
    user = client.get_user(username=username)
    if not user.data:
        print(f"{username} not found.")
        return None
    user_id = user.data.id

    # Get posts list
    response = client.get_users_tweets(
        user_id,
        max_results=max_results,
        start_time=start_date,
        tweet_fields=['created_at','public_metrics','context_annotations']
    )
    if not response.data or len(response.data) == 0:
        print(f"No posts found for {username}")
        return None

    return response.data
        

"""
    Get custom set of data from posts for a list of users
"""
def get_posts_data(usernames, start_date, max_results):

    report = []

    # Visit all users
    for username in usernames:

        # Get posts list from the user
        posts = get_user_posts(username, start_date, max_results)
        if not posts:
            continue 

        # Visit all posts
        for post in posts:

            # Gather post details
            post_metrics = post.public_metrics
            report.append({
                "Profil": username,
                "Post ID": post.id,
                "Text": post.text,
                "Created at": post.created_at,
                "Likes": post_metrics['like_count'],
                "Reposts": post_metrics['retweet_count']
            })
    
    return report

"""
    Get textual report presenting posts data
"""
#def get_posts_report(posts_data):


start_time = datetime.utcnow() - timedelta(hours=24)
report = get_posts_report(TARGET_USERS, start_time, 30)
for item in report:
    print(f"\n{item['Profil']} | {item['Created at']} | ❤️ {item['Likes']} RT {item['Reposts']}")
    print(item['Text'][:200] + "..." if len(item['Text']) > 200 else item['Text'])
    print("\n")

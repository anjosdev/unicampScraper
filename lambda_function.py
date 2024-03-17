import json
import praw
import unicamp_scraper
# Credentials
import config

def lambda_handler(event, context):
    # Define the URL of the website to scrape
    url_news = "https://www.jornal.unicamp.br/noticias/#gsc.tab=0"
    url_institutional_news = "https://www.unicamp.br/noticias-institucionais/noticias/#gsc.tab=0"
    url_events = "https://www.jornal.unicamp.br/eventos/#gsc.tab=0"
    
    posts = []
    posts.extend(unicamp_scraper.scrape_unicamp(url_news))
    posts.extend(unicamp_scraper.scrape_unicamp(url_institutional_news))
    posts.extend(unicamp_scraper.scrape_unicamp(url_events))
    
    # Reddit
    # Reddit API credentials
    reddit_client_id = config.client_id
    reddit_client_secret = config.client_secret
    reddit_username = config.username
    reddit_password = config.password
    user_agent = config.user_agent
    
    # Initialize PRAW with your Reddit API credentials
    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_client_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent=user_agent)
    
    # Subreddit where you want to post
    subreddit = reddit.subreddit('unicamp')
    
    # Function to check if the URL has already been posted
    def url_not_posted(url):
        for submission in subreddit.new(limit=None):
            if submission.url == url:
                return False
        return True
    
    # Loop through each post in the array
    for post in posts:
        # Check if the URL has not already been posted
        if url_not_posted(post['link']):
            # Create the post
            title = post['title']
            url = post['link']
            subreddit.submit(title=title, url=url)
            print(f"Posted: {title}")
        else:
            print(f"Skipped: {post['title']} (URL already posted)")
    
    print("===FINISHED===")
    return True

lambda_handler("", "")

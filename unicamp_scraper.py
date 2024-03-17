from bs4 import BeautifulSoup
import requests

def scrape_unicamp(url):
    posts = []
    response = requests.get(url)
    if response.status_code == 200:
        if '/eventos/' in url:
            soup = BeautifulSoup(response.text, "html.parser")
            # Find all elements with class 'component-calendar-day-event__header__title'
            events = soup.find_all(class_='component-calendar-day-event__header__title')
            # Loop through each event and extract the desired information
            for event in events:
                title = event.get_text(strip=True)
                link = event['href']
                # date = ?
                print("Scrapped:", title)
                post = {
                        'title': title,
                        'link': link
                    }
                posts.append(post)
        else: # if '/noticias/' in url or '/noticias-institucionais/' in url
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all elements with class 'post-cards__single-post'
            news = soup.find_all(class_='post-cards__single-post')
            # Loop through each post and extract the desired information
            for unique_news in news:
                # Extracting information
                title = unique_news.find(class_='post-cards__single-post__info-wrapper__title__title').text.strip()
                link = unique_news.find('a')['href']
                date = unique_news.find(class_='post-cards__single-post__info-wrapper__date__date').text.strip()
                print("Scrapped:", title)
                post = {
                        'title': title,
                        'link': link,
                        'date': date
                    }
                posts.append(post)
    else:
        print("Failed to scrape website")
    return posts

scrape = scrape_unicamp("https://www.jornal.unicamp.br/noticias/#gsc.tab=0")
print(scrape)

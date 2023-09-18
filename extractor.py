import requests
from bs4 import BeautifulSoup

def extract_page_articles(articles_list):
    page_articles = []
    for article in articles_list:
        title = article.find('h3').text.strip()
        link = article.find('a')['href']
        #print("Interating through article " + title + " at link " + link)
        article_opener_and_text = get_article_opener_and_text(link)
        page_articles.append({"title" : title, "link" : link,
                                                       "opener" : article_opener_and_text[0],
                                                       "text" : article_opener_and_text[1]})
    return page_articles
        
def get_article_opener_and_text(link):
    articles_soup = BeautifulSoup(requests.get(link).text, "html.parser")
    article_opener_element = articles_soup.find('div', class_ = "opener")
    #Add if statement if the text does not exist
    article_opener = (article_opener_element.get_text(separator=' ').strip().replace('\n', '').replace('\r', '').replace('\t', '')
                      if article_opener_element else "")
    article_text_element = articles_soup.find('div', id = "art-text")
    article_text = (article_text_element.get_text(separator=' ').strip().replace('\n', '').replace('\r', '').replace('\t', '')
                    if article_text_element else "")
    return (article_opener, article_text)

def save_articles_to_file(articles, found_words):
    with open('news/aritcles_words.txt', 'w') as f:
        for article, article_words in zip(articles, found_words):
            #print(article_words)   
            f.write("Title: " + article["title"] + '\n')
            f.write("Link: " + article["link"] + '\n')
            f.write("Found words: " + ' '.join(article_words) + '\n')
            f.write("Abstract: " + article["opener"] + '\n')
            f.write("Text: " + article["text"] + '\n')
            f.writelines('\n')


articles_with_word = []
articles_found_words = []
start_page = 1
end_page = 100
for i in range(start_page, end_page + 1):
    searched_words = ["Holandsk", "Maas", "Nizozem"]
    print("Interating through page " + str(i))
    news_url = f"https://www.idnes.cz/zpravy/archiv/{i}?datum=&idostrova=idnes"
    links_soup = BeautifulSoup(requests.get(news_url).text, "html.parser")
    articles_list = links_soup.find_all('div', class_ = "art")
    page_articles = extract_page_articles(articles_list)
    for article in page_articles:
        searched_word_in_opener = any(word in article['opener'] for word in searched_words)
        searched_word_in_text = any(word in article['text'] for word in searched_words)
        if searched_word_in_opener or searched_word_in_text:
            found_words_in_text = [word for word in searched_words if word in article['text']]
            articles_found_words.append(found_words_in_text)
            articles_with_word.append(article)
            #print("Found a word!")
    save_articles_to_file(articles_with_word, articles_found_words)
    
#news_url = "https://www.idnes.cz/zpravy/archiv/1?datum=&idostrova=idnes"

        
        #print(article.keys())
        #print(f"Title: {article['title']}")
        #print(f"Link: {article['link']}")
        #print(f"Opener: {article['opener']}")
        #print(f"Body text: {article['text']}")
        #print()
import time
from selenium import webdriver
from newspaper import Article
import articleDateExtractor

if __name__ == "__main__":

    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get('https://markets.businessinsider.com/news/aapl')

    page_numbers = driver.find_element_by_class_name("finando_paging").text

    #get the last page number
    last_page = int(page_numbers.split('|')[-1])

    current_page = 1
    while last_page > current_page:

        #get the links for all the posts on the current page
        posts = [p.get_attribute("href") for p in driver.find_elements_by_class_name("news-link")]

        #for every posts visit and abstract the information
        for p in posts:
            try:
                article = Article(p)
                article.download()
                article.parse()

                print("-------")
                print(article.title)
                print(article.text)
                print(article.publish_date)
                print(article.authors)

                if not article.publish_date:
                    print("Don't add it do the DB")

            except:
                print("Something went wrong -> Page Number:" + str(current_page) + " url: " + str(p))

            time.sleep(2)

        current_page += 1
        driver.get('https://markets.businessinsider.com/news/aapl?p={}'.format(current_page))

    driver.quit()

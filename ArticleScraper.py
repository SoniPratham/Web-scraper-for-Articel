import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
from datetime import date
import datetime

class ArticleScraper:
    def __init__(self, url):
        self.url = url

    def fetch_articles(self):
        # send a GET request to the URL
        response = requests.get(self.url)

        # parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # find all articles on the page
        articles = soup.find_all('ol', class_='relative')

        # create a list to store the article data
        article_list = []

        # loop through each article and extract the headline, URL, author, and date
        for article in articles[0].find_all("li"):
            headline = article.find("a", class_="group-hover:shadow-underline-franklin").text.strip()
            url = "https://www.theverge.com"+article.find("a")["href"]
            author = article.find("a", class_="text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8").text.strip()
            date = article.find("span", class_="text-gray-63 dark:text-gray-94").text.strip()
            article_list.append([url, headline, author, date])

        return article_list

    def save_articles_to_csv(self, article_list):
        # generate the filename for the CSV file
        today = datetime.date.today().strftime("%d%m%Y")
        filename = f"{today}_verge.csv"

        # write the article data to a CSV file
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["id", "URL", "headline", "author", "date"])
            for i, article in enumerate(article_list):
                csvwriter.writerow([i+1, article[0], article[1], article[2], article[3]])

    def save_articles_to_database(self, article_list):
        # create a SQLite database and table to store the article data
        conn = sqlite3.connect("verge_articles.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, URL TEXT, headline TEXT, author TEXT, date TEXT)")

        # execute the SQL query to count the rows in the article table
        c.execute('SELECT COUNT(*) FROM articles')

        # fetch the result
        result = c.fetchone()

        i=result[0]

        # insert the article data into the SQLite database
        for article in article_list:
            i=i+1
            c.execute("INSERT INTO articles (id, URL, headline, author, date) VALUES (?, ?, ?, ?, ?)",
                    (i, article[0], article[1], article[2], article[3]))

        # commit the changes and close the database connection
        conn.commit()
        conn.close()

if __name__ == "__main__":
    url = "https://www.theverge.com/"
    scraper = ArticleScraper(url)
    article_list = scraper.fetch_articles()
    scraper.save_articles_to_csv(article_list)
    scraper.save_articles_to_database(article_list)

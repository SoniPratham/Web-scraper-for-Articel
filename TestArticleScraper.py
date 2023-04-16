import unittest
import datetime
import csv
import sqlite3
from ArticleScraper import ArticleScraper

class TestArticleScraper(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.theverge.com/"
        self.scraper = ArticleScraper(self.url)
        self.article_list = self.scraper.fetch_articles()

    def test_fetch_articles(self):
        self.assertIsNotNone(self.article_list)
        self.assertIsInstance(self.article_list, list)

        for article in self.article_list:
            self.assertIsNotNone(article[0])
            self.assertIsNotNone(article[1])
            self.assertIsNotNone(article[2])
            self.assertIsNotNone(article[3])

            self.assertIsInstance(article[0], str)
            self.assertIsInstance(article[1], str)
            self.assertIsInstance(article[2], str)
            self.assertIsInstance(article[3], str)

    def test_save_articles_to_csv(self):
        filename = datetime.date.today().strftime("%d%m%Y") + "_verge.csv"
        self.scraper.save_articles_to_csv(self.article_list)

        with open(filename, "r", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            rows = list(csvreader)

            self.assertEqual(rows[0], ["id", "URL", "headline", "author", "date"])

            for i, article in enumerate(self.article_list):
                self.assertEqual(rows[i+1], [str(i+1), article[0], article[1], article[2], article[3]])

    def test_save_articles_to_database(self):
        # fetch the articles and save them to the database
        article_list = self.scraper.fetch_articles()
        self.scraper.save_articles_to_database(article_list)

        # query the database to retrieve the articles
        conn = sqlite3.connect("verge_articles.db")
        c = conn.cursor()
        c.execute("SELECT * FROM articles")
        rows = c.fetchall()

        # check that the number of rows in the table is equal to the number of articles
        self.assertEqual(len(article_list), len(rows))

        # check that the articles in the table match the articles in the article_list
        for i, row in enumerate(rows):
            self.assertEqual(row[1], article_list[i][0])
            self.assertEqual(row[2], article_list[i][1])
            self.assertEqual(row[3], article_list[i][2])
            self.assertEqual(row[4], article_list[i][3])

        # close the database connection
        conn.close()


if __name__ == "__main__":
    unittest.main()

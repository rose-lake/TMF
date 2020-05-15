from selenium import webdriver
from TMF.models import Article, Author
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestLandingPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome("/usr/local/bin/chromedriver")

    def tearDown(self):
        self.browser.close()

    def test_jumbo_article_is_displayed(self):
        self.browser.get(self.live_server_url + reverse("home"))

        # # pause for 15 seconds so we can see the page load
        # time.sleep(15)

        # grab jumbo_article 'first paragraph' section and assert a <p> tag exists
        jumbo_article = self.browser.find_element_by_css_selector('section.jumbo-card > div.card-elements > div.card-copy')
        self.assertTrue(jumbo_article.find_element_by_tag_name('p'))
        # # tested wrong way to make sure it works! yes, it worked. this failed:
        # self.assertFalse(jumbo_article.find_element_by_tag_name('p'))

    def test_first_random_article_displayed(self):
        self.browser.get(self.live_server_url + reverse("home"))
        random_article = self.browser.find_element_by_css_selector('div.cards.row > div:nth-child(1) > div.card-elements > div.card-copy')
        self.assertTrue(random_article.find_element_by_tag_name('p'))
        # # write a failing test case on purpose to be sure it works. it does.
        # self.assertTrue(random_article.find_element_by_tag_name('h1'))

    def test_second_random_article_displayed(self):
        self.browser.get(self.live_server_url + reverse("home"))
        random_article = self.browser.find_element_by_css_selector('div.cards.row > div:nth-child(2) > div.card-elements > div.card-copy')
        self.assertTrue(random_article.find_element_by_tag_name('p'))

    def test_third_random_article_displayed(self):
        self.browser.get(self.live_server_url + reverse("home"))
        random_article = self.browser.find_element_by_css_selector('div.cards.row > div:nth-child(3) > div.card-elements > div.card-copy')
        self.assertTrue(random_article.find_element_by_tag_name('p'))

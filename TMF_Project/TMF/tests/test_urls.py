from django.test import SimpleTestCase
from django.urls import reverse, resolve
from TMF.views import home, article_detail, add_comment_to_article

class TestUrls(SimpleTestCase):
    # use SimpleTestCase anytime you don't need to interact with the database

    def test_home_url_resolves(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func, home)

    def test_article_detail_url_resolves(self):
        # this doesn't need to be a valid pk in our database, just any int,
        # for testing this simple case that the url resolves
        url = reverse("article_detail", args=[1])
        self.assertEqual(resolve(url).func, article_detail)

    def test_add_comment_to_article_url_resolves(self):
        url = reverse("add_comment_to_article", args=[1])
        self.assertEqual(resolve(url).func, add_comment_to_article)

from django.db import models
from django.utils import timezone



class Author(models.Model):
    byline = models.CharField(max_length=300)
    email = models.EmailField()
    username = models.CharField(max_length=300)
    uuid = models.CharField(max_length=300)

    def __str__(self):
        return self.username


class Article(models.Model):
    authors = models.ManyToManyField(Author, related_name='articles')
    body_extras = models.TextField()
    body_first_p = models.TextField(blank=True)
    byline = models.CharField(max_length=300)
    disclosure = models.TextField()
    headline = models.CharField(max_length=300)
    image_url = models.CharField(max_length=500, blank=True)
    modified = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=300)
    promo = models.TextField()
    sfr_content = models.TextField(blank=True)
    uuid = models.CharField(max_length=300)

    # for testing purposes
    # test = models.TextField(blank=True)

    def __str__(self):
        return self.headline


class Comment(models.Model):
    article = models.ForeignKey('TMF.Article',
                                on_delete=models.CASCADE,
                                related_name='comments')
    author = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return self.text


class Quote(models.Model):

    change_dollar = models.DecimalField(max_digits=10, decimal_places=2)
    change_is_positive = models.BooleanField()
    change_percent = models.DecimalField(max_digits=5, decimal_places=2)
    company_name = models.CharField(max_length=50)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    detail_url = models.CharField(max_length=500, blank=True)
    exchange = models.CharField(max_length=25)
    image_url = models.CharField(max_length=500, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    symbol = models.CharField(max_length=15)

    def __str__(self):
        return self.company_name

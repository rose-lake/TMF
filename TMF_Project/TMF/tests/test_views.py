from django.test import TestCase, Client
from django.urls import reverse
from TMF.models import Author, Article, Comment, Quote
import json

# we're going to be dealing with database stuff, so we're using django.test.TestCase

class TestViews(TestCase):
    

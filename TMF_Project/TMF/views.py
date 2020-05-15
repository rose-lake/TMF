import json, os, random, requests, re
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Author, Quote
from .forms import CommentForm

import logging
logger = logging.getLogger(__name__)


def populate_author(api_author):

    logger.info("Populating Author 'uuid':%s", api_author["uuid"])

    author = Author()
    author.byline = api_author["byline"]
    author.email = api_author["email"]
    author.username = api_author["username"]
    author.uuid = api_author["uuid"]
    author.save()
    return author


def fetch_first_p(html):
    soup = BeautifulSoup(html, 'lxml')
    first_paragraph = soup.find("p")
    if not first_paragraph == None:
        logger.info('fetched first paragraph successfully')
        return str(first_paragraph)
    else:
        message = "Article 'body' key did not contain a '<p>' tag. Actual tags were: "
        for tag in soup.find_all(True):
            message += tag.name + " "
        logger.error(message)
        return ""


def populate_article(api_article):

    logger.info("Populating article 'uuid':%s", api_article["uuid"])

    article = Article()
    article.body_extras = "{%load tmf_extras%}" + api_article["body"]
    article.body_first_p = fetch_first_p(api_article["body"])
    article.byline = api_article["byline"]
    article.disclosure = api_article["disclosure"]
    article.headline = api_article["headline"]
    article.image_url = api_article["images"][0]["url"]
    article.modified = datetime.strptime(api_article["modified"], "%Y-%m-%dT%H:%M:%SZ")
    article.path = api_article["path"]
    article.promo = api_article["promo"]
    article.sfr_content = api_article["pitch"]["text"]
    article.uuid = api_article["uuid"]
    article.save()

    # included in the task of populating an article is the task of populating its Author(s) !!
    for api_author in api_article["authors"]:
        api_author_uuid = api_author["uuid"]
        try:
            author = Author.objects.get(uuid=api_author_uuid)
        except Author.DoesNotExist:
            logger.info("Author with uuid '%s' was not found in the DB", api_author_uuid)
            author = populate_author(api_author)
        # link that author up to the article and save the article
        article.authors.add(author)
        article.save()

    return article


def get_slug_article(slug):

    # fetch the article with "slug" == slug
    local_path = os.path.join(settings.BASE_DIR, "content_api.json")
    with open(local_path, "r") as read_file:
        content_api = json.load(read_file)
    found_slug = False
    for api_article in content_api["results"]:
        for tag in api_article["tags"]:
            if tag["slug"] == slug:
                found_slug = True
                api_article_uuid = api_article.get("uuid")
                if not api_article_uuid is None:
                    try:
                        article = Article.objects.get(uuid=api_article_uuid)
                    except Article.DoesNotExist:
                        logger.info("Article with uuid '%s' was not found in the DB", result_uuid)
                        article = populate_article(api_article)
                    return article
                else:
                    message = "The requested slug article did not have a valid 'uuid' key. The article's actual keys are: " + api_article.keys()
                    logger.error(message)
                    found_slug = False
                    # let the method keep trying to find a valid slug_article
                    # maybe the next one has a valid uuid...
                    continue

    if not found_slug:
        # for some reason, an article with the requested slug wasn't found,
        # or, the article with the requested slug was found but didn't have a valid uuid
        # return an empty article and sysout an error message
        message = "The requested slug article could not be loaded. The requested slug was: " + slug
        logger.error(message)
        return Article()


def populate_quote(api_quote):

    api_exchange = api_quote["Exchange"]
    api_symbol = api_quote["Symbol"]
    api_company_name = api_quote["CompanyName"]

    logger.info("Populating quote '%s:%s %s'", api_exchange, api_symbol, api_company_name)

    quote = Quote()
    quote.company_name = api_company_name
    quote.exchange = api_exchange
    quote.symbol = api_symbol
    quote.industry = api_quote["Industry"]
    quote.sector = api_quote["Sector"]

    quote.current_price = api_quote["CurrentPrice"]["Amount"]
    quote.change_dollar = api_quote["Change"]["Amount"]
    if quote.change_dollar >= 0:
        quote.change_is_positive = True
        # this includes 'zero change' as 'positive' (seemed better than 'negative')
        # but the front-end template handles it as a separate case
    else:
        quote.change_is_positive = False
    quote.change_percent = api_quote["PercentChange"]["Value"]

    # detail_url, using www.fool.com/quote
    base_detail_url = "https://www.fool.com/quote/"
    # regex might be more compact, but this works, too!
    company_name = (
        quote.company_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
    )
    if company_name != "barrick-gold":
        url_symbol = quote.symbol.lower()
    else:
        # company_name is barrick-gold --> Barrick Gold workaround for quote detail url
        # It should be either NYSE:GOLD or TSX:ABX
        # In the JSON file it is NYSE:ABX
        # Since this only an issue for the detail url, leave as NYSE: ABX in the db.
        if api_exchange == "NYSE":
            url_symbol = "gold"
        elif api_exchange == "TSX":
            url_symbol = "abx"
    quote.detail_url = (base_detail_url + quote.exchange.lower() + "/" + company_name + "/" + url_symbol + "/")

    #image_url, using g.foolcdn.com/image/
    base_image_url = "https://g.foolcdn.com/image/"
    key_value_pairs = {
        "url": "https://g.foolcdn.com/art/companylogos/mark/" + quote.symbol.upper() + ".png",
        "w": "64",
        "h": "64",
        "op": "resize",
    }
    r = requests.get(base_image_url, params=key_value_pairs)
    if r.status_code == requests.codes.ok:
        quote.image_url = base_image_url + "?" + urllib.parse.urlencode(key_value_pairs)
    else:
        quote.image_url=""

    logger.debug("status code: %d, image_url: %s", r.status_code, quote.image_url)

    quote.save()
    return quote

def generate_random_indeces(num, upper_bound):

    chosen_indeces = []
    index_count = 0
    while index_count < num:

        # generate a random index
        random_index = random.randrange(0, upper_bound)

        # check if we've already grabbed that one or not
        if not random_index in chosen_indeces:
            chosen_indeces.append(random_index)
            index_count += 1

        # for debugging:
        else:
            logger.debug("Index %d was already taken, try again! Current value of index_count: %d", random_index, index_count)
        # print("this index was already taken, try again!")
        # # do not increment index_count
        # print("current value of index_count " + str(index_count) )

    return chosen_indeces


def get_random_articles(num_articles, except_article_id):
    articles = []

    # the list of id's is all of the Article id's EXCEPT the one you pass in (which is in the jumbo card element)
    full_list = list(Article.objects.values_list('id', flat=True))
    # print('full_list ',full_list)
    # print('except_article_id ', except_article_id)
    full_list.remove(except_article_id)
    # print('full_list after remove() ', full_list)

    article_id_list = list(Article.objects.values_list('id', flat=True))
    article_id_list.remove(except_article_id)
    sample_n = min(len(article_id_list), num_articles)
    random_article_id_list = random.sample(article_id_list, sample_n)
    for id in random_article_id_list:
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            logger.error("Article with id '%d' did not exist.", id, exc_info=True)
            continue
        articles.append(article)
    return articles

def get_random_quotes(num_quotes):
    quotes = []
    quote_id_list = list(Quote.objects.values_list('id', flat=True))
    sample_n = min(len(quote_id_list), num_quotes)
    random_quote_id_list = random.sample(quote_id_list, sample_n)
    for id in random_quote_id_list:
        try:
            quote = Quote.objects.get(id=id)
        except Quote.DoesNotExist:
            logger.error("Quote with id '%d' did not exist.", id, exc_info=True)
            continue
        quotes.append(quote)
    return quotes

def get_matching_plus_random(max_quotes, article):

    quotes = []
    ids_found = []

    #-------------------------------------------------------------------------------
    # a rough regex match on article body for EXCHANGE:SYMBOL or SYMBOL or EXCHANGE
    # this finds:
    #    EITHER: exchange:symbol pair
    #       opening parenthese + 1 or more all caps + 0 or more space + colon
    #       + 0 or more space + 1 or more all caps
    #   OR: a possible symbol
    #       opening parenthese + 1 or more all caps + 0 or more space
    # future:
    #   could refine the regex search by looking for...
    #   a single word beginning with a CAP surrounded <strong></strong>
    #   and checking if it matches a CompanyName for any Quotes in our DB
    #-------------------------------------------------------------------------------
    regex_find_all = re.findall(r"\([A-Z]+\s*:\s*[A-Z]+|\([A-Z]+\s*", article.body_extras + article.promo)
    match_list = []
    for regex_found in regex_find_all:
        # a quick clean-up of returned regex :: this effectively splits around all-caps
        match_list.append(re.findall(r"[A-Z]+", regex_found))

    #-------------------------------------------------------------------------------
    # each elem in match_list is itself a list returned from re.findall()
    # for all our use cases (content_api.json articles) each elem is size 1 or 2
    # elem[index] is an ALLCAPS str that may or may not be EXCHANGE:SYMBOL or SYMBOL
    #-------------------------------------------------------------------------------
    for elem in match_list:
        if len(elem) == 0:
            message = "Something very weird happened here! One of the elements in " + str(match_list) + "had length zero..."
            logger.warning(message)
            continue
        elif len(elem) == 1:
            # try to get Quote from DB by SYMBOL alone
            try:
                quote = Quote.objects.get(symbol__iexact=elem[0])
            except Quote.DoesNotExist:
                logger.info("Possible Symbol '%s' was not found as a Quote's Symbol in the DB... Most likely it's not actually a valid Symbol.", elem[0])
                continue
        elif len(elem) == 2:
            # try to get Quote from DB by EXCHANGE and SYMBOL
            try:
                quote = Quote.objects.get(exchange__iexact=elem[0], symbol__iexact=elem[1])
            except Quote.DoesNotExist:
                logger.info("Possible Symbol '%s' was not found as a Quote's Symbol in the DB... Most likely it's not actually a valid Symbol.", elem[0])
                continue
        else:
            message = "Regex found more than two contiguous instances of all caps in our article body... This shouldn't happen b/c of the way our regex is written!? Here is what was found: " + str(elem)
            logger.warning(message)
            continue

        # only append unique quotes
        # only as long as we don't have the max number yet
        if len(quotes) < max_quotes:
            if not quote.id in ids_found:
                ids_found.append(quote.id)
                quotes.append(quote)
        else:
            # quit gathering quotes if we've reached our maximum number
            break

    # at this point, we've matched all we can out of the article body to the DB.
    # now, add on random quotes up to the maximum number
    num_quotes = max_quotes - len(quotes)
    all_ids = list(Quote.objects.values_list('id', flat=True))
    subset_ids = [x for x in all_ids if x not in ids_found]

    logger.debug("all ids: %s", str(all_ids))
    logger.debug("ids found: %s", str(ids_found))
    logger.debug("subset_ids: %s", str(subset_ids))

    sample_n = min(len(subset_ids), num_quotes)
    random_ids = random.sample(subset_ids, sample_n)

    logger.debug("random_ids: %s", str(random_ids))

    for id in random_ids:
        try:
            quote = Quote.objects.get(id=id)
        except Quote.DoesNotExist:
            # note: if a quote isn't found, we end up showing less quotes on the page
            logger.error("Quote with id '%d' did not exist.", id, exc_info=True)
            continue
        quotes.append(quote)

    return quotes

# this method loads all valid quotes from the 'API' JSON file into the DB
# it does not return any values
def load_all_quotes():

    local_path = os.path.join(settings.BASE_DIR, "quotes_api.json")
    with open(local_path, "r") as read_file:
        quotes_api = json.load(read_file)

    # Load all quotes into the DB
    # For each quote, check to make sure it doesn't already exist in the DB
    # this is not the way it would work in a production environment, since quotes
    # are always changing, you would grab one dynamically each time it's needed

    for index in range(0, len(quotes_api)):
        # grab our current quote
        quote = quotes_api[index]

        # match on "Exchange", "Symbol", and "CompanyName"
        exchange = quote["Exchange"]
        symbol = quote["Symbol"]
        company_name = quote["CompanyName"]

        # 'UNKNOWN' workaround: if Exchange is 'UNKNOWN', then it's not really a Quote!
        if exchange == "UNKNOWN":
            # continue to the next index, do not load this quote into the DB
            logger.error("Quote data error: '%s:%s %s' is not a valid quote. Quote was skipped and not loaded into the DB.",  exchange, symbol, company_name)
            continue
        try:
            # check if quote matching on Exchange, Symbol, and CompanyName exists in DB
            # note: Barrick Gold info is left unchanged in the DB
            quote = Quote.objects.get(
                exchange__iexact=exchange,
                symbol__iexact=symbol,
                company_name__iexact=company_name,
            )
        except Quote.DoesNotExist:
            # here is the one spot where we populate the DB
            logger.info("Quote '%s:%s %s' was not found in the DB",  exchange, symbol, company_name)
            quote = populate_quote(quote)

def load_all_articles():

    local_path = os.path.join(settings.BASE_DIR, "content_api.json")
    with open(local_path, "r") as read_file:
        content_api = json.load(read_file)

    for result in content_api["results"]:
        result_uuid = result.get("uuid")
        if not result_uuid is None:
            try:
                article = Article.objects.get(uuid=result_uuid)
            except Article.DoesNotExist:
                logger.info("Article with uuid '%s' was not found in the DB", result_uuid)
                article = populate_article(result)
        else:
            message = "While looping through content_api['results'], a 'result' did not have a valid 'uuid' key. The result's actual keys are: " + result.keys()
            logger.error(message)

###############################################################################
# home view:
#       url path name = 'home'
#       template name = 'home.html'
# this is the landing page, with one jumbo and three smaller article cards
###############################################################################
def home(request):

    # development only -- for debugging purposes
    Article.objects.all().delete()
    Quote.objects.all().delete()
    Author.objects.all().delete()

    # load all articles and (valid) quotes into the DB, first
    # if the DB is already populated, this simply verifies each article's existence (from content_api.json) and each quote's existence (from quotes_api.json)
    load_all_articles()
    load_all_quotes()

    slug_article = get_slug_article("10-promise")
    articles = get_random_articles(num_articles=3, except_article_id=slug_article.id)

    return render(
        request,
        "TMF/home.html",
        { "slug_article": slug_article, "articles": articles, }
    )


###############################################################################
# article_detail view:
#       url path name = 'article_detail'
#       template name = 'article.html'
# this is the article detail page, with quotes, headlines, and comments
###############################################################################
def article_detail(request, pk):

    # fetch the requested article detail page
    article = get_object_or_404(Article, pk=pk)

    # 7 total quotes = matching quotes + random quotes
    quotes = get_matching_plus_random(max_quotes=7, article=article)

    # populate the PROMO ARTICLES side-bar
    promos = get_random_articles(num_articles=5, except_article_id=article.id)

    return render(
        request,
        "TMF/article.html",
        {"article":article, "quotes": quotes, "promos": promos,}
        )

###############################################################################
# add_comment_to_article view:
#       url path name = 'add_comment_to_article'
#       template name = 'add_comment_to_article.html'
# this is the comment form page, which includes its article's headline & image
###############################################################################
def add_comment_to_article(request, pk):

    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', pk=pk)

    else:
        form = CommentForm()

    return render(request,
                  'TMF/add_comment_to_article.html',
                  {'form': form, 'article': article}
                  )

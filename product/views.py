from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
import requests
import re
from bs4 import BeautifulSoup
from product.models import Product, Price

logger = logging.getLogger(__name__)

PRODUCT_URL = "https://www.amazon.co.jp/dp/"
SEARCH_URL = "https://www.amazon.co.jp/s?k="
SEARCH_RESULTS_MAX = 3


def index(request):
    '''
    Home画面
    '''
    products = Product.objects.all().order_by("-created_date")
    context = {
        "products": products,
        "product_url": PRODUCT_URL,
    }
    return render(request, "product/index.html", context)


def search(request):
    '''
    検索にヒットした商品を登録する
    '''
    if not request.POST:
        return redirect("index")
    keyword = request.POST.get("keyword", "")
    if not keyword:
        return redirect("index")
    asins = get_search_results(keyword)
    for asin in asins:
        page_soup = get_product_soup(asin)
        if page_soup:
            scraped_data = scrape_product(page_soup)
            if not scraped_data:
                continue
            product, created = Product.objects.get_or_create(asin=asin)
            if created:
                # 未登録の商品のみ新規登録する
                product.title = scraped_data["title"]
                product.image = scraped_data["image"]
                product.save()
                logger.debug("New product registered.")
            scrape_price(product, page_soup)
    return redirect("index")


def delete(request, asin):
    '''
    商品を削除する
    '''
    product = Product.objects.filter(asin=asin)
    if product:
        product.delete()
        logger.debug(f"{asin} deleted.")
    return redirect("index")


def is_asin(keyword):
    '''
    ASINまたはISBNかどうかを判定する
    現時点では、10桁の英数字であればASIN/ISBNと判断する
    '''
    if re.match("^[a-zA-Z\d]{10}$", keyword):
        logger.debug(f"Consider the keyword '{keyword}' as ASIN/ISBN")
        return True
    return False


def get_product_soup(asin):
    '''
    ASINから商品ページを取得し、BeautifulSoup形式で返す
    404の場合はNoneを返す
    '''
    response = requests.get(PRODUCT_URL + asin)
    if response.status_code == 404:
        logger.debug(f"{asin} product page is 404.")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_search_results(keyword):
    '''
    キーワードから商品を検索し、ASIN番号のリストを返す
    ない場合は空リストを返す
    最大数は 'SEARCH_RESULTS_MAX'
    '''
    response = requests.get(SEARCH_URL + keyword)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", class_="s-result-item")
    asins = []
    for p in products:
        asins.append(p.get("data-asin"))
    asins = asins[:SEARCH_RESULTS_MAX]
    logger.debug(f"keyword:{keyword}, results:{asins}")
    return asins


def scrape_product(soup):
    '''
    商品ページのレスポンスからスクレイピングを行う
    PrimeVideoの場合はNoneを返却する
    '''
    category = soup.select_one('.nav-a-content')
    if category and category.text.strip() in ["Prime Video"]:
        logger.debug("Prime video detected. skipped.")
        return None
    title, image = None, None
    titles = soup.find_all(attrs={"id": ["productTitle", "ebooksProductTitle"]})
    if titles:
        title = titles[0].string.strip()
    images = soup.find_all(
        attrs={"id": ["landingImage", "imgBlkFront", "ebooksImgBlkFront"]})
    if images:
        image = images[0].get("src")

    return {"title": title, "image": image}


def scrape_price(product, soup):
    '''
    商品情報から価格をスクレイピングし、保存する
    価格が取得できない場合、nullデータとして保存する
    '''
    html = soup.select_one("#buybox .a-size-medium.a-color-price")
    price = None
    if html and html.contents:
        price = int(re.sub(r"[,￥]", "", html.contents[0].strip()))
        logger.debug(f"{product.asin} price: {price}")
    Price(product=product, price=price).save()

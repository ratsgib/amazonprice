from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
import requests
import re
from bs4 import BeautifulSoup
from product.models import Product

logger = logging.getLogger(__name__)

PRODUCT_URL = "https://www.amazon.co.jp/dp/"


def index(request):
    products = Product.objects.all()
    context = {
        "products": products,
        "product_url": PRODUCT_URL
    }
    return render(request, 'product/index.html', context)


def search(request):
    context = {}
    if request.POST:
        keyword = request.POST.get("keyword", "").upper()
        if not keyword:
            return redirect("index")
        if is_asin(keyword):
            page_soup = get_product_soup(keyword)
            if page_soup:
                product, created = Product.objects.get_or_create(asin=keyword)
                if created:
                    scraped_data = scrape_product(page_soup)
                    product.title = scraped_data["title"]
                    product.image = scraped_data["image"]
                    product.save()
                    scrape_price(soup)
                    logger.debug("New product registered.")
        return redirect("index")
    else:
        return redirect("index")


def is_asin(keyword):
    '''
    ASINまたはISBNかどうかを判定する。
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
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def scrape_product(soup):
    '''
    商品ページのレスポンスからスクレイピングを行う
    '''
    title = soup.find(id="productTitle") or soup.find(id="ebooksProductTitle")
    title = title.string.strip()
    image = soup.find(id="landingImage") or soup.find(id="imgBlkFront") or soup.find(id="ebooksImgBlkFront")
    image = image.get("src")

    return {'title': title, 'image': image}


def scrape_price(soup):
    '''
    商品情報から価格をスクレイピングし、保存する
    '''
    pass

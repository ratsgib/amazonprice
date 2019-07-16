from django.core.management.base import BaseCommand, CommandError
from product.models import Product, Price
from product.views import get_product_soup, scrape_price
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        '''
        全ての商品の価格を取得する
        '''
        logger.info("Price scraping started.")
        for p in Product.objects.all():
            soup = get_product_soup(p.asin)
            scrape_price(p, soup)
        logger.info("Price scraping finished.")

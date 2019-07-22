# amazon.co.jp Price Tracker

#### Install
```
pip install -r 'pip_reqs.txt'
./manage.py migrate
```

#### How to use
Run the django server and access the root URL.
```
https://[your server]/
```
And input a keyword of your favorite products.

#### Price scraping batch
```
manage.py scrape_price
```

#### Todo
* More tests
* More price patterns
* Search and select

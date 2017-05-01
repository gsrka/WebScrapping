from bs4 import BeautifulSoup
import requests
import pprint, urllib


def ParseAmazonProducts(searchUrl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    i = 1
    scrapeOutput = []
    while(True):
        url = searchUrl + '&page=' + str(i)
        print "Scrapping:: " + url
        page = requests.get(url, headers=headers)
        req_status = -1
        while (req_status != 200):
            page = requests.get(url, headers=headers)
            req_status = page.status_code

        mainSoup = BeautifulSoup(page.content, 'lxml')
        productsSoup = mainSoup.findAll("li", {"id": lambda x: x and 'result_' in x})

        if productsSoup.__len__() < 1:
            break

        productsData = []

        for productSoup in productsSoup:
            productTitleElement = productSoup.findAll("a", {"class": "s-access-detail-page"})
            if productTitleElement.__len__() < 1:
                continue
            productTitle = productTitleElement[0].get('title')
            productLink = productTitleElement[0].get('href')
            productId = productSoup.get('data-asin')
            productData = {
                '_id' : productId,
                'name': productTitle,
                'link': productLink
            }

            productPriceElement = productSoup.findAll(True, {"class": ["a-color-base", "sx-zero-spacing"]})
            if productPriceElement.__len__() > 0:
                productData["price"] = productPriceElement[0].get('aria-label')

            productsData.append(productData)
        i = i + 1
        scrapeOutput = scrapeOutput + productsData

    return scrapeOutput


def getMaxPagesInAmazon(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    req_status = -1
    while (req_status != 200):
        page = requests.get(url, headers=headers)
        req_status = page.status_code

    soup = BeautifulSoup(page.content, 'lxml')
    print(soup)
    maxPagesElement = soup.findAll("span", {"class": "pagnDisabled"})

    if maxPagesElement.__len__() < 1:
        return 0

    maxPages = maxPagesElement[0].string
    return int(maxPages)


def ScrapeProducts(searchKey):
    searchUrl = "https://www.amazon.com/s?field-keywords=" + urllib.quote(searchKey, safe='')

    scrapedData = []
    """maxPages = getMaxPagesInAmazon(searchUrl)
    if maxPages == 0:
        print("No Results Found")
        return
    for i in range(1, maxPages + 1):
        url = searchUrl + '&page=' + str(i)
        print "Scraping::::: " + url
        scrapedData += ParseAmazonProducts(url)"""

    scrapedData = ParseAmazonProducts(searchUrl)

    # print(scrapedData)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(scrapedData)


if __name__ == "__main__":
    ScrapeProducts('Camera')
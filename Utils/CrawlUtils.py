import re
import requests
import codecs
import random
from bs4 import BeautifulSoup

def getQuery404(inputstring):
    '''
    This functions replace "san-pham/" with "tim-kiem?q="
    It also remove all numbers from input
    '''
    query_string = re.sub("san-pham\/", "tim-kiem?q=", inputstring)
    return re.sub("[0-9]", "", query_string)


def http_https_fill(inputstring):
    '''
    This methods check whether the inputstring has the format:
    + start with http:/https:
    If not, append to the inputstring
    '''
    # Check http: and https:
    state = re.match('^(http|https):.*$', inputstring)
    if state is None:
        inputstring = "https:" + inputstring
    return inputstring


def getPriceFromString(inputstring):
    '''
    This method removes all the non-number character from string and return an integer
    '''
    return int(re.sub("[^0-9]", "", inputstring))


def getProductInfo(inputlink):
    try:
        res = requests.get(inputlink)
        soup = BeautifulSoup(res.text, 'html.parser')

        if (res.status_code == 200):
            # status code: 200
            currentPrice = soup.find_all(class_='currentPrice_2zpf')  # List
            oldPrice = soup.find_all(class_='oldPrice_119m')  # List
            imgClass = soup.find_all(class_='imageSquare_2ilQ')  # List

            statusContent = res.status_code
            currentPriceContent, oldPriceContent, imgClassContent = None, None, None

            if len(currentPrice) or len(oldPrice) or len(imgClass):
                print("Case 1")

                # Get the price and image uri
                if len(currentPrice):
                    # Get current Price
                    currentPriceContent = currentPrice[0].contents
                    currentPriceContent = currentPriceContent[0] if len(
                        currentPriceContent) else None
                    currentPriceContent = getPriceFromString(currentPriceContent) if (
                        currentPriceContent is not None) else None

                if len(oldPrice):
                    # Get old price
                    oldPriceContent = oldPrice[0].contents
                    oldPriceContent = oldPriceContent[0] if len(
                        oldPriceContent) else None
                    oldPriceContent = getPriceFromString(oldPriceContent) if (
                        oldPriceContent is not None) else None

                if len(imgClass):
                    # Get Img
                    imgClassContent = imgClass[0].select('img')
                    imgClassContent = imgClassContent[0].get('src') if (
                        imgClassContent is not None) else None

                # Processing to handle faulty value
                currentPriceContent = oldPriceContent if (
                    currentPriceContent is None) else currentPriceContent
                oldPriceContent = currentPriceContent if (
                    oldPriceContent is None) else oldPriceContent
                imgClassContent = http_https_fill(imgClassContent) if (
                    imgClassContent is not None) else None

                return statusContent, currentPriceContent, oldPriceContent, imgClassContent
            else:
                try:
                    print("Case 2 or 3")
                    strProduct = soup.find_all('script', text=re.compile('PageBasic'))[
                        0].contents[0]
                    limitString = strProduct[strProduct.find(
                        'PageBasic'):strProduct.find('HeaderInfo')]
                    matchList = re.finditer(
                        "(https:|http').*?(jpg|jpeg|png|tif|tiff|bmp|gif|eps|raw|cr2|nef|orf|sr2)", limitString)

                    img_uri_list = []
                    for x in matchList:
                        img_uri_list.append(codecs.decode(
                            x.group(), 'unicode-escape'))

                    # Randomly choose from the list
                    imgClassContent = random.choice(
                        img_uri_list) if len(img_uri_list) else None

                except:
                    print("ERROR in link: ", inputlink)
                    print("Status: ", res.status_code)
                    currentPriceContent = None
                    oldPriceContent = None
                    imgClassContent = None

                finally:
                    return statusContent, currentPriceContent, oldPriceContent, imgClassContent

        elif (res.status_code == 404):
            # status code: 404
            statusContent = res.status_code
            currentPriceContent, oldPriceContent, imgClassContent = None, None, None

            res = requests.get(getQuery404(inputlink))
            soup = BeautifulSoup(res.text, 'html.parser')

            try:
                if (len(soup.find_all('script', text=re.compile('PageBasic')))):
                    strProduct = soup.find_all(
                        'script', text=re.compile('PageBasic'))

                    if (len(strProduct[0].contents)):
                        strProduct = strProduct[0].contents[0]
                        limitString = strProduct[strProduct.find(
                            'PageBasic'):strProduct.find('HeaderInfo')]
                        matchList = re.finditer(
                            "(https:|http').*?(jpg|jpeg|png|tif|tiff|bmp|gif|eps|raw|cr2|nef|orf|sr2)", limitString)

                        img_uri_list = []
                        for x in matchList:
                            img_uri_list.append(codecs.decode(
                                x.group(), 'unicode-escape'))

                        imgClassContent = random.choice(
                            img_uri_list) if len(img_uri_list) else None
            except:
                currentPriceContent, oldPriceContent, imgClassContent = None, None, None

            finally:
                return statusContent, currentPriceContent, oldPriceContent, imgClassContent
    except:
        print('ERROR in Request')
        return None, None, None, None

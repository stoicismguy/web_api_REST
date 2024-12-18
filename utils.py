import requests
from bs4 import BeautifulSoup



def get_products():
    # print("Utils.py get_products()")
    cookies = {
    'spid': '1734511832338_685d164a864f783639c43df308a87252_esk8u94g8due51ag',
    'spsc': '1734516797246_c431ed7478e8b8e4e8b0700fb7f08170_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
    'session': 'j:{"accessToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJqdGkiOiJkNmEwODc0OC0zNDgzLTRjODYtYTBkOC1hMzYzMTQ4MjVlMzQiLCJpYXQiOjE3MzQ1MTE4MzIsImV4cCI6MTczNDU0MDYzMiwiZCI6ImY4MzRjMDc1LWFmMjUtNGMxNC1hZDQ5LWMwMWM5YmQxMTJhOCIsImFwaSI6IjEuNC4xLjAiLCJpcCI6Ijk1LjI2LjczLjE0OSIsInUiOiI5ZmRmMzk1Yy1mODcxLTQ3NDItYTJmNy1hZTJiMDUyMTFiZTgiLCJ0IjoxfQ.AMnHF2rrrzJ2PhIDS1IeZ87_omOs3DaF1Eorfht4voLpXFVrJM2PtiQSOVlDLmtJ9jVW1SQYO4Q_-CFlw2QAelT1ABzDqCVJxQySC38NmLBsjIqdu9pODvDzT3WRvdxsoQ60pgQa9H4bH7DRymt2NDUgKjiqgSWhK0JeaziJd9KHf4wH","refreshToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJqdGkiOiI0MTkzNjdmNS0wYzVmLTQxZjEtYmIzNi0zMzU1YTQzMmU4OTAiLCJpYXQiOjE3MzQ1MTE4MzIsImV4cCI6MTc1MDA2MzgzMiwiZCI6ImY4MzRjMDc1LWFmMjUtNGMxNC1hZDQ5LWMwMWM5YmQxMTJhOCIsImFwaSI6IjEuNC4xLjAiLCJpcCI6Ijk1LjI2LjczLjE0OSIsInUiOiI5ZmRmMzk1Yy1mODcxLTQ3NDItYTJmNy1hZTJiMDUyMTFiZTgiLCJ0IjoyfQ.ATEloGgGVT26C_FkRbnveMz6510GaWQ_35-E4nMTxpcmWyzZmz7QosIHN0uJ8eij1zQeFEzNZXE3f9s_kXWR5rFEAbDkMa6zRznlewNLT6-CJnG9VQY2t9cPBN18bRYLU5sFhokA8i48K04uXIFeDySnhwl-uoOh4PrXprlVOTVjKkZn","accessTokenExpiredAt":1734540632433,"refreshTokenExpiredAt":1750063832433,"device":{"uuid":"f834c075-af25-4c14-ad49-c01c9bd112a8"}}',
    'TS015bfe9d': '01b7bf3690b192a66ec2b46825962b8466cf2d574388379e23e30fae639ed0f3073b4bc5ba25a3ebe3ca8c5bf46c56ed6c4ddb9a4d77fcc4aa8a9d3930afb283f82291f029',
    '_gcl_au': '1.1.532955378.1734511834',
    '_ga_5K49P5RFR8': 'GS1.1.1734516799.2.0.1734516799.60.0.0',
    '_ga': 'GA1.1.2099577711.1734511834',
    '_ymab_param': 'upPiRmHTlxO6HaJHQrfQZ__c0EF6RvqTg8F9I5p_97sqS5dYhSxQTW3lnWP32Jb_NG98qNe5FQtY_wVFA3jCqoYP4N8',
    'agreements': 'j:{"isCookieAccepted":true,"isAdultContentEnabled":false,"isAppAppInstallPromptClosed":false}',
    'tmr_lvid': '9c91559774082e6d878ef8e4306e13d2',
    'tmr_lvidTS': '1734511835513',
    '_ym_uid': '1734511836548205208',
    '_ym_d': '1734511836',
    '_ym_isad': '1',
    'domain_sid': 'OAdskaevQztDOTHplnbn-%3A1734511837788',
    'tmr_detect': '1%7C1734516799538',
    '_ym_visorc': 'b',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        # 'Cookie': 'spid=1734511832338_685d164a864f783639c43df308a87252_esk8u94g8due51ag; spsc=1734516797246_c431ed7478e8b8e4e8b0700fb7f08170_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5; session=j:{"accessToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJqdGkiOiJkNmEwODc0OC0zNDgzLTRjODYtYTBkOC1hMzYzMTQ4MjVlMzQiLCJpYXQiOjE3MzQ1MTE4MzIsImV4cCI6MTczNDU0MDYzMiwiZCI6ImY4MzRjMDc1LWFmMjUtNGMxNC1hZDQ5LWMwMWM5YmQxMTJhOCIsImFwaSI6IjEuNC4xLjAiLCJpcCI6Ijk1LjI2LjczLjE0OSIsInUiOiI5ZmRmMzk1Yy1mODcxLTQ3NDItYTJmNy1hZTJiMDUyMTFiZTgiLCJ0IjoxfQ.AMnHF2rrrzJ2PhIDS1IeZ87_omOs3DaF1Eorfht4voLpXFVrJM2PtiQSOVlDLmtJ9jVW1SQYO4Q_-CFlw2QAelT1ABzDqCVJxQySC38NmLBsjIqdu9pODvDzT3WRvdxsoQ60pgQa9H4bH7DRymt2NDUgKjiqgSWhK0JeaziJd9KHf4wH","refreshToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJqdGkiOiI0MTkzNjdmNS0wYzVmLTQxZjEtYmIzNi0zMzU1YTQzMmU4OTAiLCJpYXQiOjE3MzQ1MTE4MzIsImV4cCI6MTc1MDA2MzgzMiwiZCI6ImY4MzRjMDc1LWFmMjUtNGMxNC1hZDQ5LWMwMWM5YmQxMTJhOCIsImFwaSI6IjEuNC4xLjAiLCJpcCI6Ijk1LjI2LjczLjE0OSIsInUiOiI5ZmRmMzk1Yy1mODcxLTQ3NDItYTJmNy1hZTJiMDUyMTFiZTgiLCJ0IjoyfQ.ATEloGgGVT26C_FkRbnveMz6510GaWQ_35-E4nMTxpcmWyzZmz7QosIHN0uJ8eij1zQeFEzNZXE3f9s_kXWR5rFEAbDkMa6zRznlewNLT6-CJnG9VQY2t9cPBN18bRYLU5sFhokA8i48K04uXIFeDySnhwl-uoOh4PrXprlVOTVjKkZn","accessTokenExpiredAt":1734540632433,"refreshTokenExpiredAt":1750063832433,"device":{"uuid":"f834c075-af25-4c14-ad49-c01c9bd112a8"}}; TS015bfe9d=01b7bf3690b192a66ec2b46825962b8466cf2d574388379e23e30fae639ed0f3073b4bc5ba25a3ebe3ca8c5bf46c56ed6c4ddb9a4d77fcc4aa8a9d3930afb283f82291f029; _gcl_au=1.1.532955378.1734511834; _ga_5K49P5RFR8=GS1.1.1734516799.2.0.1734516799.60.0.0; _ga=GA1.1.2099577711.1734511834; _ymab_param=upPiRmHTlxO6HaJHQrfQZ__c0EF6RvqTg8F9I5p_97sqS5dYhSxQTW3lnWP32Jb_NG98qNe5FQtY_wVFA3jCqoYP4N8; agreements=j:{"isCookieAccepted":true,"isAdultContentEnabled":false,"isAppAppInstallPromptClosed":false}; tmr_lvid=9c91559774082e6d878ef8e4306e13d2; tmr_lvidTS=1734511835513; _ym_uid=1734511836548205208; _ym_d=1734511836; _ym_isad=1; domain_sid=OAdskaevQztDOTHplnbn-%3A1734511837788; tmr_detect=1%7C1734516799538; _ym_visorc=b',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'If-None-Match': 'W/"121902-s5oe2AAU1OXGw6AhgorIBPkhYps"',
        'Priority': 'u=0, i',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    products = []
    request = requests.get('https://www.perekrestok.ru/cat/c/138/maso-pticy', cookies=cookies, headers=headers)

    soup = BeautifulSoup(request.content, 'lxml')
    items = soup.find_all('div', class_="product-card__content")

    for item in items:
        title = item.find('div', class_="product-card__title").get_text()
        price = int(str(item.find('div', class_="price-new").contents[1]).replace('₽', '').strip().split(",")[0])
        products.append((title, price))
    return products

# print(get_products())
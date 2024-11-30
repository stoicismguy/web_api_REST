import requests
from bs4 import BeautifulSoup



def get_products():
    # print("Utils.py get_products()")
    cookies = {
    'session': 'j:{accessToken:eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJqdGkiOiI5MjY5ZDBjNy1kZGI3LTRkMzktOWJmMS0wODA3NThmOTVmNTkiLCJpYXQiOjE3MzI5Njg1NzAsImV4cCI6MTczMjk5NzM3MCwiZCI6IjA4OGEwNGVkLTFmNDMtNDZkNy1hMWM5LTI4YTI3OTk0NDUxOCIsImFwaSI6IjEuNC4xLjAiLCJpcCI6Ijk1LjI2Ljc0LjU3IiwidSI6ImE1M2NhNTBjLTA3NjctNDEyOS1iYzRiLWUxMmY0ZTRmOTM5OCIsInQiOjF9.AJrr1EaFU5xmw9J_5R5zfs5x20czlWo0TZKI65pLf7vE0DCWAsq-s1TtuuVqcRgJ7jhpI38poCkQaeo9ypbY4jKTAOYFLF6DT90ed5C1vZDQtWfjwVUJDno_goiFp7HYcqK4TPEV1PG35FQwQjDLxxpRssn553s3HWXqwMkoSKmu_3YV,refreshToken:eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJqdGkiOiIzMzhiNjE2Ny1hNWI4LTQ1MDktYTU4OC02NDcyNDlhYjFjN2QiLCJpYXQiOjE3MzI5Njg1NzAsImV4cCI6MTc0ODUyMDU3MCwiZCI6IjA4OGEwNGVkLTFmNDMtNDZkNy1hMWM5LTI4YTI3OTk0NDUxOCIsImFwaSI6IjEuNC4xLjAiLCJpcCI6Ijk1LjI2Ljc0LjU3IiwidSI6ImE1M2NhNTBjLTA3NjctNDEyOS1iYzRiLWUxMmY0ZTRmOTM5OCIsInQiOjJ9.AIPN9mTeEvWqHS-kokl2HD-EXNYr0RxYgNarRKyJleXiM1Cprqw1ZFM40rvowHf5oGvTGXbv5qZGRnlLoTO-cJTMADVXsiBNNJoezBhwdLYPn9cE_AXopX-PwpqXroiORngFVlZDcvvSdWEWaQUU1HmUtjriMP9-zFldpTMlCoiVVhVc,accessTokenExpiredAt:1732997370079,refreshTokenExpiredAt:1748520570079,device:{uuid:088a04ed-1f43-46d7-a1c9-28a279944518}}',
    'agreements': 'j:{isCookieAccepted:true,isAdultContentEnabled:true,isAppAppInstallPromptClosed:true}',
    '_ymab_param': '-M9udQJeBs9Ss-jc9nN4Xz8BAOBOtebSTa9YF-DRSMzgTd4S4JK3a48vqORRU9Szc6W6MI2qKu5Q5G0W-kVD-GBKymM',
    '_gcl_au': '1.1.1032203242.1729173308',
    '_ym_uid': '1729173309859837043',
    '_ym_d': '1729173309',
    '_ga_5K49P5RFR8': 'GS1.1.1732979775.6.1.1732979799.36.0.0',
    '_ga': 'GA1.1.652770756.1729173309',
    'spid': '1732792933350_6ccabccad1ff91aa4f4edde5cc4fc2a4_j9iopm2snh9qfs4x',
    'spsc': '1732979773770_9243186e38d8ad2a88d947f88140914f_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
    '_ym_isad': '1',
    'httpsReferer': 'https^%^3A^%^2F^%^2Fwww.google.com^%^2F',
    'TS015bfe9d': '01b7bf3690a4d90fe1aaea1149638e2fe241588fb1eb49111cb671cff26793ef15c16c5ce4f55f016e81d957d615dac93e830caf98081de5473ae462c6142892e7b0a34ed0008117f4b349ef01837104859fc839ca',
    '_ym_visorc': 'b',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        # 'Cookie': 'session=j:{accessToken:eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJqdGkiOiI5MjY5ZDBjNy1kZGI3LTRkMzktOWJmMS0wODA3NThmOTVmNTkiLCJpYXQiOjE3MzI5Njg1NzAsImV4cCI6MTczMjk5NzM3MCwiZCI6IjA4OGEwNGVkLTFmNDMtNDZkNy1hMWM5LTI4YTI3OTk0NDUxOCIsImFwaSI6IjEuNC4xLjAiLCJpcCI6Ijk1LjI2Ljc0LjU3IiwidSI6ImE1M2NhNTBjLTA3NjctNDEyOS1iYzRiLWUxMmY0ZTRmOTM5OCIsInQiOjF9.AJrr1EaFU5xmw9J_5R5zfs5x20czlWo0TZKI65pLf7vE0DCWAsq-s1TtuuVqcRgJ7jhpI38poCkQaeo9ypbY4jKTAOYFLF6DT90ed5C1vZDQtWfjwVUJDno_goiFp7HYcqK4TPEV1PG35FQwQjDLxxpRssn553s3HWXqwMkoSKmu_3YV,refreshToken:eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJqdGkiOiIzMzhiNjE2Ny1hNWI4LTQ1MDktYTU4OC02NDcyNDlhYjFjN2QiLCJpYXQiOjE3MzI5Njg1NzAsImV4cCI6MTc0ODUyMDU3MCwiZCI6IjA4OGEwNGVkLTFmNDMtNDZkNy1hMWM5LTI4YTI3OTk0NDUxOCIsImFwaSI6IjEuNC4xLjAiLCJpcCI6Ijk1LjI2Ljc0LjU3IiwidSI6ImE1M2NhNTBjLTA3NjctNDEyOS1iYzRiLWUxMmY0ZTRmOTM5OCIsInQiOjJ9.AIPN9mTeEvWqHS-kokl2HD-EXNYr0RxYgNarRKyJleXiM1Cprqw1ZFM40rvowHf5oGvTGXbv5qZGRnlLoTO-cJTMADVXsiBNNJoezBhwdLYPn9cE_AXopX-PwpqXroiORngFVlZDcvvSdWEWaQUU1HmUtjriMP9-zFldpTMlCoiVVhVc,accessTokenExpiredAt:1732997370079,refreshTokenExpiredAt:1748520570079,device:{uuid:088a04ed-1f43-46d7-a1c9-28a279944518}}; agreements=j:{isCookieAccepted:true,isAdultContentEnabled:true,isAppAppInstallPromptClosed:true}; _ymab_param=-M9udQJeBs9Ss-jc9nN4Xz8BAOBOtebSTa9YF-DRSMzgTd4S4JK3a48vqORRU9Szc6W6MI2qKu5Q5G0W-kVD-GBKymM; _gcl_au=1.1.1032203242.1729173308; _ym_uid=1729173309859837043; _ym_d=1729173309; _ga_5K49P5RFR8=GS1.1.1732979775.6.1.1732979799.36.0.0; _ga=GA1.1.652770756.1729173309; spid=1732792933350_6ccabccad1ff91aa4f4edde5cc4fc2a4_j9iopm2snh9qfs4x; spsc=1732979773770_9243186e38d8ad2a88d947f88140914f_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5; _ym_isad=1; httpsReferer=https^%^3A^%^2F^%^2Fwww.google.com^%^2F; TS015bfe9d=01b7bf3690a4d90fe1aaea1149638e2fe241588fb1eb49111cb671cff26793ef15c16c5ce4f55f016e81d957d615dac93e830caf98081de5473ae462c6142892e7b0a34ed0008117f4b349ef01837104859fc839ca; _ym_visorc=b',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'If-None-Match': 'W/119ea7-265dCk5AwDdCTrW12LrU/UDMX2E',
        'Priority': 'u=0, i',
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
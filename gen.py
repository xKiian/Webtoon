from httpx                import Client, get, post
from random               import randint, choices, choice
from string               import ascii_lowercase, digits, ascii_letters
from re                   import search
from time                 import sleep
from rsa                  import PublicKey, encrypt as rsae
from binascii             import hexlify
from urllib.parse         import urlencode, quote
from threading            import Thread, active_count, Lock
from hmac                 import new
from hashlib              import sha1
from time                 import time,sleep,strftime, time
from base64               import b64encode
from colorama             import Fore, init
from secrets              import token_urlsafe
from os                   import system
from sys                  import exit
from yaml                 import safe_load
from multiprocessing      import freeze_support

import imaplib
import email

init(autoreset=True) 
lock = Lock()
def sprint(text: str, tid: int, sp: str) -> None:  
    lock.acquire() 
    
    tid = str(tid) +"]" +" " * (3 - len(str(tid)))
    print(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}Thread [{tid} {Fore.LIGHTBLACK_EX}| {Fore.LIGHTWHITE_EX}{text} {Fore.WHITE}-> {Fore.GREEN}{sp}")
    
    lock.release()

config      = safe_load(open("config.yaml", "r"))
proxies     = open("input/proxies.txt","r", encoding='utf-8').read().splitlines()


email_list = []

data_title  = {
    'promos'            : 0,
    'api_bal'           : 0,
    'email_purchased'   : 0,
    'fails'             : 0,
    'finished'          : 0,
    'cpm'               : 0
}


def proxy_scraper():
    while True:
        try:
            r = get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=250&country=all&ssl=all&anonymity=all")#need to find a sweet spot
            proxies_write = open("input/proxies.txt", "wb") ; proxies_write.write(r.content) ; proxies_write.close()
            globals()["proxies"] = open("input/proxies.txt","r", encoding='utf-8').read().splitlines()
            sleep(300)
        except:pass

def fetch_api_balance():
    while True:
        try:
            data_title['api_bal'] =  int(get(f"https://api.hotmailbox.me/user/balance?apikey={config['hotmailbox_api_key']}").json()['Balance']) 
            
        except:sleep(1)

def update_title():
        while True:
            system('title Promofier By NinjaRide x xKian ^> Finished: [%s] ^| Emails: [%s] ^| Api Balance: [%s] ^| Fails: [%s] ^| Threads: [%s] ^| Elapsed: [%ss]' % (
                data_title['finished'], 
                data_title['email_purchased'], 
                data_title['api_bal'], 
                data_title['fails'],
                active_count() - 5 if config['email_type'] == "api" else active_count() - 4,
                round(time() - start, 2)
            ))
            sleep(.1)


def getcookies():
    return {
        "wtu"                : token_urlsafe(24),
        "locale"             : "en",
        "needGDPR"           : "true",
        "needCCPA"           : "false",
        "needCOPPA"          : "false",
        "countryCode"        : "RO",
        "timezoneOffset"     : "+3",
        "ctZoneId"           : "Europe/Bucharest",
        "wtv"                : "1",
        "wts"                : str(int(time() * 1000)),
        "__cmpconsentx47472" : f"{token_urlsafe(2)}_{token_urlsafe(3)}_{token_urlsafe(25)}",
        "__cmpcccx47472"     : token_urlsafe(18),
        "_fbp"               : "fb.1.1684479996310.2019224647",
        "_scid"              : "858a934e-433c-4e07-b4c3-c1a1b9becc34",
        "_gid"               : "GA1.2.1016427982.1684479996",
        "_tt_enable_cookie"  : "1",
        "_ttp"               : "2dlVmcQxdz_oQTW_6zMA2eNlFy3",
        "_scid_r"            : "858a934e-433c-4e07-b4c3-c1a1b9becc34",
        "_ga"                : "GA1.1.1939944414.1684479996",
        "_ga_ZTE4EZ7DVX"     : "GS1.1.1684486049.2.0.1684486049.60.0.0",
    }

def click_email(email_link):
    for _ in range(10):
        try:
            get(email_link,headers = {
                "accept"                        : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-encoding"               : "gzip, deflate, br",
                "accept-language"               : "en-US,en;q=0.9",
                "connection"                    : "keep-alive",
                "content-type"                  : "application/x-www-form-urlencoded; charset=UTF-8",
                "host"                          : "www.webtoons.com",
                "origin"                        : "https://www.webtoons.com",
                "referer"                       : "https://www.webtoons.com/member/join?loginType=EMAIL",
                "sec-ch-ua"                     : "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
                "sec-ch-ua-full-version-list"   : "\"Google Chrome\";v=\"113.0.5672.93\", \"Chromium\";v=\"113.0.5672.93\", \"Not-A.Brand\";v=\"24.0.0.0\"",
                "sec-ch-ua-mobile"              : "?0",
                "sec-ch-ua-model"               : "\"\"",
                "sec-ch-ua-platform"            : "\"Windows\"",
                "sec-ch-ua-platform-version"    : "\"10.0.0\"",
                "sec-fetch-dest"                : "empty",
                "sec-fetch-mode"                : "cors",
                "sec-fetch-site"                : "same-origin",
                "user-agent"                    : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            }, cookies=getcookies(),proxies=f"http://{choice(proxies)}")
            return
        except:
            pass

def get_email_data_api(user,pasw,name_acc,thread_id):
 
    imap = imaplib.IMAP4_SSL('outlook.office365.com') ; logged = False
    
    for _ in range(3): # Error Handling Needed
        try:
            imap.login(user, pasw) ; logged = True ; break
        except:
            sleep(1)
            pass
    
    if not logged:
        return False
    
    for i in range(6):
        imap.select('INBOX')

        _, data = imap.search(None, 'ALL')
        email_ids = data[0].split()

        for email_id in email_ids:

            _, msg_data = imap.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            if msg.is_multipart():
                for part in msg.walk():

                    content_type = part.get_content_type()

                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass

                    if content_type == "text/html" and "EMAIL_JOIN" in str(body):
                                
                        body = body.split('"')
                        for sex in body:
                            if "https://www.webtoons.com/" in sex and ";type=EMAIL_JOIN" in sex and ">" not in sex:
                                email_link = sex.replace("&amp",'').replace(";","&")
                                click_email(email_link)

                        imap.close() ; imap.logout()
                        sprint(f"Verified", thread_id, user)

                        return True

    imap.close() ; imap.logout()
    return False


def get_email_custom(user,_,__,thread_id):
    for _ in range(15):
        email_data = get(f"https://api.tidal.lol/api/v1/emails/{user}").json()
        if email_data['emails'] is not None:
            emails = email_data.get('emails', [])
            for mail in emails:
                body = mail.get('body', {})
                html_body = body.get('html', '')
                if "https://www.webtoons.com/" in html_body and "emailVerification" in html_body:
                    click_email(html_body.split('<a href="')[2].split('"')[0])
                    sprint("Verified", thread_id, user)
                    return True
        sleep(5)

    return False            

    
def verify_email(mail,password,name,thread_id):

    if config['email_type'] == "api":
        for _ in range(3):
            verify_mail = get_email_data_api(mail,password,name,thread_id)
            if verify_mail:
                break
    else:
        verify_mail = get_email_custom(mail,password,name,thread_id)


    if not verify_mail:
        return False
    
    return True

def get_mails(thread_id):


    mail_type = "OUTLOOK"

    if config['email_type'] == "api":

        while True:

            buy_response = get(f"https://api.hotmailbox.me/mail/buy?apikey={config['hotmailbox_api_key']}&mailcode={mail_type}&quantity={mail_buy_amount}").json()

            if buy_response['Message'] == 'Bạn đã mua hàng thành công': #  Success Buy

                sprint(f"Purchased Emails", thread_id, buy_response['Data']['Emails'][0]['Email'])

                data_title['email_purchased'] += mail_buy_amount

                for email in buy_response['Data']['Emails']:
                    with Lock():
                        email_list.append(f"{email['Email']}:{email['Password']}")


                sleep(60) # idk we need a better way to do the timer xd


            elif buy_response['Message'] == 'Tồn trên hệ thống không đủ': # Out Of Stock

                mail_type = "OUTLOOK" if mail_type == "HOTMAIL" else "HOTMAIL"

                sprint(f"Error", thread_id, f"{Fore.RED}Out Of Stock, Trying With {mail_type.lower()}")

            elif buy_response['Message'] == "Số dư tài khoản không đủ": # Insufficient Balance

                sprint(f"Error", thread_id, f"{Fore.RED}Insuficient Balance, Stopping Thread.")
                return "nobalance","nobalance"

            else:
                sleep(10)
    else:
        while True:
            for _ in range(thread_count):
                email_list.append(f"{''.join(choice(ascii_letters + digits) for i in range(15))}@{config['custom_mail_domain']}:kianXninjaBestTeam")
                data_title['email_purchased'] += 1

            sleep(60)

def wait_for_server():
    print(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}Waiting For User To Open Server")
    while True:
        try:
            get("http://localhost:6969",timeout=1)
            system("cls||clear")
            return True
        except Exception:
            pass
 
def main_check_key():
    key_balance_check =  get(f"https://api.hotmailbox.me/user/balance?apikey={config['hotmailbox_api_key']}").json()
    
    if key_balance_check['Message'] == "Thành công": # good key, if it is not that response means the key invalid
        if key_balance_check['Balance'] < 10:
            input(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}Bad Key -> {Fore.RED}Balance Too Low: [{key_balance_check['Balance']}]")
            exit()
    else:
        input(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}Invalid Config -> {Fore.RED}Invalid HotMailBox Key | [{config['hotmailbox_api_key']}]")
        exit()

class Sign:
    def __init__(self) -> None:
        self.sign_key = b"gUtPzJFZch4ZyAGviiyH94P99lQ3pFdRTwpJWDlSGFfwgpr6ses5ALOxWHOIT7R1"

    def get_message(self, string, stamp):
        string = string[:min(255, len(string))]
        return string + stamp

    def sign(self, uri):
        mac     = new(self.sign_key, digestmod=sha1)
        stamp   = str(int(time() * 1000))

        mac.update(self.get_message(uri, stamp).encode('utf-8'))

        md      = quote(b64encode(mac.digest()))

        builder = []
        builder.append(uri)
        builder.append('&') if '?' in uri else builder.append('?')

        builder.append("msgpad=" + stamp)
        builder.append("&md="    + md)

        return ''.join(builder)
    
    def chrlen(self, n: str) -> str:
        return chr(len(n))
    
    def encrypt(self, json, mail, pw):
        string  = f"{self.chrlen(json['sessionKey'])}{json['sessionKey']}{self.chrlen(mail)}{mail}{self.chrlen(pw)}{pw}".encode()
        mod     = int(json['nvalue'], 16)
        evl     = int(json['evalue'], 16)
        pbk     = PublicKey(evl, mod)
        out     = rsae(string, pbk)

        return hexlify(out).decode('utf-8')

class Register:
    
    def __init__(self,mail,thread_id) -> None:
        self.pw      = "NinjaAndxKian"
        self.thread_id = thread_id
        self.mail = mail

        self.session = Client(headers = {
            "accept"                        : "*/*",
            "accept-encoding"               : "gzip, deflate, br",
            "accept-language"               : "en-US,en;q=0.9",
            "connection"                    : "keep-alive",
            "content-type"                  : "application/x-www-form-urlencoded; charset=UTF-8",
            "host"                          : "www.webtoons.com",
            "origin"                        : "https://www.webtoons.com",
            "referer"                       : "https://www.webtoons.com/member/join?loginType=EMAIL",
            "sec-ch-ua"                     : "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-full-version-list"   : "\"Google Chrome\";v=\"113.0.5672.93\", \"Chromium\";v=\"113.0.5672.93\", \"Not-A.Brand\";v=\"24.0.0.0\"",
            "sec-ch-ua-mobile"              : "?0",
            "sec-ch-ua-model"               : "\"\"",
            "sec-ch-ua-platform"            : "\"Windows\"",
            "sec-ch-ua-platform-version"    : "\"10.0.0\"",
            "sec-fetch-dest"                : "empty",
            "sec-fetch-mode"                : "cors",
            "sec-fetch-site"                : "same-origin",
            "user-agent"                    : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "x-requested-with"              : "XMLHttpRequest"
        },proxies=f"http://{choice(proxies)}",timeout=10)
        
    def getBirth(self) -> dict:
        return {
            "year"       : "1987",
            "month"      : str(randint(1, 11)),
            "dayOfMonth" : str(randint(1, 20))
        }

    def getData(self) -> dict:
        return self.session.get("https://www.webtoons.com/member/login/rsa/getKeys").json()
    
    def cook(self) -> None:
        self.session.get("https://gak.webtoons.com/v1/web/cookie")

    def register(self) -> str:
        try:
            self.cook()
            self.name   = "".join(choices(ascii_lowercase, k=18))
            url         = "https://www.webtoons.com/member/join/doJoinById"
            json        = self.getData()
            data        = urlencode({
                **self.getBirth(),
                "loginType"         : "EMAIL",
                "nickname"          : self.name,
                "encnm"             : json["keyName"],
                "encpw"             : Sign().encrypt(json, self.mail, self.pw),
                "zoneId"            : "Europe/Berlin",
                "emailEventAlarm"   : "false",
            })

            self.session.post(url, data=data)
            sprint(f"Registered Account." , self.thread_id, self.name)
            return self.name

        except Exception as e:
            Register(self.mail,self.thread_id).register() # Error Handling Needed
            return

class Claim:
    def __init__(self, email, password, name, thread_id) -> None:
        self.session = Client(headers = {
            "accept-encoding"   : "gzip",
            "connection"        : "Keep-Alive",
            "content-type"      : "application/x-www-form-urlencoded", 
            "host"              : "global.apis.naver.com",
            "user-agent"        : "Android/9 Model/SM-N975F com.naver.linewebtoon/2.12.5(2120500,uid:10059) NeoIdSignInMod/0.1.12",
        },proxies=f"http://{choice(proxies)}",timeout=10)

        self.sign       = Sign().sign
        self.email      = email
        self.password   = password
        self.name       = name
        self.thread_id  = thread_id

    def getData(self) -> dict:
        for _ in range(10):
            try:
                return self.session.get(self.sign("https://global.apis.naver.com/lineWebtoon/webtoon/getRsaKey.json?v=1&platform=APP_ANDROID&language=en&serviceZone=GLOBAL&locale=en")).json()["message"]["result"]     
            except:
                continue #sprint(f"Error", self.thread_id, f"{Fore.RED}Failed To Get Data")

    def read(self):

        for page in range(1, 5):
            self.headers_read = {
                "accept-encoding"   : "gzip",
                "connection"        : "Keep-Alive",
                "host"              : "global.apis.naver.com",
                "user-agent"        : "nApps (Android 9; SM-N975F; linewebtoon; 2.12.5)",
                "cookie"            : f'NEO_SES="{self.ses}"'
            }
            params = urlencode({
                "v"             : "2",
                "webtoonType"   : "WEBTOON",
                "titleNo"       : "5291",
                "episodeNo"     : str(page),
                "platform"      : "APP_ANDROID",
                "language"      : "en",
                "serviceZone"   : "GLOBAL&&",
                "locale"        : "en"
            })
            
            url = f"https://global.apis.naver.com/lineWebtoon/webtoon/eventReadLog.json?{params}"
            for _ in range(3):
                try: # Error Handling Needed
                    page_read = self.session.get(self.sign(url), headers=self.headers_read).json()

                    if page_read['message']['result']["progressType"] != "NONE":
                        self.session.get(page_read['message']['result']["pageUrl"],headers={ 
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                "accept-encoding": "gzip, deflate",
                                "accept-language": "en-US,en;q=0.9",
                                "connection": "keep-alive",
                                "host": "m.webtoons.com",
                                "sec-fetch-dest": "document",
                                "sec-fetch-mode": "navigate",
                                "sec-fetch-site": "none",
                                "sec-fetch-user": "?1",
                                "upgrade-insecure-requests": "1",
                                "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-N975F Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.131 Mobile Safari/537.36 linewebtoon/2.12.5 (GLOBAL; EAF)",
                                "x-requested-with": "com.naver.linewebtoon"
                            }, cookies=getcookies())
                    break
                except Exception as e:
                    pass

            

    def claim(self):
        self.session.headers = {
            "accept"            : "application/json, text/plain, */*",
            "accept-encoding"   : "gzip, deflate",
            "accept-language"   : "en-US,en;q=0.9",
            "connection"        : "keep-alive",
            "host"              : "m.webtoons.com",
            "referer"           : "https://m.webtoons.com/app/promotion/read/en_discord_phase1_202305/progress?platform=APP_ANDROID",
            "sec-fetch-dest"    : "empty",
            "sec-fetch-mode"    : "cors",
            "sec-fetch-site"    : "same-origin",
            "user-agent"        : "Mozilla/5.0 (Linux; Android 9; SM-N975F Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.131 Mobile Safari/537.36 linewebtoon/2.12.5 (GLOBAL; EAF)",
            "x-requested-with"  : "com.naver.linewebtoon",
        }

        self.session.cookies    = getcookies()
        self.session.cookies.set("NEO_SES", self.ses)
        for _ in range(10):
            try: # Error Handling Needed
                url = f"https://m.webtoons.com/app/promotion/saveCompleteInfo?promotionName=en_discord_phase1_202305&memo={self.email.replace('@', '%40')}"
                break
            except Exception as e:
                pass

        if self.session.get(url, timeout=15).text == "true":
            sprint(f"Clicked Promotion", self.thread_id, str(self.email))

    def redeem(self):
        json    = self.getData()
        url     = "https://global.apis.naver.com/lineWebtoon/webtoon/loginById.json"
        data   = urlencode({
            "v"            : "2",
            "encnm"        : json["keyName"],
            "encpw"        : Sign().encrypt(json, self.email, self.password),
            "language"     : "en",
            "loginType"    : "EMAIL",
            "serviceZone"  : "GLOBAL",
        })

        self.ses =  self.session.post(url, data=data).json()["message"]["result"]["ses"]
        
        self.session.cookies.set("NEO_SES", self.ses)
        self.session.headers["user-agent"] = "nApps (Android 7.1.2; G011A; linewebtoon; 2.12.5)"

        self.read()

        sprint(f"Read The Pages ", self.thread_id, self.email)
        self.claim()

def main(thread_id):
    while True:
        try:
            
            with Lock():
                while True:
                    try:
                        full_mail = email_list.pop(0)
                        mail = full_mail.split(":")[0]
                        password = full_mail.split(":")[1]
                        break
                    except:
                        sleep(1)
                        pass

            if mail == "nobalance":
                return False
            
            

            name = Register(mail,thread_id).register()
            
            if not verify_email(mail,password,name,thread_id):
                sprint(f"Flagged Or Bad Email / Proxy", thread_id, f"{Fore.RED}Failed To Get Verify Link") 
                data_title['fails'] += 1
                continue

            Claim(mail,"NinjaAndxKian", name,thread_id).redeem()

            post("http://localhost:6969/addemail",json={'user': mail, 'pass': password})
            data_title['finished'] += 1


        except Exception as e:
            sprint(f"Thread Crashed, Restarting.", thread_id, f"{Fore.RED}{e}")
            data_title['fails'] += 1
            continue


if __name__ == "__main__":
    start = time()
    freeze_support()
    system("cls||clear") 
    
    Thread(target=update_title, daemon=True).start() 

    if config['scrape_proxy']:
        Thread(target=proxy_scraper, daemon=True).start() 
        
    if not proxies: 
        input(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}Error -> {Fore.RED}No Proxies") 
        exit() # Check Proxies.TXT

    if config['email_type'] == "api":
        main_check_key()
        Thread(target = fetch_api_balance, daemon=True).start() 
    else:
        data_title['api_bal'] = "Not API"

    wait_for_server()
    
    if config['email_type'] == "api":
        print(f"Amount Of Emails To Buy At Once?")
        mail_buy_amount = int(input(">>> "))
        
    system("cls||clear")

    print(f"Threads?")
    thread_count = int(input(">>> "))

    Thread(target=get_mails, args= (str(0),)).start()

    system("cls||clear")
    
    for i in range(thread_count): 
        Thread(target=main, args= (str(i+1),)).start()
        sleep(0.2)

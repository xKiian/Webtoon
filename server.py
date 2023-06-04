from flask                      import Flask, request, make_response
from threading                  import Thread
from time                       import sleep, time , strftime
from random                     import randint
from re                         import search
from colorama                   import Fore,init
from os                         import system
from requests                   import get
from threading                  import Thread, Lock
import logging
import imaplib
import email

init(autoreset=True)
app = Flask("Ninja x Kian")
logging.getLogger('werkzeug').setLevel(logging.ERROR)
email_list = []
host = "0.0.0.0"
port = 8080

data_title = {
    'promos': 0,
    'emails': 0
}
def update_title():
        while True:
            system('title Promofier Server By NinjaRide x xKian ^> Genned: [%s] ^| Emails: [%s]' % (data_title['promos'],data_title['emails']))
            sleep(.1)


def get_email_api_promo(user,pasw, attempt):

    print(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}Fetching From {Fore.WHITE}-> {Fore.GREEN}{user}:{pasw} {Fore.WHITE}[Attempt: {attempt}]")
    
    imap = imaplib.IMAP4_SSL('outlook.office365.com') ; logged = False
    
    for _ in range(3): # Error Handling Needed
        try:
            imap.login(user, pasw) ; logged = True ; break
        except:
            sleep(1)
            pass
    
    if not logged:
        return False
    

    imap.select('INBOX')
    
    _, data = imap.search(None, 'ALL')
    email_ids = data[0].split()
    
    for email_id in email_ids:

        _, msg_data = imap.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
    
        if msg.is_multipart():
            for part in msg.walk():
                    
                content_type = part.get_content_type()
                
                if content_type == 'text/html':
                    
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass

                    if "https://promos.discord.gg/" in body:
                        
                        promo_re = search(r"https:\/\/promos\.discord\.gg\/(\w+)", body)

                        print(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.MAGENTA}Fetched Promo {Fore.WHITE}-> {Fore.GREEN}{promo_re.group(1)}")
                        open("output/promos.txt","a", encoding='utf-8').write(f"https://promos.discord.gg/{promo_re.group(1)}\n")
                        data_title['promos'] += 1

                        imap.close() ; imap.logout()
                        return True

    imap.close() ; imap.logout()
    return False

def get_email_custom_promo(user, attempt):
    
    print(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}Fetching From {Fore.WHITE}-> {Fore.GREEN}{user} {Fore.WHITE}[Attempt: {attempt}]")


    email_data = get(f"https://api.tidal.shop/api/v1/emails/{user}").json()
    
    if email_data['emails'] is not None:
        emails = email_data.get('emails', [])
        for mail in emails:
            body = mail.get('body', {})
            html_body = body.get('html', '')
            if "https://promos.discord.gg/" in html_body:
                
                print(html_body)
                promo_re = search(r"https:\/\/promos\.discord\.gg\/(\w+)", body)

                print(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.MAGENTA}Fetched Promo {Fore.WHITE}-> {Fore.GREEN}{promo_re.group(1)}")
                open("output/promos.txt","a", encoding='utf-8').write(f"https://promos.discord.gg/{promo_re.group(1)}\n")
                data_title['promos'] += 1

                return True

    return False

def check_email(email):
    if  time() - email['time'] > 60 and email['attempts'] <= 90: # If 60 seconds have not passed , and it has not done 10 attempts then try to fetch promo
        with Lock():
            email['time'] = time() # reset timer
            email['attempts'] += 1
        


        if email['pass'] != "kianXninjaBestTeam":
            for _ in range(3):
                try:
                    if get_email_api_promo(email['user'],email['pass'],email['attempts']):
                           with Lock():
                                email_list.remove(email) 
                    break

                except:
                    sleep(randint(1,10))
                    pass
        
        else:
            if get_email_custom_promo(email['user'],email['attempts']):
                    with Lock():
                        email_list.remove(email) 

                
 
    elif email['attempts'] >= 90: # Check the attempts, and remove it
        with Lock():
            email_list.remove(email)
        
        print(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}Failed To Fetch From {Fore.WHITE}-> {Fore.RED}{email['user']}:{email['pass']} {Fore.WHITE}[Removing...]")
        
def email_promo():
    while True:
        for email in email_list:
            Thread(target=check_email,args=(email,)).start()
            sleep(0.01)
            

@app.route("/")
def main_route():
    return """NinjaRide X xKian PromoGen Active"""

@app.route("/addemail", methods=["post"])
def license_route():
    data = request.get_json()
    data_title['emails'] += 1
    email_list.append({
                        'user': data['user'],
                        'pass': data['pass'],
                        'attempts': 0,
                        'time': time()
                       })
    
    print(f"{Fore.LIGHTBLACK_EX}{strftime('%H:%M:%S')} | {Fore.LIGHTWHITE_EX}New Email {Fore.WHITE}-> {Fore.GREEN}{data['user']}:{data['pass']}")

    response = make_response({"message": "success"})
    response.status = "200"
    return response

Thread(target=email_promo,daemon=True).start()
Thread(target=update_title,daemon=True).start()
app.run(host="0.0.0.0", port=6969)

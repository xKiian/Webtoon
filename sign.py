# webtoons sign reversed
from rsa             import PublicKey, encrypt as rsae
from binascii        import hexlify
from urllib.parse    import quote
from hmac            import new
from hashlib         import sha1
from time            import time, time
from base64          import b64encode


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

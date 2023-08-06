import random
import string
def createEmailPwd(firstname=None,lastname=None):
    if firstname and lastname:
        email = firstname+'.'+lastname+"@honeywell.com"
        letters = string.ascii_lowercase
        pwd = ''.join(random.choice(letters) for i in range(6))
        return (email,pwd)
    else:
        return "provide firname and lastname"


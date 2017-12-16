import pytesseract
import requests
from PIL import Image
from io import BytesIO
import json
import pyrebase

url = "http://www.indianrail.gov.in/enquiry/captchaDraw.png?1513338229865"
cookies = ""
db = ""


def convert(url):
    global cookies
    response = requests.get(url)
    cookies = response.cookies
    img = Image.open(BytesIO(response.content))
    img = img.resize((int(img.size[0])*2,int(img.size[1])*2), Image.ANTIALIAS)
    bg = Image.new("RGB", img.size, (255,255,255))
    bg.paste(img,img)
    # bg.save('colors.jpg')
    text = pytesseract.image_to_string(bg,config="-c tessedit_char_whitelist=0123456789+-= -psm 6")
    print(text)
    return text

def decode(number_string):
    if '+' in number_string:
        splitter="+"
        add=1
    else:
        splitter="-"
        add=0


    data = number_string.split(splitter)
    a=int(data[0])
    b=int(data[1].split("=")[0])
    if add:
        result=a+b
    else:
        result=a-b
    print(a,splitter,b,"=",result)
    return result



def finalRequest(ans):
    global cookies
    # r = requests.get('http://www.indianrail.gov.in/enquiry/SEAT/SeatAvailability.html?locale=en')
    # c = r.cookies
    # i = c.items()
    # for name, value in i:
    #     print(name, value)

    send_req = "http://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha="+str(ans)+"&trainNo=18189+-+TATA+ALLP+EXP&dt=16-12-2017&sourceStation=TATANAGAR+JN+-+TATA&destinationStation=ALLEPPEY+-+ALLP&classc=SL&quota=GN&inputPage=SEAT&language=en&_=1212395517727"
    send_req1= "http://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha="+str(ans)+"&trainNo=18189+-+TATA+ALLP+EXP&inputPage=TRAIN_SCHEDULE&language=en&_=1513413172999"
    data= requests.get(send_req,cookies=cookies)
    # print(r2.text)
    print(json.dumps(data.text, sort_keys=True, indent=4))


def firebaseinit():
    global db
    config = json.load(open('data.hd'))
    firebase = pyrebase.initialize_app(config)
    print(firebase)
    db = firebase.database()
    # db.child("users").child("Morty")
    data = {"name": "Mortimer 'Morty' Smith"}
    db.child("users").child("Morty3").set(data)

# while(1):
#     finalRequest(decode(convert(url)))

finalRequest(decode(convert(url)))
firebaseinit()
import pytesseract
import requests
from PIL import Image
from io import BytesIO
import json
import pyrebase
import threading
import datetime
import time



# The immediate work left:
# 1) Re-request if request fails for the same train.
# 2) Strategy for requesting during tatkal to get a  seat availabilty trend


lock = threading.Lock()
cookies = ""
db = ""

# the funcion converts the url capcha to text
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
    # print(text)
    return text

# string to math logic
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
    # print(a,splitter,b,"=",result)
    return result


# request with the captcha result to the sever for train list. The request string in the function can be modified to extract different json data fromt he server
def finalRequest(ans,trainNo):
    global cookies
    # r = requests.get('http://www.indianrail.gov.in/enquiry/SEAT/SeatAvailability.html?locale=en')
    # c = r.cookies
    # i = c.items()
    # for name, value in i:
    #     print(name, value)
    
    # send_req = "http://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha="+str(ans)+"&trainNo=18189+-+TATA+ALLP+EXP&dt=16-12-2017&sourceStation=TATANAGAR+JN+-+TATA&destinationStation=ALLEPPEY+-+ALLP&classc=SL&quota=GN&inputPage=SEAT&language=en&_=1212395517727"
    send_req= "http://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha="+str(ans)+"&trainNo="+ trainNo +"&inputPage=TRAIN_SCHEDULE&language=en&_=1513413172999"
    data= requests.get(send_req,cookies=cookies)
    # print(r2.text)
    # print(json.loads(data.text)["trainNumber"])
    return json.loads(data.text)


# initialisation for the firebase. Needs a file data.hd with the config details of the firebase account
def firebaseinit():
    global db
    config = json.load(open('data.hd'))
    firebase = pyrebase.initialize_app(config)
    print(firebase)
    db = firebase.database()
    # db.child("users").child("Morty")
    data = {"name": "Mortimer 'Morty' Smith"}
    db.child("users").child("Morty3").set(data)


# writing data to firebase 
def firebasewrite(data,trainname):
    global db
    db.child("Train_del").child(trainname).set(data)

# getting the list of train
def get_train_list():
    send_req = "http://www.indianrail.gov.in/enquiry/FetchTrainData?_=1513413172999"
    data= requests.get(send_req)
    return data.text
# while(1):
#     finalRequest(decode(convert(url)))


# get the train details especially for day availabilty validity and station list
def write_train_names():
    train_list = json.loads(get_train_list())
    captcha_url = "http://www.indianrail.gov.in/enquiry/captchaDraw.png?1513338229865"
    for train in train_list:        
        t = threading.Thread(target = firebasewrite, args = (finalRequest(decode(convert(captcha_url)),train.replace(" ","+")),train,))
        threads.append(t)
        t.start()

        print(train.replace(" ","+"))
        


def get_train_data(train_name):
    global db
    all_users = db.child("Train_del").get()
    for user in all_users.each():
        print(user.key()) # 05817 - APDJ DBB SPECIAL
        user_str = json.dumps(user.val())
        user_json = json.loads(user_str)        
        # print(user_json)
        if "stationList" in user_str:
            # print(len(user_json["stationList"]))
            last_item = len(user_json["stationList"])
            start_station=(user_json["stationList"][0]["stationName"] +" - " + user_json["stationList"][0]["stationCode"]).replace(" ","+")
            end_station=(user_json["stationList"][last_item-1]["stationName"] +" - " + user_json["stationList"][last_item-1]["stationCode"]).replace(" ","+")
            print(start_station)
            print(end_station)
            break
        else:
            db.child("Train_del").child(user.key()).remove()
            print("Removed")
        # print(json.loads(user.val()).serverId)



# this function gets the train status
def get_train_status(train_num):
    global db
    all_users = db.child("Train_del").get()
    for user in all_users.each():
        if train_num not in user.key():
            continue
        
        user_str = json.dumps(user.val())
        user_json = json.loads(user_str)
        if "stationList" not in user_str:
            print("The data in the database does not have station list")
            exit

        # print(len(user_json["stationList"]))
        last_item = len(user_json["stationList"])
        start_station=(user_json["stationList"][0]["stationName"] +" - " + user_json["stationList"][0]["stationCode"]).replace(" ","+")
        end_station=(user_json["stationList"][last_item-1]["stationName"] +" - " + user_json["stationList"][last_item-1]["stationCode"]).replace(" ","+")
        trainNo = user.key().replace(" ","+")
        print(start_station)
        print(end_station)
        print(trainNo)


        captcha_url = "http://www.indianrail.gov.in/enquiry/captchaDraw.png?1513338229865"
        
        
        # data for tomorrow
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(1)
        date_tomorrow = datetime.datetime.strftime(tomorrow,'%d-%m-%Y')




        f= open("guru99.txt","a")
        start_time = datetime.datetime(2018, 2, 23,10,0,0,0)
        stop_time = datetime.datetime(2018, 2, 23,10,20,10,0)
        
        print("Sleeping")
        # do not proceed loop
        while(datetime.datetime.now()< start_time):
            # print("Sleeping")
            time.sleep(2)
        print("Starting.....")
            
        global cookies
        
        while (datetime.datetime.now()<= stop_time):
            # captcha answer  
            ans = decode(convert(captcha_url))
            # SL and 3A are the classes
            send_req = "http://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha="+\
            str(ans)+"&trainNo="+ trainNo +"&dt="+ str(date_tomorrow) + "&sourceStation="+\
            start_station+"&destinationStation="+end_station+"&classc=3A&quota=TQ&inputPage=SEAT&language=en&_=1513413172999"
            data = requests.get(send_req,cookies=cookies)
            # print( str(datetime.datetime.today()) +" Query Date:" + json.loads(data.text)["avlDayList"][0]["availablityDate"])
            # print(json.loads(data.text)["avlDayList"][0]["availablityStatus"]+"\n")
            print("#", sep=' ', end='', flush=True)
            # jj.append([str(datetime.datetime.today()), json.loads(data.text)["avlDayList"][0]["availablityStatus"]])
            time.sleep(1)
            f.write(str(datetime.datetime.today())+" , "+ str(json.loads(data.text)["avlDayList"][0]["availablityStatus"])+"\n")
        # print(jj)
        
        # data = json.dumps(jj,indent=4)
        f.close()

        
        # now this loop is for the sleeper--------------------------------------------

        f= open("guru99_SL.txt","a")
        start_time = datetime.datetime(2018, 2, 23,11,0,0,0)
        stop_time = datetime.datetime(2018, 2, 23,11,20,10,0)
        print("Sleeping")
        # do not proceed loop
        while(datetime.datetime.now()< start_time):
            # print("Sleeping")
            time.sleep(2)
        print("Starting.....")
            

        
        while (datetime.datetime.now()<= stop_time):
            # captcha answer  
            ans = decode(convert(captcha_url))
            # SL and 3A are the classes
            send_req = "http://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha="+\
            str(ans)+"&trainNo="+ trainNo +"&dt="+ str(date_tomorrow) + "&sourceStation="+\
            start_station+"&destinationStation="+end_station+"&classc=SL&quota=TQ&inputPage=SEAT&language=en&_=1513413172999"
            data = requests.get(send_req,cookies=cookies)
            # print( str(datetime.datetime.today()) +" Query Date:" + json.loads(data.text)["avlDayList"][0]["availablityDate"])
            # print(json.loads(data.text)["avlDayList"][0]["availablityStatus"]+"\n")
            print("#", sep=' ', end='', flush=True)
            # jj.append([str(datetime.datetime.today()), json.loads(data.text)["avlDayList"][0]["availablityStatus"]])
            time.sleep(1)
            f.write(str(datetime.datetime.today())+" , "+ str(json.loads(data.text)["avlDayList"][0]["availablityStatus"])+"\n")
        # print(jj)
        
        # data = json.dumps(jj,indent=4)
        f.close()







    print("get the train status for the day")



       




threads = []
firebaseinit()

# write_train_names()
# get_train_data("train_name")
get_train_status("18189")

print("Finish")
# For requesting tatkal
# http://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha=734&trainNo=
# 18189+-+TATA+ALLP+EXP&dt=22-02-2018&sourceStation=TATANAGAR+JN+-+TATA&destinationStation=
# ALLEPPEY+-+ALLP&classc=SL&quota=TQ&inputPage=SEAT&language=en&_=1519274588661
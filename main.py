import pytesseract
import requests
from PIL import Image
from io import BytesIO

url = "http://www.indianrail.gov.in/enquiry/captchaDraw.png?1513338229865"


response = requests.get(url)
img = Image.open(BytesIO(response.content))
bg = Image.new("RGB", img.size, (255,255,255))
bg.paste(img,img)
bg.save('colors.jpg')
text = pytesseract.image_to_string(bg)

print(text)
import datetime, os
from io import BytesIO
import webbrowser
from PIL import	Image, ImageFilter,	ImageDraw, ImageFont, ImageEnhance
from random	import choice, shuffle
import requests

def	days_till_christmas():
	# get current date
	now	= datetime.datetime.now()

	# if has passed, get next year's christmas
	if now.month == 12 and now.day > 25:
		christmas =	datetime.datetime(now.year +1, 12, 25)
	else:
		christmas =	datetime.datetime(now.year,	12,	25)

	return (christmas -	now).days


def	get_image():
	SEARCH_TERMS = ["Christmas", "Christmas	wallpaer", "Christmas background", "Santa",	"Xmas"]
	
	response = requests.get("https://api.unsplash.com/photos/random",
			params={
			"client_id": os.getenv("UNSPLASH_ACCESS_KEY"),
			"query": (search_term := choice(SEARCH_TERMS)),
			"orientation": "squarish",
			"content_filter": "high"
		}
	)
 
 
	return (response.json(), search_term)

#max Bluesky API file size in KB
MAX_FILESIZE = 976.56 #This	is here	for	reference, but is not used in the code

def	create_download_url(response_json):
	return(response_json['urls']['raw']	+ "&" + ("h" if response_json["width"] > response_json["height"] else "w") + "=600&q=75&fm=png")

def	download_image(image_url):
	response = requests.get(image_url)
	return response.content

#image_url = create_download_url(get_image()[0])

#currently using a hard-coded image so that the API doesn't get called too much
cur_img	= Image.open(BytesIO(download_image("https://images.unsplash.com/photo-1669846510648-95ffffb8e269?ixid=M3w1NTE5NDF8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDUwOTAzMTJ8&ixlib=rb-4.0.3&w=600&q=75&fm=png")))

current_days_till_christmas= 10 #Please	make this calculate	the	days until Christmas

# crop image into square
width, height =	cur_img.size
length = min(width,	height)	 # use the smaller dimension
left = (width -	length)/2
top	= (height -	length)/2
right =	(width + length)/2
bottom = (height + length)/2
cur_img	= cur_img.crop((left, top, right, bottom))

#resize	image
cur_img	= cur_img.resize((600, 600))

#update	width and height
width, height =	(600, 600)

# add effects to image
cur_img	= cur_img.filter(ImageFilter.GaussianBlur(12))

# darken the image
enhancer = ImageEnhance.Brightness(cur_img)
cur_img	= enhancer.enhance(0.8)	 # reduce brightness to 80%

# add day to image
text_on_image =	ImageDraw.Draw(cur_img)

# set font size based on number of days
if len(str(current_days_till_christmas)) == 1:
	font = ImageFont.truetype("./python/fonts/Candcu__.ttf", 450)

elif len(str(current_days_till_christmas)) == 2:
	font = ImageFont.truetype("./python/fonts/Candcu__.ttf", 400)

else:
	font = ImageFont.truetype("./python/fonts/Candcu__.ttf", 320)

# draw number on image
text_on_image.text((width/2, height/2),	str(current_days_till_christmas+1),	font=font, anchor="mm")

# currently not working 
#draw "Days	until Christmas" on image
font = ImageFont.truetype("./python/fonts/Smiling.otf", 36)

if current_days_till_christmas+1 == 1:
	text_on_image.text((width/2, height/2 +	450), "Day until Christmas!", font=font, anchor="mm")
else:	
	text_on_image.text((width/2, height/2 +	450), "Days	until Christmas!", font=font, anchor="mm")
	
# save image
cur_img.save(f"./currentImage.png")
	
	
# https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil'''
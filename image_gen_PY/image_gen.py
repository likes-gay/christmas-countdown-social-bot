import datetime, os, json
from io import BytesIO
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
from PIL.PngImagePlugin import PngInfo
from random import choice
import requests


today_date = datetime.date.today()
christmas_date = datetime.date(today_date.year, 12, 25)

days_until_christmas = (christmas_date - today_date).days
print("There are", days_until_christmas, "days until Christmas!")

def get_image():
	SEARCH_TERMS = ["Christmas", "Christmas wallpaer", "Christmas background", "Santa", "Xmas"]

	response = requests.get("https://api.unsplash.com/photos/random",
			params={
			"client_id": os.getenv("UNSPLASH_CLIENT_ID"),
			"query": (search_term := choice(SEARCH_TERMS)),
			"orientation": "squarish",
			"content_filter": "high"
		}
	)

	print("Getting picture using search term:", search_term)

	try:
		res_json = response.json()
		print("Successfully got image from Unsplash API.")

	except json.decoder.JSONDecodeError:
		print("Unsplash API response was not valid JSON.")
		exit()

	if response.status_code != 200:
		print(f"Unsplash API responded with status code {response.status_code} and error message: {res_json['errors'][0]}.")
		exit()

	return res_json

if not os.path.exists("image_log.txt"):
	open("image_log.txt", "x").close()

with open("image_log.txt", "a+") as f:
	array_of_used_ids = f.read().split("\n")

	image_json = get_image()

	while image_json["id"] in array_of_used_ids:
		image_json = get_image()
		print(f"Image {image_json['id']} has already been used, getting another image...")

	f.write(image_json["id"] + "\n")

MAX_FILESIZE = 976.56 #This is here for reference, but is not used in the code

image_url = (image_json["urls"]["raw"] + "&" + ("h" if image_json["width"] > image_json["height"] else "w") + "=600&q=75&fm=png")

image_download = requests.get(image_url).content

#currently using a hard-coded image so that the API doesn't get called too much
cur_img = Image.open(BytesIO(image_download))

del image_json, image_download

# crop image into square
width, height = cur_img.size
length = min(width, height) # use the smaller dimension
left = (width - length)/2
top = (height - length)/2
right = (width + length)/2
bottom = (height + length)/2
cur_img = cur_img.crop((left, top, right, bottom))

#resize image
cur_img = cur_img.resize((600, 600))

# add effects to image
cur_img = cur_img.filter(ImageFilter.GaussianBlur(6))

# darken the image
enhancer = ImageEnhance.Brightness(cur_img)
cur_img = enhancer.enhance(0.8) # reduce brightness to 80%

# add day to image
text_on_image = ImageDraw.Draw(cur_img)

# set font size based on number of days
if len(str(days_until_christmas)) == 1:
	font = ImageFont.truetype("./fonts/Candcu__.ttf", 450)

elif len(str(days_until_christmas)) == 2:
	font = ImageFont.truetype("./fonts/Candcu__.ttf", 400)

else:
	font = ImageFont.truetype("./fonts/Candcu__.ttf", 320)

# draw number on image
text_on_image.text((width/2, height/2), str(days_until_christmas), font=font, anchor="mm")

#draw "Days until Christmas" on image
font = ImageFont.truetype("./fonts/Smiling.otf", 50)

text_on_image.text((width/2, height/2 + 200), "Days until Christmas!" if days_until_christmas != 1 else "Day until Christmas!", font=font, anchor="mm")

# Create caption for image

CHRISTMAS_EMOJIS = ["🎄", "🎅", "🎁", "❄️", "⛄", "🔔", "🕯️",
                    "🌟", "🎉", "🦌", "🤶", "🍪", "🥛", "🎶",
                    "👼", "🍭", "🎀", "🦌", "🏡", "🌲", "🍬",
                    "🧦", "🎊", "🛷", "🔥", "🎁"]

caption = f"There are {days_until_christmas} days until Christmas! {choice(CHRISTMAS_EMOJIS)}{choice(CHRISTMAS_EMOJIS)}"

metadata = PngInfo()
metadata.add_text("caption", caption)
metadata.add_text("days_until_christmas", str(days_until_christmas))


# save image
cur_img.save(f"../currentImage.png", pnginfo=metadata)
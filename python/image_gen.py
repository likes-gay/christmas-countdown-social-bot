from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
import os
from random import shuffle

list_of_images = os.listdir('./unchanged_images')
shuffle(list_of_images)

for i, image in enumerate(list_of_images):
    cur_img = Image.open(f'./unchanged_images/{image}')

    # crop image into square
    width, height = cur_img.size
    length = min(width, height)  # use the smaller dimension
    left = (width - length)/2
    top = (height - length)/2
    right = (width + length)/2
    bottom = (height + length)/2
    cur_img = cur_img.crop((left, top, right, bottom))
    
    #resize image
    cur_img = cur_img.resize((3500, 3500))
    
    #update width and height
    width, height = (3500, 3500)
    
    # add effects to image
    cur_img = cur_img.filter(ImageFilter.GaussianBlur(12))
    
    # darken the image
    enhancer = ImageEnhance.Brightness(cur_img)
    cur_img = enhancer.enhance(0.5)  # reduce brightness to 50%
    
    # add day to image
    
    text_on_image = ImageDraw.Draw(cur_img)
    font = ImageFont.truetype('./fonts/Candcu__.ttf', 1900)
    
    # draw number on image
    text_on_image.text((width/2, height/2), str(i+1), font=font, anchor="mm")
    
    #draw "Days until Christmas" on image
    font = ImageFont.truetype('./fonts/Christmas Smiling.otf', 410)
    
    if i+1 == 1:
        text_on_image.text((width/2, height/2 + 1000), "Day until Christmas!", font=font, anchor="mm")
    else:    
        text_on_image.text((width/2, height/2 + 1000), "Days until Christmas!", font=font, anchor="mm")
    
    # save image
    cur_img.save(f'../images/{i+1}.png')
    
    
# https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil
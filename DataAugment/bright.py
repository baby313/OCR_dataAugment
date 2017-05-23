from PIL import Image
from PIL import ImageEnhance

imageName = "/users/xiuxiuzhang/desktop/1.jpg"
image = Image.open(imageName)
#image1 = image.crop([100,50,300,300])
brightness = ImageEnhance.Brightness(image)
bright_img = brightness.enhance(1.07)
#image.paste(bright_img,[100,50,300,300])
brightname = "/users/xiuxiuzhang/desktop/12.jpg"
bright_img.save(brightname)
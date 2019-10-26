from PIL import Image, ImageDraw

img = Image.new("RGB", (100, 30), color=(33, 33, 33))
img.save("toto.png")

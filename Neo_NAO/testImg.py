from PIL import Image

image = Image.open('carte.png')

# rotate 270 degrees counter-clockwise
imRotate = image.rotate(-90)
filename = "imgRotate.png"
imRotate.save(filename)


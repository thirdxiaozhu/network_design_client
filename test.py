from PIL import Image
image = Image.open("3.PNG")
print(image.format)
image = image.convert("RGB")
image.format = "JPEG"
print(image.format)
image.save("1aa.JPEG",quality=10,optimize=True)

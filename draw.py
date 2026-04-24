from PIL import Image, ImageDraw

def rect(image: Image.Image, texture: Image.Image, x: float, y: float, angle: float):
    image.paste(texture.rotate(angle), (x, y))
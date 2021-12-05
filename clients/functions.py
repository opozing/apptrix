from PIL import Image


def watermark(input_image_path):
    """
    Создает водяной знак на аватарку.
    """
    base_image = Image.open(input_image_path)
    watermark = Image.open('watermark.png')
    base_image.paste(watermark, (0, 0), watermark)
    image = base_image.save(str(input_image_path))
    return image

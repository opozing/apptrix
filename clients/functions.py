from PIL import Image
from django.core.mail import send_mail


def watermark(input_image_path):
    """
    Создает водяной знак на аватарку.
    """
    base_image = Image.open(input_image_path)
    watermark = Image.open('watermark.png')
    base_image.paste(watermark, (0, 0), watermark)
    image = base_image.save(str(input_image_path))
    return image


def send_email(user, user_like):
    """
    Отправляет пользователю письмо с уведомлением о взаимном лайке.
    """
    send_mail(
        '',
        f'Вы понравились {user.first_name}, Почта участника:{user.email}',
        'testworkapptrix@yandex.ru',
        [user_like.email],
        fail_silently=False,)

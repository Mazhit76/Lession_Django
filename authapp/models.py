from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.timezone import now



class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='возраст', default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
    #
    # def __str__(self):
    #     return self.username

class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = "W"
    GENDER_CHOICES = (
        (None, 'Введите Ваш пол'),
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )
    # Это сделано для тоо чтобы потом можно было к переменной обращаться через .MALE или .FEMALE

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    # записи -уникальны,   нулевые значения-нет,  для поля создать индекс, при удаление все связанные записи удалить
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    # сокр имя в единств числе, мас длина 128, могут быть пустые поля
    aboutME = models. TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='', max_length=1, choices=GENDER_CHOICES, blank=True)
    #     выбор из M  или W

    @receiver(post_save, sender=User)
    # Это функция обертка для создания сигнала другим приложениям о окончании выполенения сохранения
    # sender - Класс модели, для которого только что был создан экземпляр.
    # instance - Фактический экземпляр только что созданной модели.
    # created- Логическое значение; True если была создана новая запись.
    # **kwargs-это обязательное переменнная так как пользователи в любой момент могут отправить данные и
    #  и приложение должно уметь их обрарбатывать
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    #         Здесь создали и сохранили в базу объект

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
        # Здесь мы получили объект который был сохранен ранее,


        # это ccылка на UserProfile в виде userprofile, через OneToOneField и его сохраняем

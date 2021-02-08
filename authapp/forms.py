import hashlib, random


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from authapp.models import User
from authapp.models import UserProfile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
            field.help_text = ''

    def save(self):

        user = super(UserRegisterForm, self).save()
        # переоперделяем создаваемого пользователя и сохраняем его
        user.is_active = True

        # пользователь активный
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        # Создаем соль
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        # Создаем ключи +солим
        user.save()
        # Сохраняем пользователя и возвращаем пользователя
        return user

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды')
        return data

class UserProfileForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Теперь все формам присвоен класс с пользовательскими стилями  и можно использовать
            field.widget.attrs['class'] = 'form-control py-4'
        # и задавть формы отсюда а не в html

        # Здесь мы поставили ниже, чтобы переопределить классы
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'


    # Но все-таки это объект, и поэтому
    # вы можете присвоить его переменной
    # вы можете скопировать его
    # вы можете добавить к нему атрибуты
    # вы можете передать его в качестве параметра функции
    # Метаданные модели - это «все, что не является полем»,
    #         например параметры упорядочения ( ordering), имя таблицы базы данных ( db_table)
    #         или удобочитаемые имена в единственном и множественном числе ( verbose_name и verbose_name_plural).
    #         Который позволяет добавлять дополнительные параметры в класс с помощью class Meta .
    #         Он определяет такие вещи, как доступные разрешения, связанное имя таблицы базы данных,
    #         является ли модель абстрактной или нет, сингулярная и множественная версии имени и т.д.
    #           type -это просто класс, который создает объекты класса.


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tagline', 'aboutME', 'gender')

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

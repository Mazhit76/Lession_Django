from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from authapp.models import User
from authapp.forms import UserProfileEditForm
from basketapp.models import Basket

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm


# from basketapp.models import Basket

# Create your views here.


def login(request):
    # форму заполняем данными полученными с сайта POST

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # Объявили форму и метод
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # Здесь мы проверяем и проводим авторизацию, если все правильно то
            # Отправляем на главную страницу
            user = auth.authenticate(username=username, password=password)
            # этот метод берет данные из б.д. пользователей и проверяет на
            # совпадение и на его активность
            if user and user.is_active:
                # Здесь нужно будет раобраться потомучто при создании пользователя в формах проводилась проврека на
                # выставление авторизация-нет. Из-за этого выходила ошибка. Сейчас стоит истина и работает.
                auth.login(request, user)  # Производлим авторизацию
                # отправляем главную страницу
                return HttpResponseRedirect(reverse('main'))
    else:
        form = UserLoginForm()
    context = {'form': form}  # Форму передали в контекст
    return render(request, 'authapp/login.html', context)


# @transaction.atomic
# Not work edit
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    baskets = Basket.objects.filter(user=request.user)
    context = {
        'title': 'Профиль',
        'form': form,
        'profile_form': profile_form,
        'baskets': baskets,
    }
    return render(request, 'authapp/profile.html', context)


def register(request):
    title = 'Регистрация'

    # Выдавал ошибку проверку взял с файла уроку 4
    if request.method == 'POST':
        # Создаем новую форму и передаем ей данные из запроса
        form = UserRegisterForm(request.POST)
        if form.is_valid():  # Здесь мы проверяем методам джанго правильность ввода логина и имени
            user = form.save()

            # Add let user1
            if send_verify_email(user):
                print('Сообщение подтверждения отправленно!')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                print('Ошибка отправки сообщения!')
                return HttpResponseRedirect(reverse('authapp:login'))
                # Если все ок то сохраняем форму
            messages.success(request, 'Вы успешно зарегистрировались!')
            new_user = auth.authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
            auth.login(request, new_user)
            # Если все правильно то авторизуем и отправляем на страницу товаров
            return HttpResponseRedirect(reverse('mainapp:index'))
    # Если неправильно то заново создаем метод создания формы
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        # 'baskets': Basket.objects.filter(user=request.user)
        # Дополнительно передали данные корзины и пользвателя корзины
    }  # Форму передали в контекст

    return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)  # Может быть ошибка
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            if user.is_activation_key_expired():
                user.activation_key = None  # Я так понял здесь препод убирает ключ активаци после проверки, чтобы одноразовая
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user: {e.args}')
        return HttpResponseRedirect(reverse('main'))  # Надо проверить эту ссылку


def send_verify_email(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    # Здесь ошибка должно быть заполение страницы добавлен код отображения и activation_key такого нет ругается
    subject = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username}' \
              f' на портале {settings.DOMAIN_NAME} перейдите по ссылке: ' \
              f'\n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

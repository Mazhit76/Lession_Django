from authapp.views import login
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from mainapp.models import Product
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required

from mainapp.models import Product
from basketapp.models import Basket


from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def basket_add(request, id=None):
    product = get_object_or_404(Product, id=id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        basket = Basket(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # Берем из словаря абсолютный путь, если он там есть если нет то вывод,
        # что его там нет ошибки не будет


@login_required
def basket_remove(request, id=None):
    basket = Basket.objects.get(id=id)
    if basket.quantity > 1:
        basket.quantity -= 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
# К этому методу мы обращамся из AJAX запроса, это сделанно для асинхронности.
# Получае как раз 3 переменные которые он нам отправляет и с ними уже работаем
# Изменея предстваление страницы, но не рендерим а отправляем его в JSONResponce
def basket_edit(request, id, quantity):
    if request.is_ajax():
        # Если у нас AJAX запрос то:
        quantity = int(quantity)
        basket = Basket.objects.get(id=int(id))
        # здесь должны передать в числовом формате
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        # Здесь мы удалили после того как поставили контестный процессор in mainapp
        #  Вроде как работает. Авторизовался и выбрал 2 покупки они в корзине
        #  Хотя до конца не понял как работает, то есть в каждом обработчике этот метод присутствует в любом случае
        #  Это очень опасно засорением и задержками
        # baskets = Basket.objects.filter(user=request.user)
        # context = {
        #     'baskets': baskets,
        # }


        result = render_to_string('basketapp/basket.html', context)
        return JsonResponse({'result': result})
        # Здесь указаваем куда отправить и что отправить

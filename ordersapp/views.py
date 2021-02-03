from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm



class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    # поля не нужны
    success_url = reverse_lazy('ordersapp:orders')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # Получили от родителя
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)
        #  Первый позиционный аргумент - родительский класс, второй - класс,
        #  на основе которого будет создаваться набор форм класса,
        #  указанного в именованном аргументе «form=OrderItemForm».
        #  Аргумент «extra» позволяет задать количество новых форм в наборе.
        #  Метод «inlineformset_factory()» возвращает нам конструктор набора форм.
        #  Как и при работе с обычными формами, мы можем использовать аргументы «initial»
        #  и «instance» для передачи начальных данных или объекта в форму exra=1 предуставленная форма мин 1

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            # basket_items = Basket.get_items(self.request.user)
            #
            # if len(basket_items):
            #     OrderFormSet = inlineformset_factory(Order, OrderItem,
            #                                          form=OrderItemForm, extra=len(basket_items))
            #     formset = OrderFormSet()
            #     for num, form in enumerate(formset.forms):
            #         form.initial['product'] = basket_items[num].product
            #         form.initial['quantity'] = basket_items[num].quantity
            #     basket_items.delete()
            # else:
            #     formset = OrderFormSet()
            formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            #  для защиты от сбоев, если что откатывается
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)



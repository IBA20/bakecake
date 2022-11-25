import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.conf import settings
from users.models import CustomUser
from yookassa import Payment

from bakecakeapp.models import Ingredient, Order

from .forms import CreateCakeForm


def create_payment(amount):
    payment = Payment.create(
        {
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.YOOKASSA_RETURN_URL
            },
            "description": "Оплата: торт на заказ"
        }
    )
    return payment.id, payment.confirmation.confirmation_url


def index(request):
    cake_form = CreateCakeForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
        else:
            try:
                user = CustomUser.objects.get(
                    phonenumber=request.POST['PHONE']
                )
            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create_user(
                    phonenumber=request.POST['PHONE'],
                    password='1234',
                    email=request.POST['EMAIL'],
                )
        order = Order(
            user=user,
            writing=request.POST['WORDS'],
            comments=request.POST['COMMENTS'],
            delivery_address=request.POST['ADDRESS'],
            delivery_time=datetime.fromisoformat(
                f"{request.POST['DATE']}T{request.POST['TIME']}"
            ),
            courier_info=request.POST['DELIVCOMMENTS'],
        )
        ingred_fields = ['levels', 'topping', 'shape', 'berries', 'decor']
        ingred_ids = [
            int(request.POST.get(field)) for field in ingred_fields if
            request.POST.get(field)
        ]
        order.value = Ingredient.objects\
            .filter(id__in=ingred_ids)\
            .aggregate(Sum('price'))['price__sum']
        payment_id, payment_url = create_payment(order.value)
        order.payment_id = payment_id
        order.save()
        for _id in ingred_ids:
            order.ingredients.add(
                Ingredient.objects.get(id=_id)
            )
        return redirect(payment_url)

    context = {
        'cake_form': cake_form,
        'costs': json.dumps(
            {x.pk: x.price for x in Ingredient.objects.all()}, default=str)
    }
    return render(request, 'index.html', context)


@login_required(login_url='/')
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        if name:
            current_user.first_name = name
        if email:
            current_user.email = email
        current_user.save()
    current_user = request.user
    orders = Order.objects.filter(user=current_user)\
                          .prefetch_related('ingredients')
    for order in orders:
        cake_parameters = {}
        for ingredient in order.ingredients.all():
            cake_parameters[ingredient.type.lower()] = ingredient.name
        order.cake_parameters = cake_parameters
    user_data = {
        'phonenumber': str(current_user.phonenumber),
        'email': current_user.email,
        'name': current_user.first_name
    }
    context = {
        'orders': orders,
        'user_data': user_data
    }
    return render(request, 'profile.html', context)


def check_payment(request):  # Временный костыль для локального тестирования
    if not request.user.is_authenticated:
        return redirect('/')
    pending_orders = Order.objects\
        .filter(user=request.user, paid=False)\
        .exclude(status='90')

    for order in pending_orders:
        payment_info = Payment.find_one(order.payment_id)
        if payment_info.paid:
            order.paid = True
            order.save()
        elif datetime.strptime(
            payment_info.expires_at,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ) < datetime.now():
            order.status = '90'
            order.save()

    return redirect('/profile')

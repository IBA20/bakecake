from datetime import datetime

from django.db.models import Sum
from yookassa import Payment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from bakecakeapp.models import Order, Ingredient
from users.models import CustomUser
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
                "return_url": "https://127.0.0.1"  # TODO put valid return url
            },
            "description": "Оплата: торт на заказ"
        }
    )
    return payment.id, payment.confirmation.confirmation_url


def index(request):
    cake_form = CreateCakeForm()

    if request.method == 'POST':
        print(request.POST)

        # TODO добавить валидацию формы
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
        print(ingred_ids)
        order.value = Ingredient.objects\
            .filter(id__in=ingred_ids)\
            .aggregate(Sum('price'))['price__sum']
        print('value: ', order.value)
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
    }
    return render(request, 'index.html', context)


@login_required()
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
    orders = Order.objects.filter(user=current_user).prefetch_related('ingredients')
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

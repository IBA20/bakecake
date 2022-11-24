from datetime import datetime

from django.shortcuts import render

from bakecakeapp.models import Order, Ingredient
from users.models import CustomUser
from .forms import CreateCakeForm


def index(request):
    cake_form = CreateCakeForm()

    if request.method == 'POST':
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
        order = Order.objects.create(
            user=user,
            writing=request.POST['WORDS'],
            comments=request.POST['COMMENTS'],
            delivery_address=request.POST['ADDRESS'],
            delivery_time=datetime.fromisoformat(
                f"{request.POST['DATE']}T{request.POST['TIME']}"),
            courier_info=request.POST['DELIVCOMMENTS'],
            value=999,
        )
        order.ingredients.add(
            Ingredient.objects.get(id=request.POST['topping']))
        berries = request.POST.get('berries')
        decor = request.POST.get('decor')
        levels = request.POST.get('levels')
        shape = request.POST.get('shape')

        if berries:
            order.ingredients.add(Ingredient.objects.get(id=berries))
        if decor:
            order.ingredients.add(Ingredient.objects.get(id=decor))
        if levels:
            order.ingredients.add(Ingredient.objects.get(id=levels))       
        if shape:
            order.ingredients.add(Ingredient.objects.get(id=shape))

    context = {
        'cake_form': cake_form,
    }
    return render(request, 'index.html', context)


def profile(request):
    context = {}
    return render(request, 'profile.html', context)

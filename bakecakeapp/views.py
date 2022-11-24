from datetime import datetime

from django.shortcuts import render

from bakecakeapp.models import Order, Ingredient
from users.models import CustomUser


def index(request):
    if request.method == 'POST':
        # TODO добавить валидацию формы
        if request.user.is_authenticated:
            user = request.user
        else:
            try:
                user = CustomUser.objects.get(phonenumber=request.POST['PHONE'])
            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create_user(
                    phonenumber=request.POST['PHONE'],
                    password='1234',
                    email=request.POST['EMAIL'],
                )
        order = Order.objects.create(
            user=user,
            levels=int(request.POST['LEVELS']),
            shape={'1': 'CR', '2': 'SQ', '3': 'RC'}[request.POST['FORM']],
            writing=request.POST['WORDS'],
            comments=request.POST['COMMENTS'],
            delivery_address=request.POST['ADDRESS'],
            delivery_time=datetime.fromisoformat(f"{request.POST['DATE']}T{request.POST['TIME']}"),
            courier_info=request.POST['DELIVCOMMENTS'],
            value=999,
        )
        order.ingredients.add(Ingredient.objects.get(id=request.POST['TOPPING']))
        berries = request.POST.get('BERRIES')
        decor = request.POST.get('DECOR')
        if berries:
            order.ingredients.add(Ingredient.objects.get(id=berries))
        if decor:
            order.ingredients.add(Ingredient.objects.get(id=decor))

    context = {}
    return render(request, 'index.html', context)


def profile(request):
    context = {}
    return render(request, 'profile.html', context)

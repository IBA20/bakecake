import phonenumbers

from django.shortcuts import render
from users.models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        phonenumber = request.POST['phone_number']
        try:
            parsed_phone_number = phonenumbers.parse(
                phonenumber,
                'RU'
            )
        except phonenumbers.NumberParseException:
            return JsonResponse({'phone_number_error': 'Некорректный номер телефона.'})
        if not phonenumbers.is_valid_number(parsed_phone_number):
            return JsonResponse({'phone_number_error': 'Некорректный номер телефона.'})
        normalized_phone_number = phonenumbers.format_number(
            parsed_phone_number,
            phonenumbers.PhoneNumberFormat.E164
        )
        if not CustomUser.objects.filter(phonenumber=normalized_phone_number).exists():
            user = CustomUser.objects.create_user(normalized_phone_number, '1234')
        return JsonResponse({'normalized_phone_number': 'Некорректный номер телефона.'})


def log_in(request):
    if request.method == "POST":
        phonenumber = request.POST['phone_number']
        password = request.POST['verification_code']
        parsed_phone_number = phonenumbers.parse(
            phonenumber,
            'RU'
        )
        normalized_phone_number = phonenumbers.format_number(
            parsed_phone_number,
            phonenumbers.PhoneNumberFormat.E164
        )
        user = authenticate(request, phonenumber=normalized_phone_number, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))

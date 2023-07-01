from django.shortcuts import render


def dashboard(request):
    context = {}
    return render(request, 'pos/user/dashboard.html', context)


def product(request):
    context = {}
    return render(request, 'pos/user/product.html', context)


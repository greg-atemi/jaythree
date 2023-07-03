import sys
import json
from pickle import FALSE
from flask import jsonify
from pos.models import Product
from datetime import date, datetime
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect


def dashboard(request):
    context = {}
    return render(request, 'pos/user/dashboard.html', context)


def products(request):
    product_list = Product.objects.all()
    context = {
        'products': product_list
    }
    return render(request, 'pos/user/products.html', context)


def save_product(request):
    product_list = Product.objects.all()
    context = {
        'products': product_list
    }

    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        unit_price = request.POST['unit_price']
        description = request.POST['description']

        newproduct = Product.objects.create(name=name, quantity=quantity, unit_price=unit_price,
                                            description=description)

        newproduct.save()

        return redirect('pos:products')
    return render(request, 'pos/user/new_product.html', context)


def update_product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    product_list = Product.objects.all()
    context = {
        'product': product,
        'products': product_list
    }

    if request.method == "POST":
        name = request.POST['name']
        quantity = product.quantity
        unit_price = request.POST['unit_price']
        description = request.POST['description']

        updated_product = Product(name=name, quantity=quantity, unit_price=unit_price,
                                  description=description)

        updated_product.save()

        return redirect('pos:products')
    return render(request, 'pos/user/update_product.html', context)


def delete_product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    product_list = Product.objects.all()
    context = {
        'product': product,
        'products': product_list
    }

    if request.method == "POST":
        product.delete()
        return redirect('pos:products')

    return render(request, 'pos/user/delete_product.html', context)

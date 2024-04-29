from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from pos.models import Product
from django.contrib import messages

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
        messages.success(request, "Product (" + name + ") Created Successfully. \n ")

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
        product_id = product.product_id
        name = request.POST['name']
        quantity = product.quantity
        unit_price = request.POST['unit_price']
        description = request.POST['description']

        updated_product = Product(product_id=product_id, name=name, quantity=quantity, unit_price=unit_price,
                                  description=description)

        updated_product.save()

        messages.success(request, "Product (" + name + ") Updated Successfully. \n ")

        return redirect('pos:products')
    return render(request, 'pos/user/update_product.html', context)


def delete_product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    name = product.name
    product_list = Product.objects.all()
    context = {
        'product': product,
        'products': product_list
    }

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product (" + name + ") Deleted Successfully. \n ")
        return redirect('pos:products')

    return render(request, 'pos/user/delete_product.html', context)


def stock(request):
    product_list = Product.objects.all()
    context = {
        'products': product_list
    }
    return render(request, 'pos/user/stock.html', context)


def add_stock(request, product_id):
    product_list = Product.objects.all()
    product = Product.objects.get(product_id=product_id)
    context = {
        'products': product_list,
        'product': product
    }

    if request.method == "POST":
        product_id = product.product_id
        name = product.name
        quantity = product.quantity + int(request.POST['quantity'])
        unit_price = product.unit_price
        description = product.description

        updated_product = Product(product_id=product_id, name=name, quantity=quantity, unit_price=unit_price,
                                  description=description)

        updated_product.save()

        messages.success(request, "Stock of (" + name + " " + "Amount: " + request.POST[
            'quantity'] + ") Added Successfully. \n ")
        return redirect('pos:stock')
    return render(request, 'pos/user/add_stock.html', context)


def remove_stock(request, product_id):
    product_list = Product.objects.all()
    product = Product.objects.get(product_id=product_id)
    context = {
        'products': product_list,
        'product': product
    }

    if request.method == "POST":
        product_id = product.product_id
        name = product.name
        quantity = product.quantity - int(request.POST['quantity'])
        unit_price = product.unit_price
        description = product.description

        if quantity < 0:
            messages.error(request, "Stock (" + name + ") is less than the reducing amount")
            return redirect('pos:stock')

        updated_product = Product(product_id=product_id, name=name, quantity=quantity, unit_price=unit_price,
                                  description=description)

        updated_product.save()

        messages.success(request, "Stock of (" + name + " " + "Amount: " + request.POST[
            'quantity'] + ") Reduced Successfully. \n ")
        return redirect('pos:stock')
    return render(request, 'pos/user/remove_stock.html', context)

def pos(request):
    context = {}
    return render(request, 'pos/user/pos.html', context)
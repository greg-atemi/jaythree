from django.shortcuts import redirect, render
from django.http import HttpResponse
from pos.models import Product, Sale, SaleItems
from django.contrib import messages
from django.utils import timezone

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

def create_report(request):
    context = {}
    return render(request, 'pos/user/remove_stock.html', context)

def pos(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Retrieve product details
        product = Product.objects.get(product_id=product_id)

        # Create or update sale items in session
        sale_items = request.session.get('sale_items', [])

        # Check if the product is already in the cart
        item_exists = False
        for item in sale_items:
            if item['product_id'] == int(product_id):
                item['quantity'] += quantity
                item['total'] = item['quantity'] * item['price']
                item_exists = True
                break
        
        if not item_exists:
            sale_items.append({
                'product_id': product_id,
                'product_name': product.name,
                'quantity': quantity,
                'price': product.unit_price,
                'total': quantity * product.unit_price
            })

        request.session['sale_items'] = sale_items

        # Redirect to the same page to avoid resubmitting the form on refresh
        return redirect('pos:pos')

    # Calculate total sale amount
    sale_items = request.session.get('sale_items', [])
    total_sale_amount = sum(item['total'] for item in sale_items)

    # Get all products to display in the dropdown
    products = Product.objects.all()

    context = {
        'products': products,
        'sale_items': sale_items,
        'total_sale_amount': total_sale_amount
    }

    return render(request, 'pos/user/pos.html', context)

def remove_item(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        # Get the current sale items from the session
        sale_items = request.session.get('sale_items', [])
        
        # Filter out the item that needs to be removed
        sale_items = [item for item in sale_items if item['product_id'] != product_id]

        # Update the session with the remaining items
        request.session['sale_items'] = sale_items

        # Redirect back to the POS page to apply the PRG pattern
        return redirect('pos:pos')

    return redirect('pos:pos')

def checkout(request):
    if 'sale_items' in request.session and request.session['sale_items']:
        sale_items = request.session['sale_items']
        total_sale_amount = sum(item['total'] for item in sale_items)
        tendered_amount = request.POST['amountPaid']
        balance = request.POST['balance']

        # Create a new sale
        sale = Sale.objects.create(
            code=f"SALE-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            date=timezone.now(),
            time=timezone.now(),
            total=total_sale_amount,
            tendered_amount=tendered_amount,
            balance=balance
        )

        # Save each sale item to the database
        for item in sale_items:
            product = Product.objects.get(pk=item['product_id'])
            SaleItems.objects.create(
                sale_id=sale,
                product_id=product,
                quantity=item['quantity'],
                price=item['price'],
                total=item['total']
            )

        # Clear the session
        del request.session['sale_items']
        # return redirect('sale_success')  # Redirect to a success page or another view
        print("Sale successful!!")

    # return HttpResponse("No items in sale", status=400)
    # return redirect('pos:checkout')
    return render(request, 'pos/user/checkout.html')

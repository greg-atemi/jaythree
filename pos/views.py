from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from pos.models import Product, Sale, SaleItems
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone

@login_required
def dashboard(request):
    context = {}
    return render(request, 'pos/user/dashboard.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('dashboard')

        else:
            messages.error(request, "Username or Password is incorrect")

    return render(request, 'pos/auth/login.html')

@login_required
def log_out(request):
    logout(request)
    return render(request, 'pos/auth/logout.html')

@login_required
def account(request):
    uname = request.user.username
    fname = request.user.first_name
    lname = request.user.last_name
    email = request.user.email
    context = {
        'uname': uname,
        'fname': fname,
        'lname': lname,
        'email': email
    }
    print("Username: " + uname)
    print("First name: " + fname)
    print("Last name: " + lname)
    print("Email: " + email)
    return render(request, 'pos/user/account.html', context)

def signup(request):
    if request.method == "POST":
        # username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = fname + lname
        username = username.lower()
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!!")
            return redirect('pos:signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists!!")
            return redirect('pos:signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('pos:signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True

        myuser.save()

        messages.success(request, "Your Account has been created successfully. \n ")

        return redirect('pos:login')

    return render(request, 'pos/auth/signup.html')

@login_required
def products(request, page):
    product_list = Product.objects.all().order_by("product_id")
    paginator = Paginator(product_list, per_page=10)
    page_object = paginator.get_page(page)
    context = {"page_object": page_object}
    return render(request, 'pos/user/products.html', context)

@login_required
def reports(request):
    result_list = None

    if request.method == 'POST':
        start_date_time = request.POST.get('start_date_time')
        end_date_time = request.POST.get('end_date_time')

        if start_date_time and end_date_time:
            # Convert strings to datetime objects
            start_date_time = timezone.datetime.fromisoformat(start_date_time)
            end_date_time = timezone.datetime.fromisoformat(end_date_time)

            # Query the Sale model using date and time ranges
            result_list = Sale.objects.filter(
                date__range=[start_date_time.date(), end_date_time.date()],
                time__range=[start_date_time.time(), end_date_time.time()]
            )
    return render(request, 'pos/user/reports.html', {
        'result_list': result_list,
    })

@login_required
def sales(request, page=1):
    sale_list = Sale.objects.all().order_by("-sale_id")
    paginator = Paginator(sale_list, per_page=12)
    page_object = paginator.get_page(page)
    context = {"page_object": page_object}
    return render(request, "pos/user/sales.html", context)

@login_required
def save_product(request):
    product_list = Product.objects.all()
    page_number = 1
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

        return redirect('pos:products',page=page_number)
    return render(request, 'pos/user/new_product.html', context)

@login_required
def update_product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    page_number = 1
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

        return redirect('pos:products', page=page_number)
    return render(request, 'pos/user/update_product.html', context)

@login_required
def receipt(request, sale_id):
    sale = Sale.objects.get(sale_id=sale_id)
    item_list = SaleItems.objects.filter(sale_id=sale)
    context = {
        'sale': sale,
        'item_list': item_list
    }

    return render(request, 'pos/user/receipt.html', context)

@login_required
def sale_receipt(request, sale_id):
    sale = Sale.objects.get(sale_id=sale_id)
    item_list = SaleItems.objects.filter(sale_id=sale)
    context = {
        'sale': sale,
        'item_list': item_list
    }

    return render(request, 'pos/user/sale_receipt.html', context)

@login_required
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
        return redirect('pos:products', page=1)

    return render(request, 'pos/user/delete_product.html', context)

@login_required
def stock(request, page):
    product_list = Product.objects.all().order_by("-product_id")
    paginator = Paginator(product_list, per_page=12)
    page_object = paginator.get_page(page)
    context = {"page_object": page_object}
    return render(request, 'pos/user/stock.html', context)

@login_required
def add_stock(request, product_id):
    product_list = Product.objects.all()
    page_number = 1
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
        return redirect('pos:stock', page=page_number)
    return render(request, 'pos/user/add_stock.html', context)

@login_required
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
        return redirect('pos:stock', page=1)
    return render(request, 'pos/user/remove_stock.html', context)

@login_required
def create_report(request):
    context = {}
    return render(request, 'pos/user/remove_stock.html', context)

@login_required
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

@login_required
def pos(request):
    if request.method == 'POST':
        # Handle adding sale items to session
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if product_id and quantity:
            # Retrieve product details
            product = Product.objects.get(product_id=product_id)

            if quantity <= product.quantity:
                # Create or update sale items in session
                sale_items = request.session.get('sale_items', [])

                # Check if the product is already in the cart
                item_exists = False
                for item in sale_items:
                    print(f'Checking item in session: {item}')
                    if item['product_id'] == product_id:
                        print(f'Found duplicate item with product ID: {product_id}')
                        total_quantity = item['quantity'] + quantity

                        if total_quantity <= product.quantity:
                            item['quantity'] += quantity
                            item['total'] = item['quantity'] * item['price']
                            item_exists = True
                            break
                        else:
                            item_exists = True
                            print("Not enough stock!!")
                            break
                
                if not item_exists:
                    print(f'Adding new item to session: Product ID: {product_id}, Name: {product.name}, Quantity: {quantity}')
                    sale_items.append({
                        'product_id': product_id,
                        'product_name': product.name,
                        'quantity': quantity,
                        'price': product.unit_price,
                        'total': quantity * product.unit_price
                    })

                print(f'Sale items in session before update: {sale_items}')
                request.session['sale_items'] = sale_items
                print(f'Sale items in session after update: {sale_items}')

                return redirect('pos:pos')

            else:
                #messages.error(HttpRequest,"The product" + product.name + "is not enough in stock!!")
                print(f"The product {product.name} is out of stock")
                print(f"The stock left is {product.quantity}")

                return redirect('pos:pos')

        # Handle checkout process
        if 'checkout' in request.POST:
            if 'sale_items' in request.session and request.session['sale_items']:
                sale_items = request.session['sale_items']
                total_sale_amount = sum(item['total'] for item in sale_items)
                tendered_amount = float(request.POST['amountPaid'])
                balance = float(request.POST['balance'])

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

                    product.quantity -= item['quantity']
                    product.save()

                # Clear the session
                print("Sale successful")
                del request.session['sale_items']

                # Optionally, redirect to a sale success page
                # return redirect('pos:pos')
                return redirect('pos:receipt', sale_id=sale.sale_id)

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

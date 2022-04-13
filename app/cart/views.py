from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from django.contrib import messages
from store.models import Product, Variation


@login_required(login_url='login')
def _cart_id(request):
    try:
        cart = Cart.objects.get(user=request.user)  # Get cart using the _cart_id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    cart.save()
    return cart

def cart(request, total=0, quantity=0, cart_items=None):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context=context)


def add_cart(request, product_id):
    curent_user = request.user
    product = Product.objects.get(id=product_id)  # get by id
    if curent_user.is_authenticated:
        product_variations = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variations.append(variation)
                except ObjectDoesNotExist:
                    pass
        is_exists_cart_item = CartItem.objects.filter(product=product, user=curent_user).exists()
        if is_exists_cart_item:
            cart_items = CartItem.objects.filter(product=product, user=curent_user)
            exisis_variation_list = [list(item.variations.all()) for item in cart_items]
            ids = [item.id for item in cart_items]

            if product_variations in exisis_variation_list:
                idex = exisis_variation_list.index(product_variations)
                cart_items = CartItem.objects.get(id=ids[idex])
                cart_items.quantity += 1
            else:
                cart_items = CartItem.objects.create(product=product, user=curent_user, quantity=1)
        else:
            cart_items = CartItem.objects.create(product=product, user=curent_user, quantity=1)

        if len(product_variations) > 0:
            cart_items.variations.clear()
            for item in product_variations:
                cart_items.variations.add(item)
        cart_items.save()
        return redirect('cart')
    else:
        product_variations = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value)
                    product_variations.append(variation)
                except ObjectDoesNotExist:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request=request))
        cart.save()

        is_exists_cart_item = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_exists_cart_item:
            cart_items = CartItem.objects.filter(product=product, cart=cart)
            existsing_variation_list = [list(item.variations.all()) for item in cart_items]
            ids = [item.id for item in cart_items]
            if product_variations in existsing_variation_list:
                idex = existsing_variation_list.index(product_variations)
                cart_items = CartItem.objects.get(id=ids[idex])
                cart_items.quantity += 1
            else:
                cart_items = CartItem.objects.create(product=product, cart=cart, quantity=1)
        else:
            cart_items = CartItem.objects.create(product=product, cart=cart, quantity=1)

        if len(product_variations) > 0:
            cart_items.variations.clear()
            for item in product_variations:
                cart_items.variations.add(item)
        cart_items.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(id=cart_item_id, product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception:
        messages.info(request, str(Exception))
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                product=product,
                cart=cart
            )
        cart_item.delete()
    except Exception:
        messages.info(request, str(Exception))
        pass
    return redirect('cart')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = total * 0.2
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax if 'tax' in locals() else '',
        'grand_total': grand_total if 'grand_total' in locals() else ''
    }
    return render(request, 'store/checkout.html', context=context)
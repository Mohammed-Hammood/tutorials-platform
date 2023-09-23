from django.shortcuts import render, redirect
from .models import Product, ProductAccess, Lesson


def home_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    products = Product.objects.filter(owner=request.user)
    context = {
        'products':products, 
    }
    return render(request, 'products/products-list.html', context)


def product_details(request, pk:int):
    try:
        product = Product.objects.get(id=int(pk))
    except Product.DoesNotExist:
        return render(request, 'not-found.html')
    user = request.user
    has_access = ProductAccess.objects.filter(user=user, product=product).first()

    if product.owner == user or has_access is not None:
        context = {
            'product': product
        }
        return render(request, 'products/product-details.html', context)
    return render(request, 'not-authorized.html')


def accessed_products(request):
    queryset = ProductAccess.objects.filter(user=request.user)
    products = []
    for item in queryset:
        products.append(item.product)
    context = {
            'products': products
        }
    return render(request, 'products/products-list.html', context)



def lesson_details(request, product_id:int, lesson_id:int):
    try:
        lesson = Lesson.objects.get(id=int(lesson_id))
        product = Product.objects.get(id=int(product_id))
    except Lesson.DoesNotExist or Product.DoesNotExist:
        return render(request, 'not-found.html')
    user = request.user
    has_access = ProductAccess.objects.filter(user=user, product=product).first()

    if product.owner == user or has_access is not None:
        context = {
            'lesson': lesson,
            'product': product,
        }
        return render(request, 'products/lesson-details.html', context)
    return render(request, 'not-authorized.html')


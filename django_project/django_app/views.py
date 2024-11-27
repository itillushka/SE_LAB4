import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')
            available = data.get('available')
            
            if name is None or price is None or available is None:
                return HttpResponseBadRequest("Missing field.")
            
            if Decimal(str(price)) < 0:
                return HttpResponseBadRequest("Price cannot be negative.")
            
            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            }, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON.")
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found.")
    
    if request.method == 'GET':
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        })
    else:
        return HttpResponseNotAllowed(['GET'])


from django.shortcuts import render
from marketplace.context_processors import get_cart_counter
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from .models import Cart
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count' : vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor':vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if fooditem exists:
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    # check if this food item is already there in cart or not:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status':'Success', 'message':'Increased the cart quantity', 'cart_counter':get_cart_counter(request), 'qty':chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message':'Added the food to cart' , 'cart_counter':get_cart_counter(request), 'qty':chkCart.quantity})
            except:
                return JsonResponse({'status':'Failed', 'message':' This food item does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})
    else:
        return JsonResponse({'status':'Failed', 'message':'user is not logged in'})

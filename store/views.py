from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json, datetime
from .utils import cartData, guestOrder
from django.views.generic import DetailView

# Create your views here.
def home(request):
    data = cartData(request)

    cartItems = data["cartItems"]

    products = Product.objects.all()
    products = products[:6]
    context = {"cartItems": cartItems, "products": products}
    return render(request, "store/home.html", context)


def cart(request):
    data = cartData(request)

    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)

    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


def store(request):
    data = cartData(request)

    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(request, "store/store.html", context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/detail_item.html"

    def get_context_data(self, *args, **kwargs):
        data = cartData(self.request)
        cartItems = data["cartItems"]
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        try:
            context["reviews"] = [Review.objects.get(product=self.object.id)]
        except:
            context["reviews"] = []

        context["cartItems"] = cartItems
        return context


def shipping(request):
    data = cartData(request)

    cartItems = data["cartItems"]

    context = {"cartItems": cartItems}
    return render(request, "store/shipping.html", context)


def tracking(request):
    data = cartData(request)

    cartItems = data["cartItems"]

    context = {"cartItems": cartItems}
    return render(request, "store/tracking.html", context)


def about(request):
    data = cartData(request)

    cartItems = data["cartItems"]

    context = {"cartItems": cartItems}
    return render(request, "store/about.html", context)


def termsOfService(request):
    data = cartData(request)

    cartItems = data["cartItems"]

    context = {"cartItems": cartItems}
    return render(request, "store/terms_of_service.html", context)


def privacyPolicy(request):
    data = cartData(request)

    cartItems = data["cartItems"]

    context = {"cartItems": cartItems}
    return render(request, "store/privacy_policy.html", context)


def pressAndAffiliates(request):
    data = cartData(request)

    cartItems = data["cartItems"]

    context = {"cartItems": cartItems}
    return render(request, "store/press_and_affiliates.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    print("Action:", action)
    print("Prodcut:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        print(data)
    else:
        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    return JsonResponse("Payment submitted...", safe=False)

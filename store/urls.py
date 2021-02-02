from django.urls import path
from . import views
from .views import ProductDetailView

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("item/<int:pk>", ProductDetailView.as_view(), name="detail_item"),
    path("shipping/", views.shipping, name="shipping"),
    path("order-tracking/", views.tracking, name="order-tracking"),
    path("about/", views.about, name="about"),
    path(
        "press-and-affiliates/", views.pressAndAffiliates, name="press_and_affiliates"
    ),
    path("terms-of-service/", views.termsOfService, name="terms_of_service"),
    path("privacy-policy/", views.privacyPolicy, name="privacy_policy"),
]

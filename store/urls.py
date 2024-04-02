from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views

app_name = "store"


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<slug:slug>/", views.remove_from_cart, name="remove_from_cart"),
    path(
        "products/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("category/<slug:slug>/", views.CategoryView.as_view(), name="category"),
    path("cart/", views.CartView.as_view(), name="cart_view"),
    path("checkout/", views.OrderCheckoutView.as_view(), name="checkout_view"),
    path("viewordertest/", views.view_orders, name="orders_view"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView, View

from store.forms import FiltersForm, OrderForm
from store.models import Product, Cart, CartProduct, Category, Order
from store import forms
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.


class IndexView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["objects"] = Product.objects.select_related("category").filter(
            discount_price__isnull=False
        )
        return context


class ProductDetailView(DetailView):
    model = Product


class ProductListView(ListView):
    model = Product
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        max_prod_price = Product.objects.order_by("-price").first().price

        query = self.request.GET.copy()
        query.pop("page", None)
        query = query.urlencode()
        print(query)
        filters_form = forms.FiltersForm(self.request.GET)
        if filters_form.is_valid():
            filters_form = forms.FiltersForm(initial=filters_form.cleaned_data)
        if not self.request.GET.get("max_price"):
            filters_form = forms.FiltersForm(initial={"max_price": max_prod_price})

        search_form = forms.SearchForm(self.request.GET)
        if search_form.is_valid():
            search_form = forms.SearchForm(initial=search_form.cleaned_data)

        context["search_form"] = search_form
        context["filters_form"] = filters_form
        context["query"] = query
        return context

    def get_queryset(self):
        queryset = (
            super(ProductListView, self).get_queryset().select_related("category")
        )

        if self.request.GET.get("search"):
            queryset = queryset.filter(name__icontains=self.request.GET.get("search"))

        form = FiltersForm(self.request.GET)
        if form.is_valid() and "min_price" in self.request.GET:
            if form.cleaned_data["categories"]:
                queryset = queryset.filter(
                    category__in=self.request.GET.getlist("categories")
                )

            queryset = queryset.filter(
                price__gte=self.request.GET["min_price"],
                price__lte=self.request.GET["max_price"],
            )
        return queryset


class CategoryView(ListView):
    model = Product
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context["category"] = Category.objects.get(slug__exact=self.kwargs.get("slug"))
        return context

    def get_queryset(self):
        queryset = super(CategoryView, self).get_queryset().select_related("category")
        return queryset.filter(category__slug=self.kwargs.get("slug"))


def get_cart(request):
    if not request.session or not request.session.session_key:
        request.session.save()
    if request.session.session_key:
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key, active=True
        )
    else:
        cart, created = Cart.objects.get_or_create(user=request.user, active=True)
    return cart


def get_or_create_cart_product(request, slug):
    cart = get_cart(request)
    product = get_object_or_404(Product, slug=slug)
    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart, product=product
    )
    return cart_product, created


def add_to_cart(request, slug):
    cart_product, created = get_or_create_cart_product(request, slug)
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    return redirect("store:cart_view")


def remove_from_cart(request, slug):
    cart_product, created = get_or_create_cart_product(request, slug)
    if not created and cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
    elif not created:
        cart_product.delete()

    return redirect("store:cart_view")


class CartView(TemplateView):
    template_name = "store/cart_view.html"

    def get_context_data(self, **kwargs):
        cart = get_cart(self.request)
        cart_products = cart.cartproduct_set.select_related("product__category").all()
        context = {
            "cart": cart,
            "cart_products": cart_products,
            "total": cart.get_total(),
        }
        return context


class OrderCheckoutView(TemplateView):
    template_name = "store/order_checkout.html"

    def get_context_data(self, **kwargs):
        context = super(OrderCheckoutView, self).get_context_data(**kwargs)
        order_form = forms.OrderForm()
        context["order_form"] = order_form
        return context

    def post(self, request, *args, **kwargs):
        order_form = forms.OrderForm(request.POST)
        if order_form.is_valid():
            cart = get_cart(self.request)

            order = Order.objects.create(
                cart=cart,
                address=order_form.cleaned_data["address"],
                phone=order_form.cleaned_data["phone"],
            )
            cart.active = False
            cart.save()
            return redirect("store:cart_view")
        else:
            context = {"order_form": order_form}
            return render(request, self.template_name, context)


@permission_required("store.add_order")
def view_orders(request):
    orders = Order.objects.select_related("address", "cart").prefetch_related(
        "cart__cartproduct_set", "cart__cartproduct_set__product"
    )
    context = {
        "orders": orders,
    }
    return render(request, "store/view_orders.html", context=context)

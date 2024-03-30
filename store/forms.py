from django import forms
from django.forms import CheckboxSelectMultiple

from .models import CartProduct, Address, Category, Product


class FiltersForm(forms.Form):
    product_with_max_price = Product.objects.order_by('-price').first().price
    min_price = forms.FloatField(widget=forms.NumberInput(
        attrs={'value': 0}
    ), required=False, min_value=0)
    max_price = forms.FloatField(widget=forms.NumberInput(), required=False)

    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                widget=CheckboxSelectMultiple,
                                                required=False)


class SearchForm(forms.Form):
    search = forms.CharField(label='', max_length=50, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Type product name here',
               'class': 'form-control mb-0 mt-0'}
    ))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "first_name",
            "last_name",
            "street",
            "city",
            "zip_code",
        )

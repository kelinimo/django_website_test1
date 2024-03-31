from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Address, Category, Order


class FiltersForm(forms.Form):
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


class OrderForm(forms.ModelForm):
    address = forms.ModelChoiceField(queryset=Address.objects.all(), label='Choose shop address.', required=False)

    class Meta:
        model = Order
        fields = ('address', 'phone')


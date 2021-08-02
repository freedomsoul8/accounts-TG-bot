from django import forms

from .models import Category, order



class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = (
            'external_id',
            'name',
            'price',
            'sheet'
        )
        widgets = {
            'name': forms.TextInput,
            'sheet': forms.TextInput
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = (
           'order_id',
           'order_name',
           'order_cost',
           'order_date'

        )
        widgets = {
            'order_name': forms.TextInput
        }
from django.contrib import admin



from .forms import CategoryForm, OrderForm
from .models import Category, order





@admin.register(Category)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'price','sheet')
    form = CategoryForm

@admin.register(order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_name', 'order_cost', 'order_date')
    form = OrderForm

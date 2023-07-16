from django.contrib import admin
from django import forms
from .models import Product, Color, Size


from django import forms
from .models import Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'sizes': forms.CheckboxSelectMultiple(),
            'colors': forms.CheckboxSelectMultiple(),
        }


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('product_name', 'category', 'price',
                    'is_available', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(Color)

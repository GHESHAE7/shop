from django.contrib import admin
from .models import Category, Brand, Product, ProductVariant, ManyImages

# Register your models here.


class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 1
    
       
class ManyImageInline(admin.StackedInline):
    model = ManyImages
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('created_at', 'updated_at', 'is_active',)
    list_editable = ('is_active',)
    readonly_fields = ('updated_at', 'created_at',)
    date_hierarchy = 'created_at'
    search_fields = ('name', 'url',)
    
    
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('created_at', 'updated_at', 'is_active',)
    list_editable = ('is_active',)
    readonly_fields = ('updated_at', 'created_at')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'url',)
    
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'gender', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('category', 'brand', 'gender', 'is_active', 'updated_at', 'created_at',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at',)
    date_hierarchy = 'created_at'
    search_fields = ('name', 'slug', 'category', 'brand',)
    inlines = (ProductVariantInline, )
    
    
    
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('product__name', 'product__price', 'stock', 'discount', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('stock', 'discount', 'is_active', 'created_at',)
    list_editable = ('is_active', 'stock', 'discount', 'is_active')
    readonly_fields = ('created_at', 'updated_at',)
    search_fields = ('product__name',)
    inlines = (ManyImageInline, )
    
    
    
@admin.register(ManyImages)
class ManyImageAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('product_variant' ,'is_active', 'updated_at', 'created_at',)
    list_filter = ('is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at',)
    # search_fields = ('product_variant',)
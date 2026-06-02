from django.contrib import sitemaps
from django.urls import reverse
from product_module.models import Product, Category, Brand


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return [
            "home_module:home_page",
            "notice_module:notice_page",
            "product_module:products_page",
            "product_module:products_discount_page",
        ]

    def location(self, item):
        return reverse(item)


class StaticViewSitemap2(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return [
            "about_module:about_page",
            "about_module:privacy_policy_page",
            "contact_module:contact_page",
            "support_module:support_page",
        ]

    def location(self, item):
        return reverse(item)


class ProductsSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("product_module:product_detail_page", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class CategoriesSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, obj):
        return reverse(
            "product_module:products_by_category_page", kwargs={"category_url": obj.url}
        )

    def lastmod(self, obj):
        return obj.updated_at


class BrandsSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Brand.objects.filter(is_active=True)

    def location(self, obj):
        return reverse(
            "product_module:products_by_brand_page", kwargs={"brand_url": obj.url}
        )

    def lastmod(self, obj):
        return obj.updated_at

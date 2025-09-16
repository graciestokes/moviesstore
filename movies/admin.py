from django.contrib import admin

from .models import Movie, Review
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_display = ['name', 'price', 'rating', 'amount_left', 'stock_status']
    list_filter = ['amount_left']
    
    # Add amount_left to the fields
    fields = ['name', 'description', 'price', 'image', 'rating', 'amount_left', 'watch_list']
    
    # Make watch_list field use a more user-friendly widget
    filter_horizontal = ['watch_list']
    
    def stock_status(self, obj):
        """Display stock status in admin list"""
        if obj.amount_left > 10:
            return "✅ In Stock"
        elif obj.amount_left > 0:
            return f"⚠️ Low Stock ({obj.amount_left})"
        else:
            return "❌ Out of Stock"
    
    stock_status.short_description = "Stock Status"

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)

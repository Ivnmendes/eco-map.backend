from django.contrib import admin
from .models import OperatingHour, CollectionType, CollectionPoint, PointReview

# Register CollectionType


class CollectionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(CollectionType, CollectionTypeAdmin)

# Register CollectionPoint
class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'is_active', 'created_at', 'status')
    search_fields = ('name',)
    list_filter = ('is_active',)

admin.site.register(CollectionPoint, CollectionPointAdmin)

# Register PointReview
class PointReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'created_at')
    search_fields = ('user__username', 'point__name')

admin.site.register(PointReview, PointReviewAdmin)

# Register OperatingHour
class OperatingHourAdmin(admin.ModelAdmin):
    list_display = ('collection_point', 'day_of_week', 'opening_time', 'closing_time', 'active')
    search_fields = ('collection_point__name',)
    list_filter = ('day_of_week', 'active')
admin.site.register(OperatingHour, OperatingHourAdmin)
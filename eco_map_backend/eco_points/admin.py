from django.contrib import admin
from .models import CollectionType, CollectionPoint, PointReview, PointRequest

# Register CollectionType
class CollectionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(CollectionType, CollectionTypeAdmin)

# Register CollectionPoint
class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'is_active', 'created_by', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_by')

admin.site.register(CollectionPoint, CollectionPointAdmin)

# Register PointReview
class PointReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'created_at')
    search_fields = ('user__username', 'point__name')

admin.site.register(PointReview, PointReviewAdmin)

# Register PointRequest
class PointRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'approved_status', 'user', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('approved',)

    def approved_status(self, obj):
        return 'Sim' if obj.approved else 'Não'
    approved_status.short_description = 'Aprovado'

admin.site.register(PointRequest, PointRequestAdmin)

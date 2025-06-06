from django.db import models
from accounts.models import User

class CollectionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=500)

    def __str__(self):
        return self.name

class CollectionPoint(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    types = models.ManyToManyField(CollectionType, related_name='points')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='collection_points', null=True, blank=True)

    def __str__(self):
        return self.name

class PointImage(models.Model):
    collection_point = models.ForeignKey(CollectionPoint, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='point_images/')

    def __str__(self):
        return f"Image for {self.collection_point.name}"

class PointReview(models.Model):
    point = models.ForeignKey(CollectionPoint, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.point}"
    
class OperatingHour(models.Model):
    collection_point = models.ForeignKey(CollectionPoint, on_delete=models.CASCADE, related_name='operating_hours')
    day_of_week = models.SmallIntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    active = models.BooleanField(default=True)

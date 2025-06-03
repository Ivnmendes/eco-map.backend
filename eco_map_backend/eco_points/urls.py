from django.urls import path
from .views import CollectionPointDetail, CollectionPointList, CollectionTypeDetail, CollectionTypeList, PointRequestDetail, PointRequestList, PointReviewDetail, PointReviewList, PointReviewFilteredList, PointImageUploadView

urlpatterns = [
    path('collection-point/', CollectionPointList.as_view(), name='collection-point-list'),
    path('collection-point/<int:pk>/', CollectionPointDetail.as_view(), name='collection-point-detail')
]

urlpatterns += [
    path('collection-type/', CollectionTypeList.as_view(), name='collection-type-list'),
    path('collection-type/<int:pk>/', CollectionTypeDetail.as_view(), name='collection-type-detail')
]

urlpatterns += [
    path('point-request/', PointRequestList.as_view(), name='point-request-list'),
    path('point-request/<int:pk>/', PointRequestDetail.as_view(), name='point-request-detail')
]

urlpatterns += [
    path('point-review/', PointReviewList.as_view(), name='point-review-list'),
    path('point-review/<int:pk>/', PointReviewDetail.as_view(), name='point-review-detail'),
    path('point-review/filter/', PointReviewFilteredList.as_view(), name='point-review-filtered-list'),
]

urlpatterns += [
    path('point-image/upload/', PointImageUploadView.as_view(), name='point-image-upload'),
]
from django.urls import path
from .views import CollectionPointDetail, CollectionPointList, CollectionTypeDetail, CollectionTypeList, PointReviewDetail, PointReviewList, PointReviewFilteredList, PointImageUploadView, UserPendingCollectionPointsList, ActiveCollectionPointsList, InactiveCollectionPointsList

urlpatterns = [
    path('collection-points/', CollectionPointList.as_view(), name='collection-points-list'),
    path('collection-points/<int:pk>/', CollectionPointDetail.as_view(), name='collection-points-detail'),
    path('collection-points/my-pending/', UserPendingCollectionPointsList.as_view(), name='user-pending-collection-points'),
    path('collection-points/active/', ActiveCollectionPointsList.as_view(), name='active-collection-points'),
    path('collection-points/inactive/', InactiveCollectionPointsList.as_view(), name='inactive-collection-points'),
]

urlpatterns += [
    path('collection-type/', CollectionTypeList.as_view(), name='collection-type-list'),
    path('collection-type/<int:pk>/', CollectionTypeDetail.as_view(), name='collection-type-detail'),
    path('collection-point/<int:pk>/upload_image/', PointImageUploadView.as_view(), name='point-image-upload'),
]

urlpatterns += [
    path('point-review/', PointReviewList.as_view(), name='point-review-list'),
    path('point-review/<int:pk>/', PointReviewDetail.as_view(), name='point-review-detail'),
    path('point-review/filter/', PointReviewFilteredList.as_view(), name='point-review-filtered-list'),
]
from django.urls import path
from .views import (
    FarmerListCreateView, FarmerDetailView,
    CollectionCenterListCreateView, CollectionCenterDetailView,
    ProcessingFacilityListCreateView, ProcessingFacilityDetailView,
    PackagingCenterListCreateView, PackagingCenterDetailView,
    BatchListCreateView, BatchDetailView, GenerateBatchNumberView, BatchDetailsSearchAPIView
)

urlpatterns = [ 
    path('farmers/', FarmerListCreateView.as_view(), name='farmer-list-create'),
    path('farmers/<str:farmer_id>/', FarmerDetailView.as_view(), name='farmer-detail'),
 
    path('collection-centers/', CollectionCenterListCreateView.as_view(), name='collection-center-list-create'),
    path('collection-centers/<str:center_id>/', CollectionCenterDetailView.as_view(), name='collection-center-detail'),
   
    path('processing-facilities/', ProcessingFacilityListCreateView.as_view(), name='processing-facility-list-create'),
    path('processing-facilities/<str:facility_id>/', ProcessingFacilityDetailView.as_view(), name='processing-facility-detail'),
    
    path('packaging-centers/', PackagingCenterListCreateView.as_view(), name='packaging-center-list-create'),
    path('packaging-centers/<str:center_id>/', PackagingCenterDetailView.as_view(), name='packaging-center-detail'),
 
    path('batches/', BatchListCreateView.as_view(), name='batch-list-create'),
    path('batches/<str:batch_number>/', BatchDetailView.as_view(), name='batch-detail'),
    path('generate-batch-number/', GenerateBatchNumberView.as_view(), name='generate-batch-number'),
    path('batches/search/batch_number', BatchDetailsSearchAPIView.as_view(), name='batch-search'),
]
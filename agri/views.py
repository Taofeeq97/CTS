from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView 
from django_filters.rest_framework import DjangoFilterBackend
from .models import Farmer, CollectionCenter, ProcessingFacility, PackagingCenter, Batch
from .serializers import (
    FarmerSerializer, CollectionCenterSerializer, ProcessingFacilitySerializer,
    PackagingCenterSerializer, BatchSerializer, BatchNumberSearchSerializer
)


class FarmerListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of farmers or create new farmer
    """
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'certification', 'status']
    search_fields = ['name', 'farmer_id']
    ordering_fields = ['name', 'age', 'farm_size', 'years_in_farming']


class FarmerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete farmer
    """
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer 
    lookup_field = 'farmer_id'


class CollectionCenterListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of collection centers or create new center
    """
    queryset = CollectionCenter.objects.all()
    serializer_class = CollectionCenterSerializer 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['drying_method', 'status']
    search_fields = ['name', 'center_id', 'location']
    ordering_fields = ['name', 'capacity']


class CollectionCenterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete collection center
    """
    queryset = CollectionCenter.objects.all()
    serializer_class = CollectionCenterSerializer 
    lookup_field = 'center_id'


class ProcessingFacilityListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of processing facilities or create new facility
    """
    queryset = ProcessingFacility.objects.all()
    serializer_class = ProcessingFacilitySerializer 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'facility_id', 'location']
    ordering_fields = ['name', 'capacity']


class ProcessingFacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete processing facility
    """
    queryset = ProcessingFacility.objects.all()
    serializer_class = ProcessingFacilitySerializer 
    lookup_field = 'facility_id'


class PackagingCenterListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of packaging centers or create new center
    """
    queryset = PackagingCenter.objects.all()
    serializer_class = PackagingCenterSerializer 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'center_id', 'location']
    ordering_fields = ['name', 'capacity']


class PackagingCenterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete packaging center
    """
    queryset = PackagingCenter.objects.all()
    serializer_class = PackagingCenterSerializer 
    lookup_field = 'center_id'


class BatchListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of batches or create new batch
    """
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['collection_center', 'processing_facility', 'packaging_center', 'year']
    search_fields = ['batch_number']
    ordering_fields = ['packaging_date', 'expiry_date', 'created_at']


class BatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete batch
    """
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer 
    lookup_field = 'batch_number'


class GenerateBatchNumberView(APIView):
    """
    API view to generate a new batch number
    """ 
    
    def post(self, request):
        doa = request.data.get('doa')
        year = request.data.get('year')
        
        if not doa or not year:
            return Response(
                {"error": "DOA and year are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
         
        latest_batch = Batch.objects.filter(doa=doa, year=year).order_by('-sequence').first()
        
        if latest_batch: 
            try:
                sequence = str(int(latest_batch.sequence) + 1).zfill(3)
            except ValueError:
                sequence = '001'
        else:
            sequence = '001'
        
        batch_number = f"{doa}/{year}/{sequence}"
        
        return Response(
            {
                "batch_number": batch_number,
                "doa": doa,
                "year": year,
                "sequence": sequence
            },
            status=status.HTTP_200_OK
        )
    

class BatchDetailsSearchAPIView(generics.GenericAPIView):
    """
    API view to search for batch details by batch number using POST
    with a request body payload
    """
    serializer_class = BatchSerializer 
    queryset = Batch.objects.all()
    
    def post(self, request, *args, **kwargs):
        search_serializer = BatchNumberSearchSerializer(data=request.data)
        if not search_serializer.is_valid():
            return Response(
                search_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        batch_number = search_serializer.validated_data.get('batch_number')
        
        try:
            batch = self.queryset.get(batch_number=batch_number)
            response_serializer = self.serializer_class(batch)
            
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return Response(
                {"error": f"Batch with number '{batch_number}' not found"},
                status=status.HTTP_404_NOT_FOUND
            )
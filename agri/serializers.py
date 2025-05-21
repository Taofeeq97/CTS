from rest_framework import serializers
from .models import Farmer, CollectionCenter, ProcessingFacility, PackagingCenter, Batch


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        # Auto-generate farmer_id if not provided
        if 'farmer_id' not in validated_data:
            latest_farmer = Farmer.objects.order_by('-id').first()
            farmer_id = f"F{str(latest_farmer.id + 1).zfill(3)}" if latest_farmer else "F001"
            validated_data['farmer_id'] = farmer_id
        return super().create(validated_data)


class CollectionCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionCenter
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        # Auto-generate center_id if not provided
        if 'center_id' not in validated_data:
            latest_center = CollectionCenter.objects.order_by('-id').first()
            center_id = f"CC{str(latest_center.id + 1).zfill(3)}" if latest_center else "CC001"
            validated_data['center_id'] = center_id
        return super().create(validated_data)


class ProcessingFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingFacility
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        # Auto-generate facility_id if not provided
        if 'facility_id' not in validated_data:
            latest_facility = ProcessingFacility.objects.order_by('-id').first()
            facility_id = f"PF{str(latest_facility.id + 1).zfill(3)}" if latest_facility else "PF001"
            validated_data['facility_id'] = facility_id
        return super().create(validated_data)


class PackagingCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagingCenter
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        # Auto-generate center_id if not provided
        if 'center_id' not in validated_data:
            latest_center = PackagingCenter.objects.order_by('-id').first()
            center_id = f"PC{str(latest_center.id + 1).zfill(3)}" if latest_center else "PC001"
            validated_data['center_id'] = center_id
        return super().create(validated_data)


class BatchSerializer(serializers.ModelSerializer):
    contributing_farmers = serializers.PrimaryKeyRelatedField(
        queryset=Farmer.objects.all(),
        many=True
    )
    
    class Meta:
        model = Batch
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate(self, data):
        """
        Validate that compliance checkboxes are marked
        """
        if not data.get('zero_child_labor'):
            raise serializers.ValidationError(
                "Batch must be confirmed to be produced with ZERO child labor"
            )
        if not data.get('zero_deforestation'):
            raise serializers.ValidationError(
                "Batch must be confirmed to be produced with ZERO deforestation"
            )
        return data
    
    def to_representation(self, instance):
        """
        Add detailed information about related entities
        """
        representation = super().to_representation(instance)
        representation['collection_center'] = CollectionCenterSerializer(
            instance.collection_center
        ).data
        representation['processing_facility'] = ProcessingFacilitySerializer(
            instance.processing_facility
        ).data
        representation['packaging_center'] = PackagingCenterSerializer(
            instance.packaging_center
        ).data
        representation['contributing_farmers'] = FarmerSerializer(
            instance.contributing_farmers.all(), many=True
        ).data
        return representation
    

class BatchNumberSearchSerializer(serializers.Serializer):
    batch_number = serializers.CharField(max_length=255, required=True)

from django.db import models
from django.core.validators import MinValueValidator


class Farmer(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    CERTIFICATION_CHOICES = (
        ('organic', 'Organic'),
        ('fair_trade', 'Fair Trade'),
        ('none', 'None'),
    )
    
    farmer_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(null=True, blank=True)
    farm_size = models.FloatField(validators=[MinValueValidator(0)], help_text="Farm size in hectares")
    years_in_farming = models.PositiveIntegerField(null=True, blank=True)
    region = models.CharField(max_length=100)
    certification = models.CharField(max_length=20, choices=CERTIFICATION_CHOICES, default='none')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farmer_id} - {self.name}"


class CollectionCenter(models.Model):
    DRYING_METHOD_CHOICES = (
        ('sun_dried', 'Sun-dried'),
        ('mechanical', 'Mechanical'),
        ('controlled_drying', 'Controlled drying'),
    )
    
    center_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=50, null=True, blank=True)
    manager = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    drying_method = models.CharField(max_length=30, choices=DRYING_METHOD_CHOICES)
    capacity = models.FloatField(validators=[MinValueValidator(0)], help_text="Capacity in tons/day")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.center_id} - {self.name}"


class ProcessingFacility(models.Model):
    facility_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=50, null=True, blank=True)
    manager = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    capacity = models.FloatField(validators=[MinValueValidator(0)], help_text="Capacity in tons/day")
    haccp_certified = models.BooleanField(default=False)
    iso_22000_certified = models.BooleanField(default=False)
    fair_trade_certified = models.BooleanField(default=False)
    organic_certified = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.facility_id} - {self.name}"


class PackagingCenter(models.Model):
    center_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.FloatField(validators=[MinValueValidator(0)], help_text="Capacity in tons/day")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.center_id} - {self.name}"


class Batch(models.Model):
    batch_number = models.CharField(max_length=20, unique=True)
    doa = models.CharField(max_length=4)  # Department of Agriculture
    year = models.CharField(max_length=4)
    sequence = models.CharField(max_length=10)
    collection_center = models.ForeignKey(CollectionCenter, on_delete=models.CASCADE)
    processing_facility = models.ForeignKey(ProcessingFacility, on_delete=models.CASCADE)
    packaging_center = models.ForeignKey(PackagingCenter, on_delete=models.CASCADE)
    contributing_farmers = models.ManyToManyField(Farmer, related_name='batches')
    packaging_date = models.DateField()
    expiry_date = models.DateField()
    zero_child_labor = models.BooleanField(default=False)
    zero_deforestation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.batch_number
    
    def save(self, *args, **kwargs):
        if not self.batch_number:
            # Generate batch number if not provided
            self.batch_number = f"{self.doa}/{self.year}/{self.sequence}"
        super().save(*args, **kwargs)
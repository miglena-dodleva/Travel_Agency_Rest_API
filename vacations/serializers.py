from rest_framework import serializers
from .models import Location, Holiday, Reservation


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):
    #location = LocationSerializer()  # Use nested serializer
    #location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    #location_details = LocationSerializer()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Holiday
        fields = '__all__'

    def get_location(self, obj):
        # For read operations, return detailed location data
        return LocationSerializer(obj.location).data

    def create(self, validated_data):
        location_id = validated_data.pop('location', None)
        if location_id:
            location = Location.objects.get(pk=location_id)
            validated_data['location'] = location
        return Holiday.objects.create(**validated_data)

    def to_internal_value(self, data):
        # Transform the incoming data to include location_id
        internal_data = super().to_internal_value(data)
        location_id = data.get('location')
        if location_id is not None:
            internal_data['location_id'] = location_id
        return internal_data


class ReservationSerializer(serializers.ModelSerializer):
    #holiday = serializers.PrimaryKeyRelatedField(queryset=Holiday.objects.all())

    # Use 'holiday' for the nested full holiday details
    holiday = HolidaySerializer(read_only=True)
    # If you still need to accept a holiday ID for write operations, rename this field
    holiday_id = serializers.PrimaryKeyRelatedField(
        queryset=Holiday.objects.all(),
        write_only=True,
        source='holiday')

    class Meta:
        model = Reservation
        fields = '__all__'

class CreateReservationSerializer(serializers.ModelSerializer):
    holiday = serializers.PrimaryKeyRelatedField(queryset=Holiday.objects.all())

    class Meta:
        model = Reservation
        fields = '__all__'


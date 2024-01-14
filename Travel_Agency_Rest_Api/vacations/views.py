import json
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Location, Holiday, Reservation
from .serializers import LocationSerializer, HolidaySerializer, ReservationSerializer


# Create your views here.


@api_view(['GET', 'POST', 'PUT'])
def location_list(request):

    #get all the locations
    #serialize them
    #return json

    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
        #return JsonResponse({"locations": serializer.data}, safe= False)

    if request.method == 'POST':  #add
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':  # edit

        if not request.data.get('id'):
            return Response({'message': 'Missing location ID'}, status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')

        try:
            location = Location.objects.get(pk=id)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, id):

    try:
        location = Location.objects.get(pk=id)
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT'])
def holiday_list(request):

    if request.method == 'GET':
        # Retrieve query parameters
        location_query = request.query_params.get('location', '').lower()
        start_date = request.query_params.get('startDate')
        duration_query = request.query_params.get('duration')

        holidays = Holiday.objects.all()

        # Apply location filter
        if location_query:
            holidays = holidays.filter(
                Q(location__country__iexact=location_query) |
                Q(location__city__iexact=location_query)
            )

        # Apply start date filter
        if start_date:
            start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            holidays = holidays.filter(startDate__gte=start_date_obj)

        if duration_query:
            # Assuming duration is an integer representing the number of days
            duration_query = int(duration_query)
            holidays = holidays.filter(duration__gte=duration_query)

        serializer = HolidaySerializer(holidays, many=True)
        return Response(serializer.data)

    elif request.method == 'POST': #add

        data = request.data

        serializer = HolidaySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT': #edit

        if not request.data.get('id'):
            return Response({'message': 'Missing holiday ID'}, status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')

        try:
            holiday = Holiday.objects.get(pk=id)
        except Holiday.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HolidaySerializer(holiday, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def holiday_detail(request, id):

    try:
        holiday = Holiday.objects.get(pk=id)
    except Holiday.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HolidaySerializer(holiday)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        holiday.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT'])
def reservation_list(request):

    if request.method == 'GET':

        reservations = Reservation.objects.all()

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    if request.method == 'POST': #add
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT': #edit

        if not request.data.get('id'):
            return Response({'message': 'Missing reservation ID'}, status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')

        try:
            reservation = Reservation.objects.get(pk=id)
        except Reservation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def reservation_detail(request, id):

    try:
        reservation = Reservation.objects.get(pk=id)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def find_reservation(request):

    try:
        phoneNumber = request.data.get('phoneNumber')
        reservation = Reservation.objects.get(phoneNumber=phoneNumber)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
    except Reservation.DoesNotExist:
        return Response({"message": "No reservation found for this phone number."}, status=404)
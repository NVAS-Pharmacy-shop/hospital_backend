import json
from datetime import timedelta

import pika
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from hospital_contract import models
from hospital_contract.models import Hospital, Equipment
from hospital_contract.serializers import ContractSerializer, HospitalSerializer
from hospital_contract.tasks import send_contract_to_rabbitmq

class MakeContract(APIView):
    def post(self, request):
        print(request.data)
        hospital_id = request.data.get('hospital_id')
        equipment_data = request.data.get('equipment', [])
        print(equipment_data)
        date = request.data.get('date')
        date = parse_datetime(date) - timedelta(minutes=int(request.data.get('timezone_offset')))
        company = request.data.get('company')

        if not hospital_id or not date or not company:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hospital = Hospital.objects.get(id=hospital_id)
        except Hospital.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)

        existing_contract = models.Contract.objects.filter(hospital_id=hospital_id).first()
        if existing_contract:
            existing_contract.delete()

        contract_data = {
            'hospital': hospital,
            'date': date,
            'company': company
        }

        contract = models.Contract.objects.create(**contract_data)

        for item in equipment_data:
            equipment_id = item.get('equipment_id')
            quantity = item.get('quantity')
            contract.equipment.create(equipment_id=equipment_id, quantity=quantity)

        send_contract_to_rabbitmq(contract.id)


        return Response({"contract_id": contract.id}, status=status.HTTP_201_CREATED)
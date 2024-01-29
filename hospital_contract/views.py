from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from hospital_contract import models
from hospital_contract.models import Hospital, Equipment
from hospital_contract.serializers import ContractSerializer, HospitalSerializer


class MakeContract(APIView):
    def post(self, request):
        hospital_id = request.data.get('hospital_id')
        equipment_data = request.data.get('equipment', [])
        date = request.data.get('date')
        company = request.data.get('company')

        if not hospital_id or not date or not company:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hospital = Hospital.objects.get(id=hospital_id)
        except Hospital.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)

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

        serializer = ContractSerializer(data=contract)

        if serializer.is_valid():
            serializer.save()
            return Response(contract, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from rest_framework import serializers
from .models import Hospital, Equipment, Contract

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'address']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['equipment_id', 'quantity']

class ContractSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)
    equipment = EquipmentSerializer(many=True, required=False)
    class Meta:
        model = Contract
        fields = ['id', 'hospital', 'date', 'company', 'equipment']
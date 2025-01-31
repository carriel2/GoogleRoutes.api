from rest_framework import serializers

class RotaSerializer(serializers.Serializer):
    enderecos = serializers.ListField(child=serializers.CharField())

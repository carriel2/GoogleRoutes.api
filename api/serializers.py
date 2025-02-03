from rest_framework import serializers

class RotaSerializer(serializers.Serializer):
    origem = serializers.CharField()
    enderecos = serializers.ListField(child=serializers.CharField())

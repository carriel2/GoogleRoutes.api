import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import RotaSerializer

GOOGLE_MAPS_API_KEY = 'AIzaSyBE5N_CvJrjx6G3BxTYglLe3KKXoDkkqCI'

@api_view(['POST'])
def otimizar_rota(request):
    serializer = RotaSerializer(data=request.data)
    
    if serializer.is_valid():
        enderecos = serializer.validated_data['enderecos']

        if len(enderecos) < 2:
            return JsonResponse({"erro": "É necessário pelo menos dois endereços"}, status=400)

        origem = enderecos[0]  # Localização atual (fixa)
        waypoints = enderecos[1:]  # Todos os outros endereços podem ser reordenados

        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origem,
            "destination": origem,  # O destino é igual à origem para permitir reordenação total
            "waypoints": "optimize:true|" + "|".join(waypoints),
            "key": GOOGLE_MAPS_API_KEY
        }

        response = requests.get(url, params=params)
        dados = response.json()

        print("🔹 Resposta da API do Google Maps:", dados)  # Debug no terminal

        if dados.get("status") == "OK":
            rota_otimizada = [origem]  # Começa com a localização atual (fixa)

            # Pegando a sequência otimizada de waypoints
            waypoint_order = dados["routes"][0].get("waypoint_order", [])
            waypoints_ordenados = [waypoints[i] for i in waypoint_order]

            # Adicionando waypoints otimizados à rota final
            rota_otimizada.extend(waypoints_ordenados)

            return JsonResponse({"rota_otimizada": rota_otimizada}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"erro": f"Erro na API do Google: {dados.get('status')}"}, status=400)
    
    return JsonResponse(serializer.errors, status=400)

import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import RotaSerializer
from decouple import config

GOOGLE_MAPS_API_KEY = config('GOOGLE_SECRET_KEY')
DESTINO_FIXO = "R. Cristóvão Colombo, 388 - Jardim Paulista, Santa Bárbara d'Oeste - SP"

@api_view(['POST'])
def otimizar_rota(request):
    serializer = RotaSerializer(data=request.data)
    
    if serializer.is_valid():
        enderecos = serializer.validated_data['enderecos']  # Lista de endereços inseridos (waypoints)
        if len(enderecos) < 1:
            return JsonResponse({"erro": "É necessário pelo menos um endereço além da origem."}, status=400)
        
        origem = request.data.get("origem")  # Origem enviada pelo frontend
        if not origem:
            return JsonResponse({"erro": "Origem não fornecida."}, status=400)
        
        # Limpa espaços extras de cada endereço para evitar problemas de formatação
        enderecos = [e.strip() for e in enderecos]
        
        # Monta a string de waypoints com otimização
        waypoints_str = f"optimize:true|{'|'.join(enderecos)}"
        
        # Parâmetros para a API do Google Directions
        params = {
            "origin": origem,
            "destination": DESTINO_FIXO,
            "waypoints": waypoints_str,
            "key": GOOGLE_MAPS_API_KEY
        }
        
        url = "https://maps.googleapis.com/maps/api/directions/json"
        response = requests.get(url, params=params)
        dados = response.json()
        
        # Log completo para depuração
        print("🔹 Resposta da API do Google Maps:", dados)
        
        if dados.get("status") == "OK":
            rota_otimizada = [origem]
            # Verifica se o campo 'routes' possui resultados e se 'waypoint_order' está presente
            if dados["routes"]:
                waypoint_order = dados["routes"][0].get("waypoint_order", [])
                print("🔹 waypoint_order:", waypoint_order)
                
                # Se a API retornou uma ordem otimizada para os waypoints
                if waypoint_order and len(waypoint_order) == len(enderecos):
                    waypoints_ordenados = [enderecos[i] for i in waypoint_order]
                else:
                    # Se a ordem não foi otimizada ou não corresponde ao número de waypoints,
                    # usa a lista original (ou exibe log para investigar)
                    print("🔹 Ordem otimizada não retornada ou incompleta; usando ordem original.")
                    waypoints_ordenados = enderecos
                    
                rota_otimizada.extend(waypoints_ordenados)
            else:
                # Caso não haja nenhuma rota retornada, mantém os waypoints originais
                rota_otimizada.extend(enderecos)
            
            rota_otimizada.append(DESTINO_FIXO)
            return JsonResponse({"rota_otimizada": rota_otimizada}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"erro": f"Erro na API do Google: {dados.get('status')}"}, status=400)
    
    return JsonResponse(serializer.errors, status=400)

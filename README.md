# GoogleRoutes.api

API REST com Django REST Framework:
O backend é construído sobre Django e expõe um endpoint que recebe os endereços intermediários e a origem (localização atual do dispositivo) via requisições POST.

Integração com a API do Google Maps:
Utilizando a API Directions do Google Maps, o backend envia os endereços recebidos como waypoints – com a opção de otimização ativada – e utiliza um endereço fixo pré-definido como destino final.

Otimização de Rota:
A API do Google Maps retorna a melhor ordem possível para percorrer os waypoints. O backend processa essa resposta e retorna uma lista ordenada contendo a origem, os waypoints otimizados e o destino fixo.

Facilidade de Integração:
Com um serializer simples (validando que os endereços sejam uma lista de strings) e uma lógica de tratamento robusta, o backend garante que os dados recebidos estejam no formato esperado, facilitando a integração com o frontend.

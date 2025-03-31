import requests

class LocationIQ:
    def __init__(self):
        self.access_token = 'SUA_CHAVE_AQUI'  # 🔴 Substitua pela sua chave válida

    def request_locationiq(self, url):
        """Função auxiliar para realizar requisições e tratar erros."""
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Lança erro se a resposta for ruim (4xx ou 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição LocationIQ: {e}")
            return None

    def autocomplete(self, query):
        url = f"https://us1.locationiq.com/v1/autocomplete.php?key={self.access_token}&q={query}&format=json"
        return self.request_locationiq(url)

    def geocode(self, address):
        url = f"https://us1.locationiq.com/v1/search.php?key={self.access_token}&q={address}&format=json"
        return self.request_locationiq(url)

    def reverse_geocode(self, lat, lon):
        url = f"https://us1.locationiq.com/v1/reverse.php?key={self.access_token}&lat={lat}&lon={lon}&format=json"
        return self.request_locationiq(url)

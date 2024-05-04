import requests

def get_crypto_price(crypto_symbol):
    api_key = ''  # Replace 'YOUR_API_KEY' with your actual API key
    url = f'https://min-api.cryptocompare.com/data/price?fsym={crypto_symbol}&tsyms=USD&api_key={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        if 'USD' in data:
            return data['USD']
        else:
            return None
    except Exception as e:
        print(f"Error fetching crypto price: {e}")
        return None


import requests
from datetime import datetime
from config import ALPHA_VANTAGE_API_KEY

# Sõnastik ettevõtete nimede ja sümbolite jaoks
COMPANY_SYMBOLS = {
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'tesla': 'TSLA',
    'nvidia': 'NVDA',
    'google': 'GOOGL',
    'amazon': 'AMZN',
    'meta': 'META',
    'netflix': 'NFLX',
    'intel': 'INTC',
    'amd': 'AMD',
    'samsung': '005930.KS',
    'sony': 'SONY',
    'nike': 'NKE',
    'coca-cola': 'KO',
    'mcdonalds': 'MCD',
    'visa': 'V',
    'mastercard': 'MA',
    'paypal': 'PYPL',
    'adobe': 'ADBE',
    'salesforce': 'CRM'
}

def get_stock_price(symbol):
    # Alpha Vantage API endpoint
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'Global Quote' in data:
            quote = data['Global Quote']
            price = quote.get('05. price', 'N/A')
            change = quote.get('09. change', 'N/A')
            change_percent = quote.get('10. change percent', 'N/A')
            
            return {
                'symbol': symbol,
                'price': price,
                'change': change,
                'change_percent': change_percent
            }
        else:
            return {'error': 'Aktsia andmeid ei leitud'}
            
    except Exception as e:
        return {'error': f'Viga andmete pärimisel: {str(e)}'}

def get_symbol_from_name(name):
    # Otsi sümbolit nime järgi
    name = name.lower()
    if name in COMPANY_SYMBOLS:
        return COMPANY_SYMBOLS[name]
    return None

def main():
    print("Tere tulemast aktsiahinna otsingusse!")
    print("Sisestage börsi sümbol või ettevõtte nimi (näiteks: AAPL, MSFT, Apple, Tesla)")
    print("\nSaadaval ettevõtted:")
    for name, symbol in COMPANY_SYMBOLS.items():
        print(f"- {name.title()} ({symbol})")
    
    while True:
        user_input = input("\nSisestage börsi sümbol või ettevõtte nimi (või 'välju' lõpetamiseks): ").strip()
        
        if user_input.lower() == 'välju':
            print("Tänan kasutamast! Head päeva!")
            break
        
        # Proovi leida sümbol nime järgi
        symbol = get_symbol_from_name(user_input.lower())
        if not symbol:
            # Kui sümbolit ei leitud, kasuta sisestatud teksti otse sümbolina
            symbol = user_input.upper()
            
        result = get_stock_price(symbol)
        
        if 'error' in result:
            print(f"Viga: {result['error']}")
        else:
            print(f"\nAktsia: {result['symbol']}")
            print(f"Hind: ${result['price']}")
            print(f"Muutus: ${result['change']} ({result['change_percent']})")

if __name__ == "__main__":
    main() 
import requests
from datetime import datetime
from config import ALPHA_VANTAGE_API_KEY, NEWS_API_KEY

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
    'mcdonalds': 'MCD'
}

def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'Global Quote' in data:
            quote = data['Global Quote']
            return {
                'symbol': symbol,
                'price': quote.get('05. price', 'N/A'),
                'change': quote.get('09. change', 'N/A'),
                'change_percent': quote.get('10. change percent', 'N/A')
            }
        return {'error': 'Aktsia andmeid ei leitud'}
    except Exception as e:
        return {'error': f'Viga andmete pärimisel: {str(e)}'}

def get_stock_news(symbol):
    url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'articles' in data:
            return data['articles'][:5]  # Tagasta 5 uusimat uudist
        return []
    except Exception as e:
        print(f"Viga uudiste pärimisel: {str(e)}")
        return []

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
        symbol = COMPANY_SYMBOLS.get(user_input.lower(), user_input.upper())
        
        print("\nValige, mida soovite teha:")
        print("1. Vaata aktsiahinda")
        print("2. Vaata aktsia uudiseid")
        print("3. Välju")
        
        action = input("Valik: ").strip()
        
        if action == '1':
            result = get_stock_price(symbol)
            if 'error' in result:
                print(f"Viga: {result['error']}")
            else:
                print(f"\nAktsia: {result['symbol']}")
                print(f"Hind: ${result['price']}")
                print(f"Muutus: ${result['change']} ({result['change_percent']})")
        
        elif action == '2':
            news = get_stock_news(symbol)
            if news:
                print(f"\n{symbol} aktsia uudised:")
                for article in news:
                    print(f"\nPealkiri: {article['title']}")
                    print(f"Kokkuvõte: {article['description']}")
                    print(f"Link: {article['url']}")
            else:
                print("Uudiseid ei leitud")
        
        elif action == '3':
            print("Tänan kasutamast! Head päeva!")
            break

if __name__ == "__main__":
    main() 
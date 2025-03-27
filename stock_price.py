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
        return {'error': f'Vea andmete pärimisel: {str(e)}'}

def get_historical_data(symbol, start_date, end_date):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=full'
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (Daily)' in data:
        time_series = data['Time Series (Daily)']
        filtered_data = {date: stats for date, stats in time_series.items() if start_date <= date <= end_date}
        return filtered_data
    return {'error': 'Ajaloolisi andmeid ei leitud'}

def calculate_moving_average(symbol, period=50):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (Daily)' in data:
        time_series = data['Time Series (Daily)']
        closing_prices = [float(day['4. close']) for day in time_series.values()]
        
        if len(closing_prices) >= period:
            moving_average = sum(closing_prices[:period]) / period
            return moving_average
    return {'error': 'Viga liikuva keskmise arvutamisel'}

def get_symbol_from_name(name):
    # Otsi sümbolit nime järgi
    name = name.lower()
    if name in COMPANY_SYMBOLS:
        return COMPANY_SYMBOLS[name]
    return None

def compare_stock_prices(symbol1, symbol2):
    price1 = get_stock_price(symbol1)
    price2 = get_stock_price(symbol2)
    
    if 'error' in price1 or 'error' in price2:
        return {'error': 'Viga aktsiate võrreldes'}
    
    comparison = {
        'symbol1': price1['symbol'],
        'price1': price1['price'],
        'symbol2': price2['symbol'],
        'price2': price2['price']
    }
    
    return comparison

def get_stock_news(symbol):
    url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'articles' in data:
        return [{'title': article['title'], 'description': article['description']} for article in data['articles']]
    return {'error': 'Uudiseid ei leitud'}

def get_portfolio_value(portfolio):
    total_value = 0
    for symbol, quantity in portfolio.items():
        price_data = get_stock_price(symbol)
        if 'error' in price_data:
            print(f"Viga aktsia {symbol} hinna saamisel.")
            continue
        total_value += float(price_data['price']) * quantity
    return total_value

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
        
        print("\nValige, mida soovite teha:")
        print("1. Vaata aktsiahinda")
        print("2. Vaata ajaloolisi andmeid")
        print("3. Arvuta liikuva keskmine")
        print("4. Võrdle kahte aktsiat")
        print("5. Vaata aktsia uudiseid")
        print("6. Arvuta portfellihind")
        print("7. Välju")
        
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
            start_date = input("Sisestage alguskuupäev (YYYY-MM-DD): ")
            end_date = input("Sisestage lõppkuupäev (YYYY-MM-DD): ")
            historical_data = get_historical_data(symbol, start_date, end_date)
            if 'error' in historical_data:
                print(f"Viga: {historical_data['error']}")
            else:
                print(f"Ajalooline andmed aktsiale {symbol}:")
                for date, stats in historical_data.items():
                    print(f"{date}: {stats['4. close']}")
        
        elif action == '3':
            period = int(input("Sisestage periood (nt 50): "))
            moving_average = calculate_moving_average(symbol, period)
            if 'error' in moving_average:
                print(f"Viga: {moving_average['error']}")
            else:
                print(f"{symbol} liikuva keskmine ({period} päeva): {moving_average}")
        
        elif action == '4':
            symbol2 = input("Sisestage teine aktsia sümbol: ").upper()
            comparison = compare_stock_prices(symbol, symbol2)
            if 'error' in comparison:
                print(f"Viga: {comparison['error']}")
            else:
                print(f"Aktsiad {symbol} vs {symbol2}:")
                print(f"{symbol}: {comparison['price1']}")
                print(f"{symbol2}: {comparison['price2']}")
        
        elif action == '5':
            news = get_stock_news(symbol)
            if 'error' in news:
                print(f"Viga: {news['error']}")
            else:
                print(f"{symbol} aktsia uudised:")
                for article in news:
                    print(f"Pealkiri: {article['title']}")
                    print(f"Kokkuvõte: {article['description']}")
        
        elif action == '6':
            portfolio = {}
            while True:
                stock = input("Sisestage aktsia sümbol või 'lõpeta' lõpetamiseks: ").upper()
                if stock == 'LÕPETA':
                    break
                quantity = int(input(f"Kui palju {stock} aktsiaid on teil? "))
                portfolio[stock] = quantity
            portfolio_value = get_portfolio_value(portfolio)
            print(f"Portfelli koguväärtus: ${portfolio_value}")
        
        elif action == '7':
            print("Tänan kasutamast! Head päeva!")
            break

if __name__ == "__main__":
    main()

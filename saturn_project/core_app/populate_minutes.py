from core_app.models import SupportedMinute

def populate_supported_minutes():
    minutes_data = [
        {
            'name': 'FOMC Minutes',
            'description': 'Minutas de las reuniones del Comité Federal de Mercado Abierto, discutiendo tasas de interés y política monetaria.',
            'impact': 'High',
            'country': 'United States',
            'source': 'Federal Reserve',
            'frequency': 'Every 6 weeks',
            'markets_affected': 'Forex, Equities, Commodities',
            'symbols_affected': 'EUR/USD, USD/JPY, S&P 500',
        },
        {
            'name': 'ECB Minutes',
            'description': 'Minutas de las reuniones del Banco Central Europeo, incluyendo decisiones de política monetaria.',
            'impact': 'High',
            'country': 'Eurozone',
            'source': 'European Central Bank',
            'frequency': 'Every 4 weeks',
            'markets_affected': 'Forex, Equities',
            'symbols_affected': 'EUR/USD, EUR/GBP',
        },
        {
            'name': 'BoE Minutes',
            'description': 'Minutas del Comité de Política Monetaria del Banco de Inglaterra.',
            'impact': 'High',
            'country': 'United Kingdom',
            'source': 'Bank of England',
            'frequency': 'Monthly',
            'markets_affected': 'Forex, Equities',
            'symbols_affected': 'GBP/USD, GBP/EUR',
        },
        {
            'name': 'BoJ Minutes',
            'description': 'Minutas de las reuniones de política monetaria del Banco de Japón.',
            'impact': 'High',
            'country': 'Japan',
            'source': 'Bank of Japan',
            'frequency': 'Monthly',
            'markets_affected': 'Forex, Equities',
            'symbols_affected': 'USD/JPY, EUR/JPY',
        },
        {
            'name': 'Banxico Minutes',
            'description': 'Minutas de las reuniones de política monetaria del Banco de México.',
            'impact': 'Medium',
            'country': 'Mexico',
            'source': 'Banco de México',
            'frequency': 'Every 6 weeks',
            'markets_affected': 'Forex',
            'symbols_affected': 'USD/MXN, EUR/MXN',
        },
    ]

    for data in minutes_data:
        SupportedMinute.objects.update_or_create(
            name=data['name'],
            defaults=data
        )

if __name__ == "__main__":
    populate_supported_minutes()
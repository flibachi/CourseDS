import sys

def get_stock_price():
    COMPANIES = {  
        'Apple': 'AAPL',  
        'Microsoft': 'MSFT',  
        'Netflix': 'NFLX',  
        'Tesla': 'TSLA',  
        'Nokia': 'NOK'  
    }  
    STOCKS = {  
        'AAPL': 287.73,  
        'MSFT': 173.79,  
        'NFLX': 416.90,  
        'TSLA': 724.88,  
        'NOK': 3.37  
    }

    if len(sys.argv) != 2:
        return
        
    company_name = sys.argv[1].title()

    if company_name in COMPANIES:
        print(STOCKS[COMPANIES[company_name]])
    else:
        print("Unknown company")

if __name__ == '__main__':
    get_stock_price()
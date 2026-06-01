import sys

def get_comp_and_price():
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

    ticker = sys.argv[1].upper()
    if ticker in STOCKS:
        for k, v in COMPANIES.items():
            if v == ticker:
                print(f"{k} {STOCKS[v]}")
    else:
        print("Unknown company")

if __name__ == '__main__':
    get_comp_and_price()
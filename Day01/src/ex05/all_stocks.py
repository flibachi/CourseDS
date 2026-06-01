import sys

# def company_dict():
#     return {  
#         'Apple': 'AAPL',  
#         'Microsoft': 'MSFT',  
#         'Netflix': 'NFLX',  
#         'Tesla': 'TSLA',  
#         'Nokia': 'NOK'  
#     }  

# def tickers_dict():
#     return {  
#         'AAPL': 287.73,  
#         'MSFT': 173.79,  
#         'NFLX': 416.90,  
#         'TSLA': 724.88,  
#         'NOK': 3.37  
#     }


def dicts():
    companies = {  
        'Apple': 'AAPL',  
        'Microsoft': 'MSFT',  
        'Netflix': 'NFLX',  
        'Tesla': 'TSLA',  
        'Nokia': 'NOK'  
    }  
    tickers = {  
        'AAPL': 287.73,  
        'MSFT': 173.79,  
        'NFLX': 416.90,  
        'TSLA': 724.88,  
        'NOK': 3.37  
    }
    return companies, tickers

def convert_input():
    if len(sys.argv) != 2:
        return None
    
    input_string = sys.argv[1]
    correct_string = [expr.strip() for expr in input_string.split(',')]
    
    return correct_string

def all_stocks():
    correct_string = convert_input()

    if correct_string is None:
        return

    if '' in correct_string:
        return
    
    companies, tickers = dicts()
    companies_lower = {key.lower(): value for key, value in companies.items()}
    tickers_to_companies = {value: key for key, value in companies.items()}

    for arg in correct_string:
        arg_upper = arg.upper()
        arg_lower = arg.lower()

        if arg_upper in tickers_to_companies:
            company_name = tickers_to_companies.get(arg_upper)
            print(f"{arg_upper} is a ticker symbol for {company_name}")
        elif arg_lower in companies_lower:
            ticker = companies_lower[arg_lower]
            price = tickers[ticker]
            print(f"{arg_lower.title()} stock price is {price}")
        else:
            print(f"{arg} is an unknown company or an unknown ticker symbol")

if __name__ == '__main__':
    all_stocks()
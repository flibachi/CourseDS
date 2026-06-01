import logging

num_of_steps = 3

logging.basicConfig(
    filename='analytics.log',
    level=logging.DEBUG,
    format="%(asctime)s %(message)s"
)

TOKEN = "5519391736:AAFhg1BpgjgI8YesHN3GvU3lTzYH7NjH8As"
CHAT_ID = "1170586159"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

SUCCESS_MSG = "The report has been successfully created"
ERROR_MSG = "The report hasn't been created due to an error"

# get_updates_url = f"https://api.telegram.org/bot{token}/getUpdates"

report_text = """Report\n\nWe have made {observations} observations from \
tossing a coin: {heads1} of them were tails and {tails1} of them were
heads. The probabilities are {fract_heads1:.2f}% and {fract_tails1:.2f}%, \
respectively. Our forecast is that in the next {num_of_steps}
observations we will have: {tails2} tail{s1} and {heads2} head{s2}."""

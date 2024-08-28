import bokeh, requests
import globals

def check_network_status():
    try:
        requests.get(r"https://www.google.com",timeout=10)
        globals.NETWORK_STATUS = True
    except requests.ConnectionError:
        globals.NETWORK_STATUS = False

def create_main_page(doc):
    pass
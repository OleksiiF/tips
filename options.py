# Proxy options.
USE_PROXY = False
PROXIES_FILENAME = 'proxies.json'  # Format of content ['host:port', 'host2:port2']
PROXY_SOURCE = 'http://pubproxy.com/api/proxy'
PROXIES_QUANTITY = 10

# Search options.
BASE_URL = 'https://allo.ua/ru/catalogsearch/ajax/suggest'
LETTERS_QUANTITY = 3
LANGUAGES = ['ru', 'en']

# Result of script work.
ERROR_LOG_NAME = 'err_log.log'
DATABASE_NAME = 'tips.sqlite'

# Essential data for the request.
REQUEST_PARAMS = {
    'currentTheme': 'main',
    'currentLocale': 'ru_RU'
}
REQUEST_HEADERS = {
    'x-requested-with': 'XMLHttpRequest'
}
REQUEST_PAYLOAD = {
    'isAJax': 1,
    'q': ''
}

import logging

# PISA-SERVER
DEFAULT_PISA_API_SERVER = 'btc.pisa.watch'
DEFAULT_PISA_API_PORT = 9814

# PISA-CLI
CLIENT_LOG_FILE = 'pisa.log'

# CRYPTO
SUPPORTED_HASH_FUNCTIONS = ["SHA256"]
SUPPORTED_CIPHERS = ["AES-GCM-128"]

# Configure logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO, handlers=[
    logging.FileHandler(CLIENT_LOG_FILE),
    logging.StreamHandler()
])

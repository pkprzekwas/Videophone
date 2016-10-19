import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.DEBUG)
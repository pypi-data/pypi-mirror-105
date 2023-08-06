from hestia_earth.utils.tools import non_empty_list, list_average

from hestia_earth.models.log import logger
from hestia_earth.models.utils.product import _new_product


def _run(product: dict):
    value = list_average(product.get('min') + product.get('max'))
    logger.info('term=%s, value=%s', product.get('term', {}).get('@id'), value)
    product = _new_product(product.get('term'))
    product['value'] = [value]
    return product


def _should_run(product: dict):
    return ('value' not in product or len(product['value']) == 0) and \
        len(product.get('min', [])) > 0 and len(product.get('max', [])) > 0


def run(cycle: dict):
    products = list(filter(_should_run, cycle.get('products', [])))
    return non_empty_list(map(_run, products))

from hestia_earth.utils.tools import non_empty_list, list_average

from hestia_earth.models.log import logger
from hestia_earth.models.utils.input import _new_input


def _run(input: dict):
    value = list_average(input.get('min') + input.get('max'))
    logger.info('term=%s, value=%s', input.get('term', {}).get('@id'), value)
    input = _new_input(input.get('term'))
    input['value'] = [value]
    return input


def _should_run(input: dict):
    return ('value' not in input or len(input['value']) == 0) and \
        len(input.get('min', [])) > 0 and len(input.get('max', [])) > 0


def run(cycle: dict):
    inputs = list(filter(_should_run, cycle.get('inputs', [])))
    return non_empty_list(map(_run, inputs))

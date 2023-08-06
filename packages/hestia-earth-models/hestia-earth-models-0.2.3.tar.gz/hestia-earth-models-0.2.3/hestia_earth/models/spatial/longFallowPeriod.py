from hestia_earth.schema import PracticeStatsDefinition

from hestia_earth.models.log import logger
from hestia_earth.models.utils.practice import _new_practice
from .utils import download, has_geospatial_data, _site_gadm_id
from . import MODEL

TERM_ID = 'longFallowPeriod'


def _practice(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    practice = _new_practice(TERM_ID, MODEL)
    practice['value'] = value
    practice['statsDefinition'] = PracticeStatsDefinition.SPATIAL.value
    return practice


def _run(site: dict):
    reducer = 'sum'

    # 1) extract maximum monthly growing area (MMGA)
    MMGA_value = download(collection='users/hestiaplatform/MMGA',
                          ee_type='raster',
                          reducer=reducer,
                          latitude=site.get('latitude'),
                          longitude=site.get('longitude'),
                          gadm_id=_site_gadm_id(site),
                          boundary=site.get('boundary'),
                          fields=reducer
                          )
    MMGA_value = MMGA_value.get('first', MMGA_value.get('sum'))

    # 2) extract cropping extent (CE)
    CE_value = download(collection='users/hestiaplatform/CE',
                        ee_type='raster',
                        reducer=reducer,
                        latitude=site.get('latitude'),
                        longitude=site.get('longitude'),
                        gadm_id=_site_gadm_id(site),
                        boundary=site.get('boundary'),
                        fields=reducer
                        )
    CE_value = CE_value.get('first', CE_value.get('sum'))

    # 3) estimate longFallowPeriod from MMGA and CE.
    value = None if MMGA_value is None or CE_value is None else 365 * ((CE_value / MMGA_value) - 1)

    return [] if value is None else [_practice(value)]


def _should_run(site: dict):
    should_run = has_geospatial_data(site)
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else []

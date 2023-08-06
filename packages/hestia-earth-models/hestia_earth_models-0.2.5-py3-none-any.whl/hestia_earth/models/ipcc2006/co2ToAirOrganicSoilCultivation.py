from hestia_earth.models.log import logger
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.measurement import _most_relevant_measurement_value
from hestia_earth.schema import EmissionMethodTier, SiteSiteType
from hestia_earth.utils.tools import list_sum

from . import MODEL

TERM_ID = 'co2ToAirOrganicSoilCultivation'
CONVERT_FACTOR = 44 / 120
CO2_FACTORS_ORGANIC_SOILS = {
    SiteSiteType.CROPLAND.value: {
        '1': 10.0 * CONVERT_FACTOR,
        '2': 10.0 * CONVERT_FACTOR,
        '3': 5.0 * CONVERT_FACTOR,
        '4': 5.0 * CONVERT_FACTOR,
        '5': 5.0 * CONVERT_FACTOR,
        '6': 5.0 * CONVERT_FACTOR,
        '7': 5.0 * CONVERT_FACTOR,
        '8': 5.0 * CONVERT_FACTOR,
        '9': 20.0 * CONVERT_FACTOR,
        '10': 20.0 * CONVERT_FACTOR,
        '11': 20.0 * CONVERT_FACTOR,
        '12': 20.0 * CONVERT_FACTOR,
        '13': 20.0 * CONVERT_FACTOR
    },
    SiteSiteType.PERMANENT_PASTURE.value: {
        '1': 2.5 * CONVERT_FACTOR,
        '2': 2.5 * CONVERT_FACTOR,
        '3': 0.25 * CONVERT_FACTOR,
        '4': 0.25 * CONVERT_FACTOR,
        '5': 0.25 * CONVERT_FACTOR,
        '6': 0.25 * CONVERT_FACTOR,
        '7': 0.25 * CONVERT_FACTOR,
        '8': 0.25 * CONVERT_FACTOR,
        '9': 5.0 * CONVERT_FACTOR,
        '10': 5.0 * CONVERT_FACTOR,
        '11': 5.0 * CONVERT_FACTOR,
        '12': 5.0 * CONVERT_FACTOR,
        '13': 5.0 * CONVERT_FACTOR
    }
}


def _emission(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    return emission


def _run(histosol: float, organic_soil_factor: float, land_use_change: float):
    value = land_use_change * histosol * organic_soil_factor
    return [_emission(value)]


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    site_type = site.get('siteType', None)
    measurements = site.get('measurements', [])

    def _get_measurement_content(term_id: str):
        return _most_relevant_measurement_value(measurements, term_id, end_date)

    histosol = list_sum(_get_measurement_content('histosol'))
    eco_climate_zone = _get_measurement_content('ecoClimateZone')
    eco_climate_zone = str(eco_climate_zone[0]) if len(eco_climate_zone) > 0 else None
    organic_soil_factor = organic_soil_factor = CO2_FACTORS_ORGANIC_SOILS.get(site_type, {}).get(eco_climate_zone)
    land_use_change = list_sum(_get_measurement_content('landTransformation20YearAverage'))

    should_run = all([organic_soil_factor, land_use_change, histosol])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, histosol, organic_soil_factor, land_use_change


def run(cycle: dict):
    should_run, histosol, organic_soil_factor, land_use_change = _should_run(cycle)
    return _run(histosol, organic_soil_factor, land_use_change) if should_run else []

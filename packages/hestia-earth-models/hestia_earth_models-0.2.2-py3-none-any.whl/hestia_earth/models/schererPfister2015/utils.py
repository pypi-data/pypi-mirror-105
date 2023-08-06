from hestia_earth.schema import TermTermType
from hestia_earth.utils.lookup import download_lookup, get_table_value
from hestia_earth.utils.tools import list_sum, safe_parse_float
from hestia_earth.utils.model import filter_list_term_type, find_primary_product

from hestia_earth.models.utils.input import filter_by_term_type_and_lookup, \
    get_organic_fertilizer_P_total, get_total_phosphate, get_total_value


C2_FACTORS_TILLAGE = {
    'fullTillage': 0.95,
    'minimumTillage': 0.475,
    'noTillage': 0.25
}

SLOPE_RANGE = [
    [0.0, 0.03, 1.2],
    [0.03, 0.08, 1.0],
    [0.08, 0.12, 1.2],
    [0.12, 0.16, 1.4],
    [0.16, 0.20, 1.6],
    [0.20, 0.24, 1.8],
    [0.24, 0.28, 2.0],
    [0.28, 0.32, 2.2]
]


def get_liquid_slurry_sludge_ratio(cycle: dict):
    lss_inputs = filter_by_term_type_and_lookup(
        cycle.get('inputs', []), TermTermType.ORGANICFERTILIZER,
        col_name='OrganicFertilizerClassification',
        col_value='Liquid, Slurry, Sewage Sludge'
    )
    P_total = get_organic_fertilizer_P_total(cycle)
    P_lss = list_sum(get_total_phosphate(lss_inputs))
    return P_lss / P_total if P_total > 0 else 0


def get_management(cycle: dict):
    filter_management = ['fullTillage', 'minimumTillage', 'noTillage']
    practices = cycle.get('practices', [])
    v = next(filter(lambda i: i.get('term', {}).get('@id') in filter_management, practices), None)
    return v.get('term', {}).get('@id') if v is not None else None


def get_pcorr(slope: float):
    return next((element[2] for element in SLOPE_RANGE if slope >= element[0] and slope < element[1]), None)


def _search_lookup(lookup_name: str, column_name: str, term_id: str):
    lookup = download_lookup(lookup_name, True)
    return get_table_value(lookup, 'termid', term_id, column_name)


def get_p_ef_c1(cycle: dict):
    primary_product = find_primary_product(cycle)
    product_id = primary_product.get('term', {}).get('@id') if primary_product else None
    return safe_parse_float(_search_lookup('crop.csv', 'p_ef_c1', product_id), None) if product_id else None


def get_country_factors(cycle: dict):
    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    ef_p_c2 = safe_parse_float(_search_lookup('region.csv', 'ef_p_c2', country_id), None)
    practise_factor = safe_parse_float(_search_lookup('region.csv', 'practice_factor', country_id), None)
    return ef_p_c2, practise_factor


def get_water(cycle: dict, precipitation: float):
    inputs = cycle.get('inputs', [])
    filter_irrigation = filter_list_term_type(inputs, TermTermType.WATER)
    irrigation = list_sum(get_total_value(filter_irrigation))
    return list_sum([irrigation/10, precipitation])


def calculate_R(heavy_winter_precipitation: float, water: float):
    winter_precipitation = 1 if heavy_winter_precipitation > 0 else 0.1
    water_coeff = (587.8 - 1.219 * water) + (0.004105 * water ** 2) if water > 850 else (0.0483 * water ** 1.61)
    return water_coeff * winter_precipitation


def calculate_A(R: float, practise_factor, erodability, slope_length, pcorr, p_ef_c1, ef_p_c2, management):
    # TODO: for product == 'Pasture', replace `if management is None` by `if product is pasture or management is none`
    return R * erodability * slope_length * practise_factor * pcorr * p_ef_c1 * (
        ef_p_c2 if management is None else C2_FACTORS_TILLAGE[management])

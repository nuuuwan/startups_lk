from utils import jsonx

from startups_lk._constants import DATA_FILE


def load(min_funding_stage_i=-1, min_startup_stage_i=-1):
    data_list = jsonx.read(DATA_FILE)
    if min_funding_stage_i != -1:
        data_list = list(
            filter(
                lambda data: data['funding_stage_i'] >= min_funding_stage_i,
                data_list,
            )
        )
    if min_startup_stage_i != -1:
        data_list = list(
            filter(
                lambda data: data['startup_stage_i'] >= min_startup_stage_i,
                data_list,
            )
        )
    return data_list

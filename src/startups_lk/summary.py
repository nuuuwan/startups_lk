from utils import filex, timex

from startups_lk._utils import log
from startups_lk.startups import load_startups
from startups_lk._constants import REMOTE_DATA_DIR

startup_id=startup_id,
name=name,
remote_img_url=remote_img_url,
image_file_only=image_file_only,
tagline=tagline,
description=description,
url=url,
business_registration_date=business_registration_date,
business_registration_ut=business_registration_ut,
category_list=category_list,
startup_stage=startup_stage,
startup_stage_i=get_startup_stage_i(startup_stage),
funding_stage=funding_stage,
funding_stage_i=get_funding_stage_i(funding_stage),
founder_info=founder_info,
founder_info_list_raw=founder_info_list_raw,

def build_startup_summary(data):
    name = data['name']
    description = data['description']
    url = data['url']
    img_url = os.path.join(REMOTE_DATA_DIR, 'startups_lk-images', data['remote_img_url'])
    return [
        f'## [{}]()',
        f'## {name}',
        f'{description}',
        f'[{url}]({url})',
    ]


def build_summary():
    data_list = load_startups()
    time_str = timex.format_time(timex.get_unixtime(), '%B %d, %Y')
    md_lines = [
        '# Startups in Sri Lanka',
        'Source: [https://www.startupsl.lk](https://www.startupsl.lk)',
        f'*Generated: {time_str}*',
    ]

    for data in data_list:
        md_lines += build_startup_summary(data)

    md_file = '/tmp/README.md'
    filex.write(md_file, '\n\n'.join(md_lines))
    log.info(f'Wrote summary to {md_file}')

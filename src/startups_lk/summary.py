import os

from utils import filex, timex

from startups_lk._constants import REMOTE_DATA_DIR
from startups_lk._utils import log
from startups_lk.startups import load_startups

# startup_id=startup_id,
# name=name,
# remote_img_url=remote_img_url,
# image_file_only=image_file_only,
# tagline=tagline,
# description=description,
# url=url,
# business_registration_date=business_registration_date,
# business_registration_ut=business_registration_ut,
# category_list=category_list,
# startup_stage=startup_stage,
# startup_stage_i=get_startup_stage_i(startup_stage),
# funding_stage=funding_stage,
# funding_stage_i=get_funding_stage_i(funding_stage),
# founder_info=founder_info,
# founder_info_list_raw=founder_info_list_raw,


def build_startup_summary(data):
    name = data['name']
    tagline = data['tagline']
    description = data['description']
    url = data['url']
    img_url = os.path.join(
        REMOTE_DATA_DIR, 'startups_lk-images', data['image_file_only']
    )
    business_registration_ut = (int)(data['business_registration_ut'])
    business_registration_str = timex.format_time(
        business_registration_ut, '%B %d, %Y'
    )

    category_list = data['category_list']
    category_str = ' · '.join(category_list)

    founder_info = data['founder_info']
    founder_info_str_list = []
    email = founder_info.get('email')
    name = founder_info.get('name')
    phone = founder_info.get('phone')
    if email:
        founder_info_str_list.append(f'[{email}](mailto:{email})')
    if phone:
        founder_info_str_list.append(f'[{phone}](tel:{phone})')
    if name:
        name_str = name.replace(' ', '+')
        name_url = (
            'https://www.linkedin.com/search/results/people/?'
            + f'keywords={name_str}'
        )
        founder_info_str_list.append(f'[{name}](mailto:{name_url})')
    founder_info_str = ' · '.join(founder_info_str_list)

    startup_stage = data['startup_stage']
    funding_stage = data['funding_stage']
    details_str = ' · '.join([startup_stage, funding_stage])

    return [
        f'## {name}',
        f'*"{tagline}"*',
        f'Business Registration: **{business_registration_str}**',
        f'**{category_str}**',
        f'<img src="{img_url}" alt="{name}" style="height:100px;" />',
        f'{description}',
        f'{details_str}',
        f'{founder_info_str}',
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

    for data in data_list[:10]:
        md_lines += build_startup_summary(data)

    md_file = '/tmp/README.md'
    filex.write(md_file, '\n\n'.join(md_lines))
    log.info(f'Wrote summary to {md_file}')


if __name__ == '__main__':
    build_summary()

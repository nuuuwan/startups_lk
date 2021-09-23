import os

from utils import filex, timex

from startups_lk import startups
from startups_lk._constants import REMOTE_DATA_DIR
from startups_lk._utils import log


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
    founder_info_str_list = [f'[{url}]({url})']
    email = founder_info.get('email')
    founder_name = founder_info.get('name')
    phone = founder_info.get('phone')
    if email:
        founder_info_str_list.append(f'[{email}](mailto:{email})')
    if phone:
        founder_info_str_list.append(f'[{phone}](tel:{phone})')
    if founder_name:
        name_str = founder_name.replace(' ', '+')
        name_url = (
            'https://www.linkedin.com/search/results/people/?'
            + f'keywords={name_str}'
        )
        founder_info_str_list.append(f'[{founder_name}]({name_url})')
    founder_info_str = ' · '.join(founder_info_str_list)

    startup_stage = data['startup_stage']
    funding_stage = data['funding_stage']
    details_str = ' · '.join(
        [f'**{startup_stage}**', f'Funding **{funding_stage}**']
    )

    return [
        f'## {name}',
        f'<img src="{img_url}" alt="{name}" '
        + 'style="height:100px; text-align:left;" />',
        f'*"{tagline}"*',
        f'Business Registration: **{business_registration_str}**',
        f'**{category_str}**',
        f'{details_str}',
        f'{description}',
        f'Contact: {founder_info_str}',
    ]


def build_summary():
    data_list = startups.load()
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


if __name__ == '__main__':
    build_summary()

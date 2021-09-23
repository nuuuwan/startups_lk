from utils import filex, timex

from startups_lk._utils import log
from startups_lk.startups import load_startups


def build_startup_summary(data):
    name = data['name']
    description = data['description']
    url = data['url']
    return [
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

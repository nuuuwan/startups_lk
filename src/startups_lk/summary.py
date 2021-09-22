from utils import filex

from startups_lk._utils import log
from startups_lk.startups import load_startups


def build_summary():
    data_list = load_startups()
    md_lines = [
        '# Startups in Sri Lanka',
        'Source: [https://www.startupsl.lk](https://www.startupsl.lk)',
    ]

    for data in data_list:
        name = data['name']
        description = data['description']
        url = data['url']
        md_lines += [
            f'## {name}',
            f'{description}',
            f'[{url}]({url})',
        ]

    md_file = '/tmp/README.md'
    filex.write(md_file, '\n'.join(md_lines))
    log.info(f'Wrote summary to {md_file}')

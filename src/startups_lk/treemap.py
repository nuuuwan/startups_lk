import xml.etree.ElementTree as ET

import squarify
from utils import filex

from startups_lk._utils import log
from startups_lk.startups import load_startups

WIDTH, HEIGHT = 1600, 900


def get_cat_to_data_list():
    data_list = load_startups()
    cat_to_data_list = {}
    for data in data_list:
        for cat in data['category']:
            if cat not in cat_to_data_list:
                cat_to_data_list[cat] = []
            cat_to_data_list[cat].append(data)
            break # Only consider first cat
    return cat_to_data_list


def get_cat_to_n():
    cat_to_data_list = get_cat_to_data_list()
    cat_to_n = dict(
        sorted(
            list(
                map(
                    lambda x: [x[0], len(x[1])],
                    cat_to_data_list.items(),
                )
            ),
            key=lambda x: -x[1],
        )
    )
    return cat_to_n


def draw_treemap():
    cat_to_data_list = get_cat_to_data_list()
    cat_to_n = get_cat_to_n()
    cats, values = zip(*cat_to_n.items())

    values = squarify.normalize_sizes(values, WIDTH, HEIGHT)
    X0, Y0 = 0, 0
    square_info_list = squarify.squarify(values, X0, Y0, WIDTH, HEIGHT)

    _svg = ET.Element(
        'svg',
        {
            'xmlns': 'http://www.w3.org/2000/svg',
            'width': str(WIDTH),
            'height': str(HEIGHT),
        },
    )
    for cat, square_info in zip(cats, square_info_list):
        x = square_info['x']
        y = square_info['y']
        width = square_info['dx']
        height = square_info['dy']
        ET.SubElement(
            _svg,
            'rect',
            {
                'x': str(x),
                'y': str(y),
                'width': str(width),
                'height': str(height),
                'fill': 'white',
                'stroke': 'gray',
            },
        )

        font_size = min(height / 10, 144, 2 * width / len(cat))
        ET.SubElement(
            _svg,
            'text',
            {
                'x': str(x + width / 2),
                'y': str(y + height / 2),
                'fill': 'red',
                'text-anchor': 'middle',
                'font-family': 'Futura',
                'font-size': str(font_size),

            },
        ).text = cat

    svg_file = '/tmp/startups_lk.svg'
    filex.write(svg_file, ET.tostring(_svg).decode())
    log.info(f'Wrote SVG to {svg_file}')


if __name__ == '__main__':
    draw_treemap()

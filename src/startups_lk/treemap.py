import math
import xml.etree.ElementTree as ET

import squarify
from utils import filex

from startups_lk._utils import log
from startups_lk.startups import load_startups

WIDTH, HEIGHT = 1600, 900
BORDER_RADIUS = 24
RECT_PADDING = 24


def get_cat_to_data_list():
    data_list = load_startups()[:60]
    cat_to_data_list = {}
    for data in data_list:
        for cat in data['category']:
            if cat not in cat_to_data_list:
                cat_to_data_list[cat] = []
            cat_to_data_list[cat].append(data)
            break  # Only consider first cat
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
        x = square_info['x'] + RECT_PADDING
        y = square_info['y'] + RECT_PADDING
        width = square_info['dx'] - RECT_PADDING * 2
        height = square_info['dy'] - RECT_PADDING * 2
        ET.SubElement(
            _svg,
            'rect',
            {
                'x': str(x),
                'y': str(y),
                'width': str(width),
                'height': str(height),
                'rx': str(BORDER_RADIUS),
                'ry': str(BORDER_RADIUS),
                'fill': 'white',
                'stroke': 'gray',
            },
        )

        cat_data_list = cat_to_data_list[cat]
        n_cat = len(cat_data_list)
        header_text = f'{cat} ({n_cat})'
        font_size = min(height / 10, 144, 1.5 * width / len(header_text))
        margin_top = font_size * 1.2
        ET.SubElement(
            _svg,
            'text',
            {
                'x': str(x + width / 2),
                'y': str(y + margin_top),
                'fill': 'red',
                'text-anchor': 'middle',
                'font-family': 'Futura',
                'font-size': str(font_size),
            },
        ).text = header_text


        df = math.sqrt(width * height / n_cat)
        n_cols = math.ceil(width / df)
        n_rows = math.ceil(n_cat / n_cols)

        img_width = width / n_cols
        img_height = height / n_rows
        PADDING = max(img_width, img_height) * 0.1

        i_x, i_y = 0, 0
        for i_data, data in enumerate(cat_data_list):
            image_x = x + img_width * i_x
            image_y = y + img_height * i_y
            img = data['img']
            ET.SubElement(
                _svg,
                'image',
                {
                    'href': img,
                    'x': str(image_x + PADDING),
                    'y': str(image_y + PADDING + margin_top),
                    'width': str(img_width - PADDING * 2),
                    'height': str(img_height - PADDING * 2 - margin_top),
                    'fill': 'rgba(255, 0, 0, 0.5)'
                },
            )

            i_x += 1
            if i_x >= n_cols:
                i_x = 0
                i_y += 1

    svg_file = '/tmp/startups_lk.svg'
    filex.write(svg_file, ET.tostring(_svg).decode())
    log.info(f'Wrote SVG to {svg_file}')


if __name__ == '__main__':
    draw_treemap()

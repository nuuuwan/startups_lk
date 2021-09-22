import math
import ssl
import xml.etree.ElementTree as ET

import squarify
from utils import filex

from startups_lk._constants import (URL_DATA_SOURCE_DOMAIN, get_funding_stage,
                                    get_startup_stage)
from startups_lk._utils import log
from startups_lk.category_colors import get_category_color
from startups_lk.startups import load_startups

WIDTH, HEIGHT = 1600, 900
BORDER_RADIUS = 6
RECT_PADDING = 6
STROKE_WIDTH = 1
HEADER_HEIGHT = 72
FOOTER_HEIGHT = 72
PADDING_OUTER_X = 24
PADDING = 5
FONT_FAMILY = 'Futura'
BUILD_PNG = True


ssl._create_default_https_context = ssl._create_unverified_context


def get_cat_to_data_list(min_startup_stage_i, min_funding_stage_i):
    data_list = load_startups(min_startup_stage_i, min_funding_stage_i)
    cat_to_data_list = {}
    for data in data_list:
        for cat in data['category_list']:
            if cat not in cat_to_data_list:
                cat_to_data_list[cat] = []
            cat_to_data_list[cat].append(data)

    return cat_to_data_list


def get_cat_to_n(min_startup_stage_i, min_funding_stage_i):
    cat_to_data_list = get_cat_to_data_list(
        min_startup_stage_i, min_funding_stage_i
    )
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


def get_filter_details(min_startup_stage_i, min_funding_stage_i):
    min_startup_stage = get_startup_stage(min_startup_stage_i)
    min_funding_stage = get_funding_stage(min_funding_stage_i)
    return f'{min_startup_stage}+ & {min_funding_stage}+'


def draw_treemap(min_startup_stage_i, min_funding_stage_i):
    cat_to_data_list = get_cat_to_data_list(
        min_startup_stage_i, min_funding_stage_i
    )
    cat_to_n = get_cat_to_n(min_startup_stage_i, min_funding_stage_i)
    cats, values = zip(*cat_to_n.items())

    values = squarify.normalize_sizes(
        values,
        WIDTH - PADDING_OUTER_X * 2,
        HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT,
    )
    X0, Y0 = 0, 0
    square_info_list = squarify.squarify(
        values,
        X0,
        Y0,
        WIDTH - PADDING_OUTER_X * 2,
        HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT,
    )

    _svg = ET.Element(
        'svg',
        {
            'xmlns': 'http://www.w3.org/2000/svg',
            'width': str(WIDTH),
            'height': str(HEIGHT),
        },
    )

    ET.SubElement(
        _svg,
        'rect',
        {
            'x': str(PADDING / 2),
            'y': str(PADDING / 2),
            'width': str(WIDTH - PADDING),
            'height': str(HEIGHT - PADDING),
            'rx': str(BORDER_RADIUS),
            'ry': str(BORDER_RADIUS),
            'fill': 'black',
            'fill-opacity': str(0.05),
            'stroke': 'lightgray',
            'stroke-width': str(STROKE_WIDTH),
        },
    )

    ET.SubElement(
        _svg,
        'text',
        {
            'x': str(WIDTH / 2),
            'y': str(HEADER_HEIGHT / 2),
            'fill': 'black',
            'text-anchor': 'middle',
            'font-family': FONT_FAMILY,
            'font-size': str(35),
        },
    ).text = 'Startups in Sri Lanka'

    ET.SubElement(
        _svg,
        'text',
        {
            'x': str(WIDTH / 2),
            'y': str(HEADER_HEIGHT / 2 + 24),
            'fill': 'black',
            'text-anchor': 'middle',
            'font-family': FONT_FAMILY,
            'font-size': str(12),
        },
    ).text = get_filter_details(min_startup_stage_i, min_funding_stage_i)

    ET.SubElement(
        _svg,
        'text',
        {
            'x': str(WIDTH / 2),
            'y': str(HEIGHT - (FOOTER_HEIGHT / 2)),
            'fill': 'gray',
            'text-anchor': 'middle',
            'font-family': FONT_FAMILY,
            'font-size': str(24),
        },
    ).text = f'Data by {URL_DATA_SOURCE_DOMAIN} · Visualization by @nuuuwan'

    for cat, square_info in zip(cats, square_info_list):
        x = square_info['x'] + RECT_PADDING + PADDING_OUTER_X
        y = square_info['y'] + RECT_PADDING + HEADER_HEIGHT
        width = square_info['dx'] - RECT_PADDING * 2
        height = square_info['dy'] - RECT_PADDING * 2
        color = get_category_color(cat)
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
                'stroke': color,
                'stroke-width': str(STROKE_WIDTH),
            },
        )

        cat_data_list = cat_to_data_list[cat]
        n_cat = len(cat_data_list)
        header_text = f'{cat} ({n_cat})'.upper()
        font_size = min(height / 10, 144, 1.5 * width / len(header_text))
        margin_top = font_size * 1.2

        ET.SubElement(
            _svg,
            'text',
            {
                'x': str(x + width / 2),
                'y': str(y + margin_top),
                'fill': color,
                'text-anchor': 'middle',
                'font-family': FONT_FAMILY,
                'font-size': str(font_size),
            },
        ).text = header_text

        df = math.sqrt(width * height / n_cat)
        n_cols = math.ceil(width / df)
        n_rows = math.ceil(n_cat / n_cols)

        img_width = width / n_cols
        img_height = (height - margin_top) / n_rows

        i_x, i_y = 0, 0
        for i_data, data in enumerate(cat_data_list):
            image_x = x + img_width * i_x
            image_y = y + img_height * i_y
            image_file_only = data['image_file_only']
            img = f'/tmp/startups_lk-images/{image_file_only}'
            # img = f'http://localhost:8000/{image_file_only}'
            ET.SubElement(
                _svg,
                'image',
                {
                    'href': img,
                    'x': str(image_x + PADDING),
                    'y': str(image_y + PADDING + margin_top),
                    'width': str(img_width - PADDING * 2),
                    'height': str(img_height - PADDING * 2),
                },
            )
            i_x += 1
            if i_x >= n_cols:
                i_x = 0
                i_y += 1

    ET.SubElement(
        _svg,
        'text',
        {
            'x': str(WIDTH / 2),
            'y': str(HEIGHT / 2),
            'fill': 'black',
            'fill-opacity': str(0.05),
            'text-anchor': 'middle',
            'alignment-baseline': 'hanging',
            'font-family': FONT_FAMILY,
            'font-size': str(288),
        },
    ).text = '@nuuuwan'

    svg_file = '/tmp/startups_lk.svg'
    svg_code = ET.tostring(_svg).decode()
    filex.write(svg_file, svg_code)
    log.info(f'Wrote SVG to {svg_file}')


if __name__ == '__main__':
    draw_treemap(min_startup_stage_i=1, min_funding_stage_i=1)

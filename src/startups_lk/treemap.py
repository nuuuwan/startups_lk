import math
import os
import ssl
import time
import xml.etree.ElementTree as ET

import squarify
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import dt, filex

from startups_lk._constants import (URL_DATA_SOURCE_DOMAIN, get_funding_stage,
                                    get_startup_stage)
from startups_lk._utils import log
from startups_lk.category_colors import get_category_color
from startups_lk.startups import load_startups

WIDTH = 2000
ASPECT_RATIO = 9 / 16
HEIGHT = WIDTH * ASPECT_RATIO
BORDER_RADIUS = 6
RECT_PADDING = 9
STROKE_WIDTH = 3
HEADER_HEIGHT = 144
FOOTER_HEIGHT = 144
PADDING_OUTER_X = 48
PADDING = 1
FONT_FAMILY = 'Futura'
BUILD_PNG = False
DEFAULT_REMOTE_IMG_URL = (
    'https://www.startupsl.lk/CompanyLogos/deault-logo.jpg'
)
TIME_WAIT = 4
REMOTE_DATA_DIR = 'https://raw.githubusercontent.com/nuuuwan/startups_lk/data'
USE_REMOTE = False

ssl._create_default_https_context = ssl._create_unverified_context
OTHER_CAT_N_LIMIT = 10
OTHER_CAT_P_LIMIT = 0.1


def get_cat_to_data_list(min_startup_stage_i, min_funding_stage_i):
    data_list0 = load_startups(min_startup_stage_i, min_funding_stage_i)
    # data_list = []
    # for data in data_list0:
    #     category_key = ';'.join(data['category_list'])
    #     if 'e-commerce' not in category_key:
    #         continue
    #     data_list.append(data)
    data_list = data_list0

    n_data_list = len(data_list)
    cat_to_data_map = {}
    for data in data_list:
        startup_id = data['startup_id']
        for cat in data['category_list']:
            if cat not in cat_to_data_map:
                cat_to_data_map[cat] = {}
            cat_to_data_map[cat][startup_id] = data

    other_cats = []
    for cat, cat_data_map in cat_to_data_map.items():
        n_cat = len(cat_data_map.values())
        if (n_cat < n_data_list * OTHER_CAT_P_LIMIT) and (
            n_cat < OTHER_CAT_N_LIMIT
        ):
            other_cats.append(cat)

    cat_to_data_map = {}
    for data in data_list:
        startup_id = data['startup_id']
        for cat in data['category_list']:
            if cat in other_cats:
                cat = 'Other'
            if cat not in cat_to_data_map:
                cat_to_data_map[cat] = {}
            cat_to_data_map[cat][startup_id] = data

    cat_to_data_list = dict(
        list(
            map(
                lambda x: [x[0], list(x[1].values())],
                cat_to_data_map.items(),
            )
        )
    )
    cat_to_n = dict(
        sorted(
            list(
                map(
                    lambda x: [x[0], len(x[1])],
                    cat_to_data_list.items(),
                )
            ),
            key=lambda x: (-x[1]),
        )
    )

    return cat_to_n, cat_to_data_list, n_data_list


def draw_treemap(min_startup_stage_i, min_funding_stage_i):
    cat_to_n, cat_to_data_map, n_data_list = get_cat_to_data_list(
        min_startup_stage_i, min_funding_stage_i
    )
    if not cat_to_n:
        log.error('No data for filters.')
        return

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

    _html = ET.Element('html')
    _body = ET.SubElement(_html, 'body')
    _svg = ET.SubElement(
        _body,
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
            'fill': 'white',
            'stroke': 'white',
            'stroke-width': str(STROKE_WIDTH),
        },
    )

    ET.SubElement(
        _svg,
        'text',
        {
            'x': str(WIDTH / 2),
            'y': str(HEADER_HEIGHT - 48),
            'fill': 'black',
            'text-anchor': 'middle',
            'font-family': FONT_FAMILY,
            'font-size': str(35),
        },
    ).text = 'Startups in Sri Lanka (2021 September)'

    min_startup_stage = get_startup_stage(min_startup_stage_i)
    min_funding_stage = get_funding_stage(min_funding_stage_i)
    min_startup_stage_id = dt.to_kebab(min_startup_stage)
    min_funding_stage_id = dt.to_kebab(min_funding_stage)
    filter_details = (
        f'{n_data_list} Startups at '
        + f'{min_startup_stage}+ & {min_funding_stage}+'
    )

    ET.SubElement(
        _svg,
        'text',
        {
            'x': str(WIDTH / 2),
            'y': str(HEADER_HEIGHT - 48 + 24),
            'fill': 'black',
            'text-anchor': 'middle',
            'font-family': FONT_FAMILY,
            'font-size': str(12),
        },
    ).text = filter_details

    ET.SubElement(
        _svg,
        'text',
        {
            'x': str(WIDTH / 2),
            'y': str(HEIGHT - FOOTER_HEIGHT + 48),
            'fill': 'gray',
            'text-anchor': 'middle',
            'font-family': FONT_FAMILY,
            'font-size': str(18),
        },
    ).text = f'Data by {URL_DATA_SOURCE_DOMAIN} · Visualization by @nuuuwan'

    ET.SubElement(
        _svg,
        'text',
        {
            'x': str(WIDTH / 2),
            'y': str(HEIGHT - FOOTER_HEIGHT + 18),
            'fill': 'gray',
            'text-anchor': 'middle',
            'font-family': FONT_FAMILY,
            'font-size': str(12),
        },
    ).text = (
        'This listing might not be exhaustive '
        + '· Categories, startup status and funding status'
        + ' are self-reported by the startups '
        + '· Each startup might be categorized into multiple categories'
    )

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

        cat_data_list = cat_to_data_map[cat]
        n_cat = len(cat_data_list)
        header_text = f'{cat} ({n_cat})'
        font_size = min(height / 10, 72, 1 * width / len(header_text))
        margin_top = font_size * 1.2

        BACKGROUND_RECT_P = 0.1
        ET.SubElement(
            _svg,
            'rect',
            {
                'x': str(x + width * BACKGROUND_RECT_P),
                'y': str(y - margin_top / 2),
                'rx': str(BORDER_RADIUS),
                'ry': str(BORDER_RADIUS),
                'width': str(width * (1 - BACKGROUND_RECT_P * 2)),
                'height': str(margin_top),
                'fill': 'white',
            },
        )

        ET.SubElement(
            _svg,
            'text',
            {
                'x': str(x + width / 2),
                'y': str(y + margin_top / 4),
                'fill': color,
                'text-anchor': 'middle',
                'font-family': FONT_FAMILY,
                'font-size': str(font_size),
            },
        ).text = header_text

        df = math.sqrt(width * height / n_cat)
        if width > height:
            n_cols = math.ceil(width / df)
            n_rows = math.ceil(n_cat / n_cols)
        else:
            n_rows = math.ceil(height / df)
            n_cols = math.ceil(n_cat / n_rows)

        img_width = width / n_cols
        img_height = (height - margin_top) / n_rows

        i_x, i_y = 0, 0
        for i_data, data in enumerate(cat_data_list):
            image_x = x + img_width * i_x
            image_y = y + img_height * i_y + margin_top / 2
            image_file_only = data['image_file_only']
            if USE_REMOTE:
                img = f'{REMOTE_DATA_DIR}/startups_lk-images/{image_file_only}'
            else:
                img = f'/tmp/startups_lk-images/{image_file_only}'

            ET.SubElement(
                _svg,
                'image',
                {
                    'href': img,
                    'x': str(image_x + PADDING),
                    'y': str(image_y + PADDING),
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

    svg_file_only = (
        'startups_lk.startupscape.'
        + f'{min_startup_stage_id}.{min_funding_stage_id}.svg'
    )
    svg_file = f'/tmp/{svg_file_only}'

    svg_code = ET.tostring(_html).decode()
    filex.write(svg_file, svg_code)
    log.info(f'Wrote SVG to {svg_file}')

    os.system(f'open -a firefox {svg_file}')

    if BUILD_PNG:
        png_file = svg_file.replace('.svg', '.png')
        url = f'file:///private/tmp/{svg_file_only}'
        options = Options()
        options.headless = False

        driver = webdriver.Firefox(options=options)
        log.info(f'Opening {url}...')
        driver.get(url)
        driver.maximize_window()
        time.sleep(TIME_WAIT)

        driver.get_screenshot_as_file(png_file)
        driver.quit()

        # im = Image.open(png_file)
        # im_cropped = im.crop((0, 0, WIDTH * P, HEIGHT * P))
        # im_cropped.save(png_file)


if __name__ == '__main__':
    draw_treemap(min_startup_stage_i=1, min_funding_stage_i=1)

    # for min_startup_stage_i in range(1, 7):
    #     draw_treemap(
    #         min_startup_stage_i=min_startup_stage_i, min_funding_stage_i=1
    #     )
    #
    # for min_funding_stage_i in range(1, 9):
    #     draw_treemap(
    #         min_startup_stage_i=1, min_funding_stage_i=min_funding_stage_i
    #     )

from startups_lk._constants import CATEGORY_TO_COLOR


def get_category_color(cat):
    if cat not in CATEGORY_TO_COLOR:
        color = 'gray'
        CATEGORY_TO_COLOR[cat] = color
        print(CATEGORY_TO_COLOR)

    return CATEGORY_TO_COLOR[cat]

import squarify

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
    cat_to_n = get_cat_to_n()
    values = list(cat_to_n.values())

    values = squarify.normalize_sizes(values, WIDTH, HEIGHT)
    X0, Y0 = 0, 0
    rects = squarify.squarify(values, X0, Y0, WIDTH, HEIGHT)
    print(rects)


if __name__ == '__main__':
    draw_treemap()

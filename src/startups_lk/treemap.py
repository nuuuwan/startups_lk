# import squarify
#
# x = 0.
# y = 0.
# width = 700.
# height = 433.
#
# values = [500, 433, 78, 25, 25, 7]
# values.sort(reverse=True)
#
#
# values = squarify.normalize_sizes(values, width, height)
#
# rects = squarify.squarify(values, x, y, width, height)
#
# print(rects)
#
#

from startups_lk.startups import load_startups


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


if __name__ == '__main__':
    # draw_treemap()

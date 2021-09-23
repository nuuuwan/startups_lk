from startups_lk.scrape import download_html, download_images, parse_and_dump
from startups_lk.summary import build_summary
from startups_lk.treemap import draw_treemap

if __name__ == '__main__':
    download_html()
    parse_and_dump()
    download_images()
    build_summary()
    draw_treemap(min_startup_stage_i=1, min_funding_stage_i=1)

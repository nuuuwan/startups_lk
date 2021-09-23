from startups_lk.startups import download_html, download_images, parse_and_dump
from startups_lk.summary import build_summary

if __name__ == '__main__':
    download_html()
    parse_and_dump()
    download_images()
    build_summary()

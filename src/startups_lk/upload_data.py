from startups.summary import build_summary

from startups_lk.startups import scrape_and_dump

if __name__ == '__main__':
    scrape_and_dump()
    build_summary()

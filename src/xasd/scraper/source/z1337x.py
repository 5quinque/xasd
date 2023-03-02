from xasd.scraper.source import Source


class Z1337x(Source):
    source_name = "1337x"
    base_url = "https://1337x.to/cat/Music/1/"
    title_link_selector = ".coll-1.name a:last-child"
    next_page_selector = ".pagination  li:nth-child(8) > a"

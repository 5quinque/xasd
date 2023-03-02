from xasd.scraper.source import Source


class Demonoid(Source):
    source_name = "Demonoid"
    base_url = "https://demonoid.is/files/?to=0&uid=0&category=9&subcategory=0&language=0&seeded=2&quality=0&external=2&query=&sort=&page=1"
    title_link_selector = None
    next_page_selector = (
        ".ctable_content_no_pad > table:nth-child(1) tr:nth-child(2)  a"
    )

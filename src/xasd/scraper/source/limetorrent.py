from xasd.scraper.source import Source


class LimeTorrent(Source):
    source_name = "LimeTorrent"
    base_url = "https://limetorrents.unblockit.bio/browse-torrents/Music/date/1/"
    title_link_selector = ".tt-name a:last-child"
    next_page_selector = "#next"

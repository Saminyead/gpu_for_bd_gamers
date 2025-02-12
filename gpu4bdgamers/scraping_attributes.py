import dataclasses

@dataclasses.dataclass
class ScrapingAttributes:
    first_page_url: str
    card_css_sel: str
    gpu_name_css_sel: str
    gpu_price_css_sel: str
    retailer_name: str
    next_page_url_tag_str: str|None = None
    next_page_url_css_sel: str|None = None

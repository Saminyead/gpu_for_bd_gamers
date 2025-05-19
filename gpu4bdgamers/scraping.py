import dataclasses
import pydantic
import re

import requests

from bs4 import BeautifulSoup
from bs4.element import Tag


def get_page_soup_list(
    first_page_url: str, next_page_url_sel: str | None = None
) -> list[BeautifulSoup]:
    """Starting from the first page, this function will navigate through
    all the GPU listing pages of a retailer website by finding the next
    page URL (through the next_page_url_sel selector) and return a list of
    BeautifulSoup objects of the contents of the pages."""
    soup_list = []
    next_page_url = first_page_url
    i = 0  # to check if next_page_url_elem exists in the first page
    # if next_page_url_elem does not exist in the latter pages, it means
    # we will have reached the last page
    while next_page_url:
        page_content = requests.get(next_page_url).content
        soup = BeautifulSoup(page_content, features="html.parser")
        soup_list.append(soup)
        if not next_page_url_sel:
            break
        next_page_url_elem = soup.select_one(next_page_url_sel)
        if i == 0 and not next_page_url_elem:
            raise ElementDoesNotExistError(
                f"Unable to find next page element with selector {next_page_url_sel}"
            )
        if not next_page_url_elem:  # for when we reach the last page
            break
        next_page_url = next_page_url_elem["href"]
        i += 1
    return soup_list


def get_card_list(
    soup_list: list[BeautifulSoup],
    card_css_sel: str,
) -> list[Tag]:
    """A card is a section of the page that contains all the information
    regarding a listed GPU."""
    card_list = []
    for soup in soup_list:
        card_list_in_soup = soup.select(card_css_sel)
        if not card_list_in_soup:
            raise ElementDoesNotExistError(
                f"""Unable to find any card with selector {card_css_sel} in one
                of the pages."""
            )
        card_list.extend(card_list_in_soup)
    return card_list


@dataclasses.dataclass
class GpuListingAttrs:
    """CSS selectors of the GPU name, price, and retail url."""

    gpu_name_css_sel: str
    gpu_price_css_sel: str
    retail_url_css_sel: str
    retailer_name: str

    def get_gpu_listing_data(self, card_list: list[Tag]) -> list["GpuListingData"]:
        gpu_listing_list = []
        for card in card_list:
            gpu_name_tag = card.select_one(self.gpu_name_css_sel)
            gpu_price_tag = card.select_one(self.gpu_price_css_sel)
            retail_url_tag = card.select_one(self.retail_url_css_sel)
            if not gpu_name_tag or not gpu_price_tag or not retail_url_tag:
                raise ElementDoesNotExistError(
                    f"Either gpu name, price or retail url does not exist for {self.retailer_name}."
                )
            gpu_name = gpu_name_tag.text
            gpu_price_str = gpu_price_tag.text
            gpu_price = get_price_int_regex(gpu_price_str)
            retail_url = retail_url_tag["href"]
            gpu_listing = self.handle_pydantic_validation_error_gpu_listing(
                gpu_name=gpu_name,
                gpu_price=gpu_price,
                retail_url=retail_url,
                retailer_name=self.retailer_name,
            )
            gpu_listing_list.append(gpu_listing)
        return gpu_listing_list

    def handle_pydantic_validation_error_gpu_listing(
        self, gpu_name: str, gpu_price: str, retail_url: str, retailer_name: str
    ):
        try:
            return GpuListingData(
                gpu_name=gpu_name,
                gpu_price=gpu_price,
                retail_url=retail_url,
                retailer_name=retailer_name,
            )
        except pydantic.ValidationError as e:
            error_details_dict_list = e.errors()
            for error_details_dict in error_details_dict_list:
                raise Exception(
                    f"""While getting GPU listing attribute of {self.retailer_name}
                    we got:\n{error_details_dict['loc']=}
                    expected type of{error_details_dict['loc']} should be 
                    {error_details_dict['type']}"""
                ) from e


class GpuListingData(pydantic.BaseModel):
    gpu_name: str
    gpu_price: int
    retail_url: pydantic.AnyUrl
    retailer_name: str


class ElementDoesNotExistError(Exception):
    pass


# probably best to move to another module
def get_price_int_regex(price_str: str) -> str:
    """Gets the price in a format which can be easily converted to an int.
    e.g. 28,000 will be converted to 28000."""
    nums = re.findall(pattern=r"\d+", string=price_str)
    nums_combined = "".join(nums)
    return nums_combined


def handle_pydantic_validation_error_gpu_listing(
    gpu_name: str, gpu_price: str, retail_url: str, retailer_name: str
):
    try:
        GpuListingData(
            gpu_name=gpu_name,
            gpu_price=gpu_price,
            retail_url=retail_url,
            retailer_name=retailer_name,
        )
    except pydantic.ValidationError as e:
        error_details_dict = e.errors()[0]
        raise Exception(
            f"""{error_details_dict['loc']=}
            expected type of{error_details_dict['loc']} should be 
            {error_details_dict['type']}"""
        ) from e

import pytest
import pandas as pd

from bs4 import BeautifulSoup, Tag

import subprocess
import time
from typing import Generator, Any

MASTER_DF_CSV_FILE = "master_df.csv"


@pytest.fixture
def radeon_gpu_list() -> list[str]:
    return ["RX 580", "RX 6900 XT", "RX 7600", "RX 7600 XT"]


@pytest.fixture
def geforce_gpu_list() -> list[str]:
    return [
        "GTX 1650",
        "RTX 2060",
        "RTX 2080 Super",
        "RTX 3070",
        "RTX 4060",
        "RTX 4060 Ti",
    ]


@pytest.fixture
def intel_gpu_list() -> list[str]:
    return ["Arc A580", "Arc A750", "Arc A770"]


@pytest.fixture
def master_df_test(filename: str = MASTER_DF_CSV_FILE) -> pd.DataFrame:
    return pd.read_csv(filename)


@pytest.fixture
def gpu_unit_index() -> dict[str, dict[str, list[int]]]:
    return {
        "Radeon": {
            "Radeon RX 580": [0],
            "Radeon RX 7600": [1],
            "Radeon RX 7600 XT": [2],
            "Radeon RX 6900 XT": [3, 4],
        },
        "Geforce": {
            "Geforce GTX 1650": [5, 6],
            "Geforce RTX 2060": [7],
            "Geforce RTX 2080 Super": [8],
            "Geforce RTX 4060": [9, 10],
            "Geforce RTX 4060 Ti": [11, 12],
            "Geforce RTX 3070": [13],
        },
        "Intel": {
            "Intel Arc A580": [14],
            "Intel Arc A750": [15, 16],
            "Intel Arc A770": [17],
        },
    }


@pytest.fixture
def mock_server(
    html_pages_dir: str = "./mock_pages/", port="5000"
) -> Generator[None, Any, Any]:
    proc = subprocess.Popen(
        ["python3", "-m", "http.server", "-d", html_pages_dir, port]
    )
    time.sleep(1)
    yield
    proc.kill()


@pytest.fixture(scope="function")
def no_next_page_url() -> str:
    return "http://127.0.0.1:5000/no_next_page.html"


@pytest.fixture
def missing_card_soup_list():
    return [
        BeautifulSoup(
            '<section><div class = "card">This is a card</div></section>',
            features="html.parser",
        ),
        BeautifulSoup(
            "<section><div>This is not a card</div></section>", features="html.parser"
        ),
    ]


@pytest.fixture
def missing_gpu_name_in_card():
    soup = """
            <div class = "card">
                    <li class = "gpu-name">Asus ROG Geforce RTX 3080</li>
                    <li class = "gpu-price">86000</li>
                    <li class = "product-url"><a href="https://goslinghardware.com/product/3361">Buy Now</a></li>
            </div>
            <div class = "card">
                    <li class = "gpu-price">68000</li>
                    <li class = "product-url"><a href="https://jerryshardware.com/product/3690">Buy Now</a></li>,
            </div>
            <div class = "card">
                <li class = "gpu-name">Zotac Geforce RTX 4060</li>
                <li class = "gpu-price">48000</li>
                <li class = "product-url"><a href="https://powerpc.com/product/3301">Buy Now</a></li>
            </div>"""
    card_list = BeautifulSoup(soup, features="html.parser").select("div.card")
    return card_list


@pytest.fixture
def missing_gpu_price_in_card():
    soup = """
            <div class = "card">
                    <li class = "gpu-name">Asus ROG Geforce RTX 3080</li>
                    <li class = "gpu-price">86000</li>
                    <li class = "product-url"><a href="https://goslinghardware.com/product/3361">Buy Now</a></li>
            </div>
            <div class = "card">
                    <li class = "gpu-name">MSI Radeon RX 6700 XT</li>
                    <li class = "gpu-price">68000</li>
                    <li class = "product-url"><a href="https://jerryshardware.com/product/3690">Buy Now</a></li>,
            </div>
            <div class = "card">
                <li class = "gpu-name">Zotac Geforce RTX 4060</li>
                <li class = "product-url"><a href="https://powerpc.com/product/3301">Buy Now</a></li>
            </div>"""
    card_list = BeautifulSoup(soup, features="html.parser").select("div.card")
    return card_list


@pytest.fixture
def missing_retail_url_in_card():
    soup = """
            <div class = "card">
                    <li class = "gpu-name">Asus ROG Geforce RTX 3080</li>
                    <li class = "gpu-price">86000</li>
            </div>
            <div class = "card">
                    <li class = "gpu-name">MSI Radeon RX 6700 XT</li>
                    <li class = "gpu-price">68000</li>
                    <li class = "product-url"><a href="https://jerryshardware.com/product/3690">Buy Now</a></li>,
            </div>
            <div class = "card">
                <li class = "gpu-name">Zotac Geforce RTX 4060</li>
                <li class = "gpu-price">48000</li>
                <li class = "product-url"><a href="https://powerpc.com/product/3301">Buy Now</a></li>
            </div>"""
    card_list = BeautifulSoup(soup, features="html.parser").select("div.card")
    return card_list


@pytest.fixture
def missing_multipe_in_card():
    soup = """
            <div class = "card">
                    <li class = "gpu-name">Asus ROG Geforce RTX 3080</li>
                    <li class = "gpu-price">86000</li>
            </div>
            <div class = "card">
                    <li class = "gpu-name">MSI Radeon RX 6700 XT</li>
                    <li class = "gpu-price"></li>
                    <li class = "product-url"><a href="https://jerryshardware.com/product/3690">Buy Now</a></li>,
            </div>
            <div class = "card">
                <li class = "gpu-name">Zotac Geforce RTX 4060</li>
                <li class = "gpu-price">48000</li>
                <li class = "product-url"><a href="https://powerpc.com/product/3301">Buy Now</a></li>
            </div>"""
    card_list = BeautifulSoup(soup, features="html.parser").select("div.card")
    return card_list

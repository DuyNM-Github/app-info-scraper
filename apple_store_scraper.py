from flask import Blueprint, request, jsonify
from app_store_scraper import AppStore

from bs4 import BeautifulSoup
import requests
import re

astore_scraper = Blueprint("apple_store_scraper", __name__)


@astore_scraper.route("/query_app_name", methods=['POST'])
def get_app_data_by_name():
    request_data = request.get_json()
    app_name = request_data['app_name']

    app_data = AppStore(country="vn", app_name=app_name)

    return serve_and_scrape(app_data.app_id, app_name)


@astore_scraper.route("/query_app_id", methods=['POST'])
def get_app_data_by_id():
    request_data = request.get_json()
    app_name = request_data['app_name']

    app_data = AppStore(country="vn", app_name=app_name)

    return serve_and_scrape(app_data.app_id)


def serve_and_scrape(app_id: str, app_name: str = None):
    app_store_url = f"https://apps.apple.com/vn/app/apple-store/id{app_id}?l=en"

    store_page = requests.get(app_store_url)
    bs = BeautifulSoup(store_page.content, "lxml")

    title_elems = bs.select("h1.app-header__title")
    app_data = dict()
    app_data["store"] = "App Store"
    for elem in title_elems:
        app_data["app_name"] = (elem.get_text().strip().split("\n")[0])

    if app_name is not None and app_name.lower() not in app_data["app_name"].lower():
        return {"message": "App not found"}, 400

    information_elems = bs.select("dl.information-list > div")
    print(len(information_elems))
    for elem in information_elems:
        dt_elem = elem.find("dt").get_text().strip().replace("\n", "")
        dt_elem = re.sub(r'\s+', ' ', dt_elem)
        dd_elem = elem.find("dd").get_text().strip().replace("\n", "")
        dd_elem = re.sub(r'\s+', ' ', dd_elem)
        app_data[dt_elem.lower().replace(" ", "_")] = dd_elem

    return app_data

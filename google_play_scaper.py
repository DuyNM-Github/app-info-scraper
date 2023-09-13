from flask import Blueprint, request
from google_play_scraper import app as gp_scraper, search as gp_search

gplay_scraper = Blueprint("google_play_scraper", __name__)


@gplay_scraper.route("/query_package_name", methods=["POST"])
def query_using_package_name():
    request_data = request.get_json()
    package_name = request_data['package_name']

    result = gp_scraper(
        package_name,
        lang='en',
        country='vn'
    )

    if result is None or len(result.keys()) == 0:
        return {"message": "App not found"}, 400

    app_data = dict()
    app_data["store"] = "Google Play"
    app_data["app_name"] = result['title']
    app_data["in-app_purchases"] = result['inAppProductPrice']
    app_data["price"] = result['price']
    app_data["age_rating"] = " ".join([result['contentRating'], result["contentRatingDescription"]])
    app_data["copyright"] = result['developer']
    app_data["compatibility"] = None
    app_data["language"] = None
    app_data["provider"] = result['developer']
    app_data["size"] = None
    app_data["category"] = str(result["genreId"]).replace("_", " ").capitalize()

    return app_data

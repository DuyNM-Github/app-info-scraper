from flask import Flask, request, jsonify

from google_play_scaper import gplay_scraper
from apple_store_scraper import astore_scraper


app = Flask(__name__)
app.register_blueprint(gplay_scraper, url_prefix='/gp')
app.register_blueprint(astore_scraper, url_prefix="/as")






import random
import string

from faker import Faker
from flask import Flask, jsonify, Response, abort
import pycountry

fake = Faker(['it_IT', 'en_US', 'ja_JP', 'pl_PL'])
app = Flask(__name__)


def generate_random_data_record() -> dict:
    first_name = fake.first_name()
    last_name = fake.last_name()
    country_code = fake.country_code()
    latitude, longitude = None, None

    latlong = fake.local_latlng(country_code=country_code, coords_only=True)
    if latlong is not None:
        latitude, longitude = latlong

    country = None
    try:
        country = pycountry.countries.get(alpha_2=country_code).name
    except Exception:
        pass

    record = {
        "_type": "Position",
        "_id": random.randint(0, 100000),
        "key": "".join([random.choice(string.ascii_lowercase) for _ in range(10)]),
        "name": first_name,
        "fullName": f"{first_name} {last_name}",
        "iata_airport_code": "".join([random.choice(string.ascii_uppercase) for _ in range(3)]),
        "type": "location",
        "country": country,
        "geo_position": {
            "latitude": latitude,
            "longitude": longitude
        },
        "location_id": random.randint(0, 100000),
        "inEurope": random.choice([True, False]),
        "countryCode": country_code,
        "coreCountry": random.choice([True, False]),
        "distance": random.randint(0, 100000)
    }

    record_with_nones = {}
    for key, value in record.items():
        if random.random() < 0.2:
            record_with_nones[key] = None
            continue

        record_with_nones[key] = value

    return record_with_nones


@app.route('/generate/json/<int:size>', methods=['GET'])
def generate_endpoint(size: int) -> Response:
    if size > 1000:
        abort(Response("Size too high (>1000)", status=418))
    records = [generate_random_data_record() for _ in range(size)]
    return jsonify(records)


app.run(host="0.0.0.0", debug=True)

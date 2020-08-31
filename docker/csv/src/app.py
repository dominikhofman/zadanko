import os
from typing import List, Optional
import csv
import io

from flask import Flask, jsonify, Response
from flask import request
import requests

app = Flask(__name__)


def get_data_records(size: int = 1) -> List[dict]:
    r = requests.get(
        f"http://{os.environ['RANDOM_GENERATOR_HOST']}:{os.environ['RANDOM_GENERATOR_PORT']}/generate/json/{size}")
    r.raise_for_status()
    return r.json()


def extract_field(data: dict, path: List[str]) -> Optional[str]:
    if isinstance(path, str):
        return data[path]

    try:
        res = data
        for key in path:
            res = res[key]
    except Exception:
        return None

    return res


def convert_to_csv(data: List[dict], fields: List[str]) -> str:
    output = io.StringIO()
    spamwriter = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    for record in data:
        spamwriter.writerow([extract_field(record, field) for field in fields])
    return output.getvalue()


@app.route('/predefined/csv/<int:size>', methods=['GET'])
def predefined_endpoint(size: int) -> Response:
    data = get_data_records(size)
    response = convert_to_csv(data, ["type", "_id", "name", "type", [
        "geo_position", "latitude"], ["geo_position", "longitude"]])

    return Response(response, mimetype='text/csv')


@app.route('/custom/csv/<int:size>', methods=['GET'])
def custom_endpoint(size: int) -> Response:
    data = get_data_records(size)
    fields = [path.split(":") for path in request.args.getlist('fields')]
    response = convert_to_csv(data, fields)

    return Response(response, mimetype='text/csv')


app.run(host="0.0.0.0", port=5001, debug=True)

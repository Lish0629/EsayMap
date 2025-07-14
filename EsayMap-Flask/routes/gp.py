from flask import Blueprint, request, jsonify
from services.geo_tools import buffer_geojson, intersect_geojson

gp_bp = Blueprint('gp', __name__)

@gp_bp.route('/buffer', methods=['POST'])
def handle_buffer():
    data = request.get_json()
    geojson = data.get('geojson')
    radius = data.get('radius', 1000)

    result = buffer_geojson(geojson, radius)
    return jsonify(result)


@gp_bp.route('/intersect', methods=['POST'])
def handle_intersect():
    data = request.get_json()
    geo1 = data.get('geojson1')
    geo2 = data.get('geojson2')

    result = intersect_geojson(geo1, geo2)
    return jsonify(result)

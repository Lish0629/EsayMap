from flask import Blueprint, request, jsonify
from services.llm_agent import call_llm
from utils.parser import parse_response_to_instruction

infer_bp = Blueprint('infer', __name__)

@infer_bp.route('', methods=['POST'])
def handle_infer():
    data = request.get_json()
    instruction = data.get('instruction')
    geojson = data.get('geojson')

    if not instruction or not geojson:
        return jsonify({'error': 'Missing instruction or geojson'}), 400

    llm_response = call_llm(instruction)
    parsed = parse_response_to_instruction(llm_response)

    # 返回结构，如 {"endpoint": "/gp/buffer", "params": {"radius": 1000}}
    return jsonify(parsed)

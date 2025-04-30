import logging
import os
import json
import functions_framework
from flask import jsonify, make_response, request
from utils.supporting_functions import stock_data_validation, data_transformation, simulate_db_save

logger = logging.getLogger('stock_purchase_order')

logger.setLevel(logging.INFO)
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    ))
    logger.addHandler(h)


@functions_framework.http
def stock_purchase_order(request):
    logger.info("Received %s %s", request.method, request.path)
    if request.method != "POST":
        logger.warning("Only POST allowed")
        return make_response(jsonify({"error": "Use POST"}), 405)
    
    data = request.get_json(silent=True)
    logger.info(data)

    if not data:
        logger.error('No JSON format')
        return make_response(jsonify({"error": "Invalid JSON"}), 400)
    
    # 1 Run data validations
    try:
        stock_data_validation(data)       
    except:
        logger.error('Data validation step not passed, please review input')
        return make_response(jsonify({"error": "Invalid JSON"}), 400)
    
    # 2 Transform Data
    transofmed_data = data_transformation(data)
    transofmed_data['status'] = 'Processed'
    transofmed_data['message'] = 'Data processed correcly, thanks for choosing us'
    # 3 Simluate data load to a Data base
    simulate_db_save(data)
    return make_response(jsonify(transofmed_data), 200)
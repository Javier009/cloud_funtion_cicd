from typing import Dict, Any, List
import uuid
from datetime import datetime
import logging

logger = logging.getLogger('order_utils')

# Validation
def stock_data_validation(data: Dict[str,Any]):
    required_fields = ['symbol',
                       'price',
                       'position',
                       'broker',
                       'purchase_country'
                       ]
    
    missing_fields = [f for f in required_fields  if f not in data]
    if len(missing_fields)>0:
        raise ValueError(f'Missing fields: {missing_fields}')
    
    # Review Symbol
    symbol = data['symbol']
    if not isinstance(symbol, str) or symbol == '':
        raise ValueError('Not correct symbol format provided')
    # Review price
    price = data['price']
    if not isinstance(price, (int,float)):
        raise ValueError('Not correct price format provided')
    position = data['position']
    if not isinstance(position, dict):
        raise ValueError('Not Position should be in the format of dict')
    else:
        position_options = ['Long', 'Short']
        missing_possition_keys = [p for p in position_options if p not in position]
        if len(missing_possition_keys)>0:
            raise ValueError('Postion dict should have Long and short values, missing values: {missing_possition_keys}')
        else:
            not_bool = [v for v in position.values() if not isinstance(v, bool)]
            if len(not_bool)>0:
                 raise ValueError('Postion dict values should be Boolean and at least one is not')
    
    purchase_country = data['purchase_country']
    if not isinstance(purchase_country, str) or purchase_country == '':
        raise ValueError('Not correct symbol format provided')
    
    return True

def data_transformation(data: Dict[str,Any]) -> Dict[str,Any]:
    data['processing_id'] = uuid.uuid4().hex
    data['opertion_time'] =  datetime.utcnow().isoformat() + "Z"
    logger.info('Data tranformation perfromed succesfuly')
    return data


def simulate_db_save(data: Dict[str, Any]) -> bool:
    logger.info("Simulating DB save for order %s", data["order_id"])
    return True    
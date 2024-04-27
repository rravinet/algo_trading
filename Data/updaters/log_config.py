import os
import logging

def setup_logging():
    
    root = os.path.dirname(os.path.abspath(__file__))

    logs_path = os.path.join(root, 'logs')
    os.makedirs(logs_path, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(logs_path, 'algo_trading.log'),
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s - %(lineno)d]'
    )

    sqlalchemy_engine_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_engine_logger.setLevel(logging.WARNING)




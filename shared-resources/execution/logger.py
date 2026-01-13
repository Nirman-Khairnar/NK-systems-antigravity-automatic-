import logging
import os
from datetime import datetime

class CentralLogger:
    def __init__(self, source_department, script_name):
        self.source_department = source_department
        self.script_name = script_name
        
        # Ensure logs directory exists (relative to workspace root)
        # Assuming script is running from a subdirectory, we look for root 'logs'
        # Adjust base_path as needed based on execution context
        self.log_dir = os.path.abspath(os.path.join(os.getcwd(), 'logs'))
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        self.log_file = os.path.join(self.log_dir, 'central_activity.log')
        
        self.logger = logging.getLogger(f"{source_department}.{script_name}")
        self.logger.setLevel(logging.INFO)
        
        # File Handler
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        self.logger.addHandler(fh)

    def log(self, message, level="INFO"):
        if level.upper() == "INFO":
            self.logger.info(message)
        elif level.upper() == "ERROR":
            self.logger.error(message)
        elif level.upper() == "WARNING":
            self.logger.warning(message)
        else:
            self.logger.info(message)

# Usage Example:
# logger = CentralLogger("sales-team", "close_deal_script")
# logger.log("Deal closed successfully")

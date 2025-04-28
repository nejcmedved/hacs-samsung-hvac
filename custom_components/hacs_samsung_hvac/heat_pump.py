import threading
import time
import logging

_LOGGER = logging.getLogger(__name__)

class HeatPump(threading.Thread):
    def __init__(self, ip: str, port:int):
        super().__init__()
        self.ip = ip
        self.port = port
        self._is_running = False
        self.daemon = True
        self.start()    
            
    def run(self):
        self._is_running = True
        # Simulate some work being done in the thread
        while self._is_running:
            _LOGGER.info(f"HeatPump running on {self.ip}:{self.port}")
            time.sleep(1)
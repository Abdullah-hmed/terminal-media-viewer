import time
import itertools
import threading

class Spinner:
    def __init__(self):
        self._running = False
        self._thread = None
        
    def spinner(self):
        spinner_values = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
                
        for face in itertools.cycle(spinner_values):
            if not self._running:
                break
            print(f"\r{face} ", flush=True, end="")
            time.sleep(0.05)
        print("\r", end="")
            
    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self.spinner, daemon=True)
        self._thread.start()
        
    def stop(self):
        if self._running:
            self._running = False
            self._thread.join()
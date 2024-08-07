import os, signal, psutil, sys

def kill_browser_processes(browser_name, list_only=False):
    for process in psutil.process_iter(['pid', 'name']):
        try:
            if browser_name.lower() in process.info['name'].lower():
                if list_only:
                    print(f"Found {process.info['name']} with PID {process.info['pid']}")
                else:
                    print(f"Killing {process.info['name']} with PID {process.info['pid']}")
                    os.kill(process.info['pid'], signal.SIGTERM)
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            pass

if __name__ == "__main__":
    list_only = "-a" in sys.argv
    kill_browser_processes("msedge", list_only)

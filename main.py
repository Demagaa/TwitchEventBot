import subprocess
import threading

from flask import Flask

app = Flask(__name__)


def run_skript(script_name, port=None):
    command = f"python {script_name}"
    if port is not None:
        command += f" --port {port}"

    subprocess.run(command, shell=True)


if __name__ == '__main__':
    processes = []

    # Start separate processes for each script
    thread1 = threading.Thread(target=run_skript, args=("bot.py",))
    thread2 = threading.Thread(target=run_skript, args=("subscribers_listener.py", 8082))
    thread3 = threading.Thread(target=run_skript, args=("twitch_listener.py", 443))

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

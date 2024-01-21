import subprocess
import threading
import ngrok_run
import configparser
from flask import Flask

configparser = configparser.ConfigParser()
configparser.read('config.ini')
auth_token = configparser.get('Keys', 'NGROK_AUTH_TOKEN')
ngrok_command = configparser.get('Keys', 'NGROK_COMM')

app = Flask(__name__)


def run_skript(script_name, port=None):
    command = f"python {script_name}"
    if port is not None:
        command += f" --port {port}"

    subprocess.run(command, shell=True)


if __name__ == '__main__':
    processes = []

    command = f"install_windows.bat"
    subprocess.run(command, shell=True)

    # Start separate processes for each script
    ngrok_run.run_ngrok(auth_token, ngrok_command)
    thread1 = threading.Thread(target=run_skript, args=("bot.py",))
    thread2 = threading.Thread(target=run_skript, args=("twitch_listener.py", 443))

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()

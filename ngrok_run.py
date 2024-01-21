import subprocess
import configparser

def run_ngrok(auth_token, command):
    ngrok_path = r'ngrok.exe'  # Replace with the actual path to ngrok.exe

    # Build the command to run ngrok in shadow mode
    ngrok_command = f'{ngrok_path} authtoken {auth_token} && start /b ngrok {command}'

    # Run the ngrok command
    subprocess.run(ngrok_command, shell=True)

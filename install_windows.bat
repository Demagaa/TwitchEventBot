@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

choco install python -y

SET "PATH=%PATH%;C:\ProgramData\chocolatey\lib\python3\tools;%ALLUSERSPROFILE%\chocolatey\bin"

"C:\Python312\python.exe" -m ensurepip --default-pip
"C:\Python312\python.exe" -m pip install --upgrade pip
"C:\Python312\python.exe" -m pip install -r requirements.txt

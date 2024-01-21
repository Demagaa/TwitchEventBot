Start-Process -Wait -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -ArgumentList "-NoProfile -InputFormat None -ExecutionPolicy Bypass -Command ""[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"" && SET ""PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin""" -Verb RunAs


choco install python -y

python -m ensurepip --default-pip
python -m pip install --upgrade pip
pip install -r requirements.txt

choco install doxygen -y

@echo off
python -m PyInstaller --runtime-tmpdir C:\Windows\Temp\WindowsUpdateCache --onefile --console --name server.exe portest.py
python -m PyInstaller --runtime-tmpdir C:\Windows\Temp\WindowsUpdateCache --onefile --console --name client.exe client.py
echo "Done!"
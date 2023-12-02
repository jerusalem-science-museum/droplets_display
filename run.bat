@echo off
pip install --upgrade --user numpy matplotlib midvoxio
python "%~dp0\src\droplets_simulator.py" %*

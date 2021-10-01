#!/bin/sh
pip3 install -r requirements.txt
sudo apt install mosquitto mosquitto-clients
tar -xvf model.tar.gz
sudo systemctl enable mosquitto
sudo systemctl status mosquitto > mosquitto_startup.log
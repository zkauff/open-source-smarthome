# open-source-smarthome by Zachary Kauffman / ztk@iastate.edu

## Overview

Amazon Alexa, Google Home, and the wide array of similar products made by the tech giants can make many aspects of our lives more convenient, but at what cost? This project seeks to create an open-source assistant that users can build upon, knowing that they are the only person with access to their data.

The core code provided here gives a general framework that is light-weight and easy to modify.

## Installation

```language=bash
git clone git@github.com:zkauff/open-source-smarthome.git
pip install -r requirements.txt
```

## Adding Modules

Add a new yaml file under `devices/`. The general structure is quite simple. To keep the core library light weight, the yaml files allow you to specify Python modules to import and relevant code to execute. Also, the SmartModule class, when instantiated, imports everything from the yaml into a configuration dictionary. This lets you add configuration modes to the yaml and access them in the Python command. A commented example is shown below.

```language=yaml

---
# Common configuration modes.
id: "bedroom light" # This is the name of my specific light
type: "Philips Hue Light" # This is the model of my light
connection_type: api # This is the connection method 
address: "192.168.4.68" # This is the address. In this case, an IP address. 
url: "https://192.168.4.68/api/v1" # the URL for the api 
imports: 
- "phue" # the code we execute under commands requires phue, so we import it here 
commands: {
  # EVERY Smart Module must implement setup
  "setup": "self._bridge = self.get_pref('phue').Bridge(self.address)", # setup our main object 
  "turn on": "self._bridge.set_light(2, 'on', True); ", #simple one-line function to perform our task
  "turn off": "self._bridge.set_light(2, 'on', False); ",
  "turn white": "self._bridge.set_light(2, 'xy', [1, 1])",
  "turn blue": "self._bridge.set_light(2, 'xy', [.15, .15])"
} 
# Optional configuation modes go here. 
# this could be a few things, such as brightness, color codes, etc.
```

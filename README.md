kapacitor_alert_to_icinga2
==========================

This plugin will help you import alert data from kapacitor into Icinga 2.

## Requirements
* Python 2.7

## How it work
You can add it as topic-handler:
```
kind: exec
options:
  prog: "/path/to/plugin/kapacitor_alert_to_icinga2.py"
  args:
    - "-u"
    - "user"
    - "-P"
    - "password"
```

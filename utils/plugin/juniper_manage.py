#! /usr/bin/env python

import sys

class Juniper_manage:

 _class_name = "Juniper Manage Class"

 def _show_run(self,get_switch,get_switch_property,get_switch_access):
  print get_switch
  print get_switch_property
  print get_switch_access

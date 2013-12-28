#! /usr/bin/env python

import sys
import re
from telnetlib import Telnet
import time

class Cisco_catalyst_switch:

 _class_name = "Cisco catalyst manage Class"
 _login_pattern = ['[Uu][Ss][Ee][Rr][Nn][Aa][Mm][Ee]:']
 _password_pattern = ['[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]:']
 _enable_pattern = ['[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]:']
 _error_pattern = ['\s*%+\s*']


 def _show_run(self,switch_db,switch_property_db,switch_access_db):
  ### variable arrange
  switch_name = switch_db['name']
  network_inform = switch_db['ip']
  telnet_port = network_inform.split(':')[1]
  telnet_ip = network_inform.split(':')[0].split('/')[0]
  telnet_user = switch_access_db['account']
  telnet_pass = switch_access_db['password']
  telnet_enable = switch_access_db['enable']
  ### telnet open time out in second
  self.telnet_open_timeout = float(10)

  ### telnet open processing
  telnet_pointer = self._connect_switch(switch_name,telnet_ip,telnet_port,telnet_user,telnet_pass,telnet_enable)
  ### enable command processing
  print "111"
  telnet_pointer.write("enable\n")
  telnet_pointer = self._enable_password(telnet_pointer)
  telnet_pointer.write(telnet_enable+"\n")
  telnet_pointer, response_msg = self._success_switch_confirm(telnet_pointer,switch_name)
  print "222"
  ### confirm the enable is ok or not
  telnet_pointer.write("show interfaces description\n")
  telnet_pointer.write(" ")
  print "333"
  telnet_pointer, response_msg = self._success_switch_confirm(telnet_pointer,switch_name)
  print "444"
  telnet_pointer.write("exit\n")

  print response_msg 
  ## telnet close()
  telnet_pointer.close()
  print "[done]"

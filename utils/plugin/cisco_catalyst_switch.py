#! /usr/bin/env python

import sys
from telnetlib import Telnet
import time

class Cisco_catalyst_switch:

 _class_name = "Cisco catalyst manage Class"
 _login_pattern = ['1','2']

 def _show_run(self,get_switch,get_switch_property,get_switch_access):
  ### variable arrange
  network_inform = get_switch['ip']
  telnet_port = network_inform.split(':')[1]
  telnet_ip = network_inform.split(':')[0].split('/')[0]
  telnet_user = get_switch_access['account']
  telnet_pass = get_switch_access['password']
  telnet_enable = get_switch_access['enable']
  ### telnet open time out in second
  self.telnet_open_timeout = float(10)

  print self.telnet_open_timeout
  print telnet_ip
  print telnet_port

  ### telnet open processing
  try:
   telnet_pointer =  Telnet(telnet_ip,telnet_port,self.telnet_open_timeout)
  except:
   msg="[ error : "+time.asctime()+" ] can't open the telnet, ip : "+telnet_ip+", port :"+telnet_port
   self.logging_msg(self.run_syslog,msg)
   sys.exit()
   
  print dir(self)
  print Cisco_manage._login_pattern
  #print telnet_pointer.expect([],5)
  telnet_pointer.close()

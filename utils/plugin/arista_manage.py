#! /usr/bin/env python

import sys
import time
from telnetlib import Telnet

class Arista_manage:

 _class_name = "Arista Manage Class"
 _login_pattern = ['login:',]
 _passwd_pattern = ['Password:',]

 def _show_run(self,get_switch,get_switch_property,get_switch_access):
  ### variable arrange
  switch_name = get_switch['name']
  network_inform = get_switch['ip']
  telnet_port = network_inform.split(':')[1]
  telnet_ip = network_inform.split(':')[0].split('/')[0]
  telnet_user = get_switch_access['account']
  telnet_pass = get_switch_access['password']
  telnet_enable = get_switch_access['enable']
  ### telnet open time out in second
  self.telnet_open_timeout = float(10)

  ### telnet open processing
  try:
   telnet_pointer =  Telnet(telnet_ip,telnet_port,self.telnet_open_timeout)
  except:
   msg="[ error : "+time.asctime()+" ] can't open the telnet, ip : "+telnet_ip+", port :"+telnet_port
   self.logging_msg(self.run_syslog,msg)
   sys.exit()


  ### telnet login processing
  try: 
   line_result = telnet_pointer.expect(Arista_manage._login_pattern,self.telnet_open_timeout)[1]
  except:
   msg="[ error : "+time.asctime()+" ] can't 2read login pattern : "+str(Arista_manage._login_pattern)
   self.logging_msg(self.run_syslog,msg)
   sys.exit()
  
  if not line_result:
   sys.exit()


  ### insert account for login
  telnet_pointer.write(telnet_user+"\n")

  ### wait the password pattern
  try:
   telnet_pointer.expect(Arista_manage._passwd_pattern,self.telnet_open_timeout)
  except:
   msg="[ error : "+time.asctime()+" ] can't read login pattern : "+str(Arista_manage._passwd_pattern)
   self.logging_msg(self.run_syslog,msg)
   sys.exit()  

  telnet_pointer.write(telnet_pass+"\n")
  print telnet_pointer.expect([switch_name+"\w*>"],self.telnet_open_timeout)
  telnet_pointer.write("enable1234\n")
  print telnet_pointer.expect(Arista_manage._passwd_pattern,self.telnet_open_timeout)
  telnet_pointer.write(telnet_enable+"\n")
  print telnet_pointer.expect([switch_name+"\w*#"],self.telnet_open_timeout)
  
  
  telnet_pointer.write("exit\n")
  telnet_pointer.read_all()
   
  telnet_pointer.close()

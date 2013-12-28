#! /usr/bin/env python

import sys
from telnetlib import Telnet
import time
import re

class Common_switch_manage:

 _telnet_open_timeout = float(10)

 ### processing pattern
 __login_pattern = ['[Uu][Ss][Ee][Rr][Nn][Aa][Mm][Ee]:']
 __password_pattern = ['[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]:']
 __enable_pattern = ['[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]:']
 __error_pattern = ['\s*%+\s*']

 ### connect function
 def _connect_switch(self,switch_name,ip,port,account,password,enable):
  telnet_pointer = Common_switch_manage.__telnet_open(self,ip,port)
  telnet_pointer = Common_switch_manage.__telnet_login(self,telnet_pointer)
  telnet_pointer.write(account+"\n")
  telnet_pointer = Common_switch_manage.__telnet_login_password(self,telnet_pointer)
  telnet_pointer.write(password+"\n")
  telnet_pointer, response_msg = Common_switch_manage._success_switch_confirm(self,telnet_pointer,switch_name) 
  ### return the pointer
  return telnet_pointer

 def __telnet_open(self,ip,port):
  ### telnet open processing
  try:
   telnet_pointer =  Telnet(ip,port,Common_switch_manage._telnet_open_timeout)
  except:
   msg="[ error : "+time.asctime()+" ] can't open the telnet, ip : "+ip+", port :"+port
   self.logging_msg(self.run_syslog,msg)
   sys.exit()
  ### return pointer
  return telnet_pointer

 def __telnet_login(self,pointer): 
  ### error message
  msg="[ error : "+time.asctime()+" ] can't read login pattern :"+str(Common_switch_manage.__login_pattern)
  ### telnet login processing
  try:
   process_result = pointer.expect(Common_switch_manage.__login_pattern,Common_switch_manage._telnet_open_timeout)
  except:
   ### timeout error happen when time out value is not existed
   self.logging_msg(self.run_syslog,msg)
   pointer.close()
   sys.exit()
  ### login not matched
  if not process_result[1]:
   self.logging_msg(self.run_syslog,msg)
   pointer.close()
   sys.exit()
  ### return pointer
  return pointer

 def __telnet_login_password(self,pointer):
  ### error message
  msg="[ error : "+time.asctime()+" ] can't read password pattern :"+str(Common_switch_manage.__password_pattern)
  ### telnet login password processing
  try:
   process_result = pointer.expect(Common_switch_manage.__password_pattern,Common_switch_manage._telnet_open_timeout)
  except:
   ### timeout error happen when time out value is not existed
   self.logging_msg(self.run_syslog,msg)
   pointer.close()
   sys.exit()
  ### password not matched!
  if not process_result[1]:
   self.logging_msg(self.run_syslog,msg)
   pointer.close()
   sys.exit()
  ### return pointer
  return pointer

 def _enable_password(self,pointer):
  ### error message
  msg="[ error : "+time.asctime()+" ] can't read enable password pattern :"+str(Common_switch_manage.__enable_pattern)
  ### telnet login password processing
  try:
   process_result = pointer.expect(Common_switch_manage.__enable_pattern,Common_switch_manage._telnet_open_timeout)
  except:
   ### timeout error happen when time out value is not existed
   self.logging_msg(self.run_syslog,msg)
   pointer.close()
   sys.exit()
  ### password not matched!
  if not process_result[1]:
   self.logging_msg(self.run_syslog,msg)
   pointer.close()
   sys.exit()
  ### return pointer
  return pointer
 
 def __success_pattern_create(self,switch_name):
  return [switch_name+"\w*>",switch_name+"\w*#",switch_name+"\(\w*\)>",switch_name+"\(\w*\)#"]

 def _success_switch_confirm(self,pointer,switch_name):
  ### error message
  msg="[ error : "+time.asctime()+" ] switch invalid command processing"
  ### login status check
  success_pattern = Common_switch_manage.__success_pattern_create(self,switch_name)
  try:
   process_result = pointer.expect(success_pattern,Common_switch_manage._telnet_open_timeout)
  except:
   self.logging_msg(self.run_syslog,msg)
   pointer.close()
   sys.exit()
  ### not matched success!
  response_msg = process_result[2]
  print response_msg
  for pattern in Common_switch_manage.__error_pattern:
   if re.search(pattern,response_msg):
    self.logging_msg(self.run_syslog,msg)
    pointer.close()
    sys.exit()
  ### return
  return pointer, response_msg

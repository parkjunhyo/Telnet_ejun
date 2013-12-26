#! /usr/bin/env python

import sys
import os
import re
import time
from help_manual import Help_manual
from MySQL_ejun.utils import common_function as MySQL_ejun_common

class Common_function(Help_manual,MySQL_ejun_common.Common_function):

 letter_mark_pattern=r'[\~\!\@\#\$\%\^\&\*\(\)\_\+\=\\\{\}\[\]\:\;\"\'\<\>\?\,\.\/]'
 ip_pattern=r'(\d+)\.(\d+)\.(\d+)\.(\d+)\/(\d+)\:(\d+)'
 
 def letter_status_confirm(self,value):
  if not re.search(self.letter_mark_pattern,value):
   return value
  else:
   msg="[ error : "+time.asctime()+" ] can't use "+letter_mark_pattern
   self.logging_msg(self.run_syslog,msg)
   sys.exit()
  
 def ip_format_confirm(self,value):
  ### if the value exist, this process can go
  ip_forms = re.search(self.ip_pattern,value)
  if ip_forms:
   ### element confirmation
   status=True
   for index in range(6):
    if index in [0,1,2,3]:
     if int(ip_forms.group(index+1)) > 255:
      status=False
      break
    elif index in [4]:
     if int(ip_forms.group(index+1)) > 32:
      status=False
      break
    else: 
     if int(ip_forms.group(index+1)) <= 0:
      status=False
      break
   ### status (error case), sys exit()
   if not status:
    msg="[ error : "+time.asctime()+" ] "+value+" is not correct ip address format"
    self.logging_msg(self.run_syslog,msg)
    sys.exit()
  else:
   msg="[ error : "+time.asctime()+" ] "+value+" is not correct ip address format"
   self.logging_msg(self.run_syslog,msg)
   sys.exit()
  ### return the ip address
  return ip_forms.group(0)

 def int_number_format_confirm(self,value):
  if re.match(r'\d+',value):
   return int(value)
  else:
   msg="[ error : "+time.asctime()+" ] "+value+" is "+str(type(value))
   self.logging_msg(self.run_syslog,msg)
   sys.exit()

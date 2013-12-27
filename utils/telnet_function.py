#! /usr/bin/env python

import sys
import os
import time
import re
from system_info import *

class Telnet_function:

 def show_switch_list(self,values):
  ### confirm the variables validation
  valid_values = self.confirm_input_number(values,[0,1])

  ### confirm the switch reg table is exist or not
  try:
   sample_msg = "select "+','.join(self.tbentries_dict[switch_reg_table])+" from "+switch_reg_table
  except:
   msg="[ error : "+time.asctime()+" ] there is no table "+switch_reg_table+" in the "+database_name
   self.logging_msg(self.run_syslog,msg)
   sys.exit()

  if valid_values:
   for search_condition in self.tbentries_dict[switch_reg_table]:
    result_msg = sample_msg+" where "+search_condition+"='"+valid_values[0]+"';"
    print "the result from ["+result_msg+"] :"
    self.send_msg([database_name,result_msg,'echo'])
    print "\n"
  else:
   result_msg = sample_msg+";"
   print "the result from ["+result_msg+"] :"
   self.send_msg([database_name,result_msg,'echo'])
   print "\n"


 def register_switch(self,values):
  ### confirm the variables validation
  valid_values = self.confirm_input_number(values,[0,len(self.send_msg([database_name,"desc "+switch_reg_table+";"]))])
  ### get the information to register into the database from input or user-define
  if values:
   if values[0] == '-a':
    ### input paramter validation check
    valid_params_list = self._register_paramter_validation_check(values[1:])
   else:
    ### mis-matched option
    self.show_manual(values)
    sys.exit()
  else:
   ### user define input processing
   require_msgs={0:"1. What is the switch name? :",
                 1:"2. What is the management ip address:port?(ex,10.0.0.1/24:23) :",
                 2:"3. What group is this switch belonged to?[group name] :",
                 3:"4. What is the vender name? :",
                 4:"5. What is the product name? :",
                 5:"6. What is the os version on? :",
                 6:"7. How many port number does this switch have? :",
                 7:"8. Where is the switch on? :",
                 8:"9. Write the extra comment for description! :"}
   input_values=[]
   for require_msg in range(len(require_msgs.keys())):
    print require_msgs[require_msg],
    ### get data from user input
    user_data = raw_input().strip()
    if user_data:
     input_values.append(user_data)
    else:
     print "[ command falult ] any information is inserted!"
     sys.exit()
   ### input paramter validation check
   valid_params_list = self._register_paramter_validation_check(input_values)

  ### check the valid parameter is already used or not
  search_result = self.send_msg([database_name,"select "+switch_reg_compare_name+" from "+switch_reg_table+" where "+switch_reg_compare_name+"='"+valid_params_list[0]+"';"])
  if search_result:
   msg="[ error : "+time.asctime()+" ] "+valid_params_list[0]+" is alread used"
   self.logging_msg(self.run_syslog,msg)
   sys.exit()
  search_result = self.send_msg([database_name,"select "+switch_reg_compare_ip+" from "+switch_reg_table+" where "+switch_reg_compare_ip+"='"+valid_params_list[1]+"';"])
  if search_result:
   msg="[ error : "+time.asctime()+" ] "+valid_params_list[0]+" is alread used"
   self.logging_msg(self.run_syslog,msg)
   sys.exit()
  ### totally, this valid paramter is ok to be register into the database now
  print valid_params_list
 
 def _register_paramter_validation_check(self,values):
  if len(values) == len(self.send_msg([database_name,"desc "+switch_reg_table+";"]))-1:
   switch_name = self.letter_status_confirm(values[0])
   switch_ip = self.ip_format_confirm(values[1])
   switch_group_name = self.letter_status_confirm(values[2])
   switch_vendor = self.letter_status_confirm(values[3])
   switch_product = self.letter_status_confirm(values[4])
   switch_os_version = values[5]
   switch_port = self.int_number_format_confirm(values[6])
   switch_location = self.letter_status_confirm(values[7])
   switch_description = self.letter_status_confirm(values[8])
   return switch_name,switch_ip,switch_group_name,switch_vendor,switch_product,switch_os_version,switch_port,switch_location,switch_description
  else:
   self.show_manual(values)
   sys.exit()

#! /usr/bin/env python

import sys
import os
import time
import re
import uuid
from plugin_manage import Plugin_manage

class Telnet_function(Plugin_manage):

 def show_switch_list(self,values):
  ### confirm the variables validation
  valid_values = self.confirm_input_number(values,[0,1])
  search_domain_switch = self.tbentries_dict['switch']

  ### confirm the switch reg table is exist or not
  try:
   basic_msg = "select "+','.join(search_domain_switch)+" from switch"
  except:
   msg="[ error : "+time.asctime()+" ] there in no switch table in the "+self.database_name
   self.logging_msg(self.run_syslog,msg)
   sys.exit()

  ### extend the basic_msg for searching every thing
  if valid_values:
   search_domain_switch.remove('id')
   search_value = valid_values[0]
   for entry in search_domain_switch:
    result_msg = basic_msg+" where "+entry+"='"+search_value+"';"
    print "this the result from command ("+result_msg+") ::\n"
    self.send_msg([self.database_name,result_msg,'echo'])
    print "\n"
  else:
   result_msg = basic_msg+";"
   print "this the result from command ("+result_msg+") ::\n"
   self.send_msg([self.database_name,result_msg,'echo'])
   print "\n"


 def register_switch(self,values):
  ### confirm the variables validation
  search_domain_switch = self.tbentries_dict['switch']
  search_domain_switch_property = self.tbentries_dict['switch_property']
  search_domain_switch_access = self.tbentries_dict['switch_access']
  search_domain_switch.remove('id')
  search_domain_switch_property.remove('id')
  search_domain_switch_access.remove('id')
  required_count = len(search_domain_switch)+len(search_domain_switch_property)+len(search_domain_switch_access)+1
  valid_values = self.confirm_input_number(values,[0,required_count])
  ### get the information to register into the database from input or user-define
  if valid_values:
   if valid_values[0] == '-a':
    ### input paramter validation check
    valid_params_list = list(self._register_paramter_validation_check(valid_values[1:]))
   else:
    ### mis-matched option
    self.show_manual(values)
    sys.exit()
  else:
   ### user define input processing
   require_msgs={0:" 1. What is the switch name? :",
                 1:" 2. What is the management ip address:port?(ex,10.0.0.1/24:23) :",
                 2:" 3. What group is this switch belonged to?[group name] :",
                 3:" 4. What is the vender name? :",
                 4:" 5. What is the product name? :",
                 5:" 6. What is the os version on? :",
                 6:" 7. How many port number does this switch have? :",
                 7:" 8. Where is the switch on? :",
                 8:" 9. What is the extra description? :",
                 9:"10. What is the account to access? :",
                10:"11. What is the password to access? :",
                11:"12. What is the enable password to access? :"}
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
   valid_params_list = list(self._register_paramter_validation_check(input_values))

  ### check the valid parameter is already used or not (using switch database)
  search_values = valid_params_list[0:2]
  for count in range(len(search_values)):
   search_values.reverse() 
   for entry in zip(search_domain_switch,search_values):
    search_msg = "select id from switch where "+entry[0]+"='"+entry[1]+"';"
    if self.send_msg([self.database_name,search_msg]):
     msg="[ error : "+time.asctime()+" ] "+str(search_values)+" has been alread assigned"
     self.logging_msg(self.run_syslog,msg)
     sys.exit()

  ### random uuid value find out
  switch_id = str(uuid.uuid4())
  while self.send_msg([self.database_name,"select id from switch where id='"+switch_id+"';"]):
   switch_id = str(uuid.uuid4())

  ### register the data into the database
  self._insert_data_into_switch_table([switch_id]+valid_params_list[0:2])
  self._insert_data_into_switch_property_table([switch_id]+valid_params_list[2:9])
  self._insert_data_into_switch_status_table([switch_id,'deactive'])
  self._insert_data_into_switch_access_table([switch_id]+valid_params_list[9:])

 def _insert_data_into_switch_table(self,values):
  uuid, name, ip = values
  sending_msg = "insert into switch (id,name,ip) values ('"+uuid+"','"+name+"','"+ip+"');"
  self.send_msg([self.database_name,sending_msg])

 def _insert_data_into_switch_property_table(self,values):
  uuid,group_name,vendor,product,os_version,port,location,description = values
  sending_msg = "insert into switch_property (id,group_name,vendor,product,os_version,port,location,description) values ('"+uuid+"','"+group_name+"','"+vendor+"','"+product+"','"+os_version+"',"+str(port)+",'"+location+"','"+description+"');"
  self.send_msg([self.database_name,sending_msg])

 def _insert_data_into_switch_status_table(self,values):
  uuid,status = values
  sending_msg = "insert into switch_status (id,status) values ('"+uuid+"','"+status+"');"
  self.send_msg([self.database_name,sending_msg])

 def _insert_data_into_switch_access_table(self,values):
  uuid,account,password,enable = values
  sending_msg = "insert into switch_access (id,account,password,enable) values ('"+uuid+"','"+account+"','"+password+"','"+enable+"');"
  self.send_msg([self.database_name,sending_msg])
  
 
 def _register_paramter_validation_check(self,values):
  switch_name = self.letter_status_confirm(values[0])
  switch_ip = self.ip_format_confirm(values[1])
  switch_group_name = self.letter_status_confirm(values[2])
  switch_vendor = self.letter_status_confirm(values[3])
  switch_product = self.letter_status_confirm(values[4])
  switch_os_version = values[5]
  switch_port = self.int_number_format_confirm(values[6])
  switch_location = self.letter_status_confirm(values[7])
  switch_description = self.letter_status_confirm(values[8])
  switch_account = self.letter_status_confirm(values[9])
  switch_password = values[10]
  switch_enable = values[11]
  return switch_name,switch_ip,switch_group_name,switch_vendor,switch_product,switch_os_version,switch_port,switch_location,switch_description,switch_account,switch_password,switch_enable

 ### removing the data from database with uuid
 def deregister_switch(self,values):
  valid_values = self.confirm_input_number(values,[1])
  self._delete_data_from_switch_table(valid_values)
  self._delete_data_from_switch_property_table(valid_values)
  self._delete_data_from_switch_status_table(valid_values)
  self._delete_data_from_switch_access_table(valid_values)

 def _delete_data_from_switch_table(self,values):
  sending_msg = "delete from switch where id='"+values[0]+"';"
  self.send_msg([self.database_name,sending_msg])

 def _delete_data_from_switch_property_table(self,values):
  sending_msg = "delete from switch_property where id='"+values[0]+"';"
  self.send_msg([self.database_name,sending_msg])

 def _delete_data_from_switch_status_table(self,values):
  sending_msg = "delete from switch_status where id='"+values[0]+"';"
  self.send_msg([self.database_name,sending_msg])

 def _delete_data_from_switch_access_table(self,values):
  sending_msg = "delete from switch_access where id='"+values[0]+"';"
  self.send_msg([self.database_name,sending_msg])

 ### show running-configuration processing
 def show_run(self,values):
  valid_values = self.confirm_input_number(values,[1])
  ### get information(data), name,ip,vendor,product,etc
  get_switch = self._get_data_from_switch_table(valid_values[0])
  get_switch_property = self._get_data_from_switch_property_table_by_uuid(get_switch['id'])
  ### re-arrange the data
  plug_name = get_switch_property['vendor'].lower()
  ### run the matched plugin function
  self.plugin_dict[plug_name]._show_run(self,get_switch,get_switch_property)

 def _get_data_from_switch_table(self,values):
  search_condition = self.tbentries_dict['switch']
  search_contents = ','.join(search_condition)
  for condition in search_condition:
   sending_msg = "select "+search_contents+" from switch where "+condition+"='"+values+"'"
   search_result = self.send_msg([self.database_name,sending_msg])
   if search_result:
    break
  ### return the values
  return dict(zip(search_condition,list(search_result[0])))

 def _get_data_from_switch_property_table_by_uuid(self,values):
  search_condition = self.tbentries_dict['switch_property']
  search_contents = ','.join(search_condition)
  sending_msg = "select "+search_contents+" from switch_property where id='"+values+"'"
  search_result = self.send_msg([self.database_name,sending_msg])
  return dict(zip(search_condition,list(search_result[0])))
  

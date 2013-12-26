#! /usr/bin/env python

import sys
import os
from utils.common_function import Common_function
from utils.system_info import *


class Run_commander(Common_function):

 def __init__(self, values):

  ### current Working directory
  self.directory=os.getcwd()

  ### default log file information
  self.log_d = log_directory
  self.log_dirname = log_directory.split("/")[len(log_directory.split("/"))-1]
  self.run_syslog = self.log_d+"/runsys.log"

  ### shell name define
  self.shell_name=values[0]

  ### Confrim the folder status 
  self.create_directory_if_exists_not(["/".join(log_directory.split("/")[:len(log_directory.split("/"))-1]),self.log_dirname])
 
  ### table entries list up of database
  self.database_name = database_name
  self.tbentries_dict = self._get_table_enties_from_database(self.database_name)

 def run_command(self,values):

  # Confirm the input values
  self.command, self.values = Common_function.get_input_values(self, values)
  self.function[self.command](self,self.values)


if __name__=='__main__':
 command = Run_commander(sys.argv)
 command.run_command(sys.argv)
 

#! /usr/bin/env python

import sys
from telnet_function import Telnet_function

class Help_manual(Telnet_function):

 def show_manual(self,values):
  print "\n"
  print "this is the [ "+self.shell_name+" ] command manual"
  print "\n"
  print "  : show_switch_list (search condition, option)"
  print "          >> print out the registerd switch lists"
  print "          >> echo option is used for viewing on monitor\n"
  print "  : register_switch (-a, option)"
  print "          >> register the switch device in the database"
  print "          >> '-a' option : full option register"
  print "          >> full option register parameter"
  print "             (1.S/W name) (2.management ip:port) (3.group name)"
  print "             (4.vendor name) (5.product model) (6.product name) (7.os verion)"
  print "             (8.the number of ports) (9.location) (10.description)"
  print "             (11.access user) (12.access password) (13.enable)\n"
  print "  : deregister_switch (switch_id, uuid)"
  print "          >> deregister the switch device in the database\n"
  print "  : show_run (S/W ID : S/W name : management ip:port)"
  print "          >> print out the running-configuration of the switch"
  print "          >> choose one of S/W ID, S/W name and management ip:port\n"


 function={"-h":show_manual,
           "--help":show_manual,
           "show_switch_list":Telnet_function.show_switch_list,
           "register_switch":Telnet_function.register_switch,
           "deregister_switch":Telnet_function.deregister_switch,
           "show_run":Telnet_function.show_run}

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
  print "             (4.vendor name) (5.product name) (6.os verion)"
  print "             (7.the number of ports) (8.location) (9.description)\n"


 function={"-h":show_manual,
           "--help":show_manual,
           "show_switch_list":Telnet_function.show_switch_list,
           "register_switch":Telnet_function.register_switch}

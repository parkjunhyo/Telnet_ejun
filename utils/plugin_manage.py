#! /usr/bin/env python

import sys
from plugin.cisco_manage import Cisco_manage
from plugin.juniper_manage import Juniper_manage
from plugin.arista_manage import Arista_manage

class Plugin_manage(Cisco_manage,Juniper_manage,Arista_manage):

 plugin_dict={"cisco":Cisco_manage,
              "juniper":Juniper_manage,
              "arista":Arista_manage}

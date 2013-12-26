#! /usr/bin/env python

import sys
from telnetlib import Telnet
import time
from cisco_catalyst_switch import Cisco_catalyst_switch

class Cisco_manage(Cisco_catalyst_switch):

 _model_dict={"catalyst":Cisco_catalyst_switch,}

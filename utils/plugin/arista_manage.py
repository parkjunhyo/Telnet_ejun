#! /usr/bin/env python

import sys
import time
from telnetlib import Telnet
from arista_arista_switch import Arista_arista_switch

class Arista_manage(Arista_arista_switch):

 _model_dict={"arista":Arista_arista_switch,}

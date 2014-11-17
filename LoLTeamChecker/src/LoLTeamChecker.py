# -*- coding: latin-1 -*-

# script to check LoLTeamCheckerGUI
from __future__ import division # must be first import
#from riotapi_py import *
from rankeddata import GrabRankedData
from staticdata import GrabStaticData
from LoLTeamCheckerModel import LoLTeamCheckerModel
from LoLTeamCheckerController import LoLTeamCheckerController
from lolteamchecker_gui import LoLTeamCheckerGUI
import Tkinter as tk
# Explicitly initialise arguments to controller
my_gui = LoLTeamCheckerGUI()
myapp = LoLTeamCheckerController(my_gui, LoLTeamCheckerModel())
my_gui.mainloop()

##root = tk.Tk()
##my_gui = LoLTeamCheckerController(LoLTeamCheckerGUI())
##root.mainloop()

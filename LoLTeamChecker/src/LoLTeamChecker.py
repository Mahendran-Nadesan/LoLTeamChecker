# -*- coding: latin-1 -*-

# script to check LoLTeamCheckerGUI
from __future__ import division # must be first import
#from riotapi_py import *
from rankeddata import GrabRankedData
from staticdata import GrabStaticData
from LoLTeamCheckerModel import LoLTeamCheckerModel
from LoLTeamCheckerController import LoLTeamCheckerController
from LoLTeamCheckerGUI import LoLTeamCheckerGUI
import Tkinter as tk

#api_key = "e20154f8-3601-40ac-ae35-5af13e62cc8c" 
#region = "euw" 
#versions = {"gsbn": "v1.4", "gsbid": "v1.4", "ggbid": "v1.3", "grsbid": "v1.3", "sgcbid": "v1.2"} 



# Explicitly initialise arguments to controller


my_gui = LoLTeamCheckerGUI()
##
####data_model = LoLTeamCheckerModel()
myapp = LoLTeamCheckerController(my_gui, LoLTeamCheckerModel())
my_gui.mainloop()

##root = tk.Tk()
##my_gui = LoLTeamCheckerController(LoLTeamCheckerGUI())
##root.mainloop()

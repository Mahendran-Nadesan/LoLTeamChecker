"""The Controller for LoLTeamChecker

Controls calls to GUI and the data model."""



class LoLTeamCheckerController:
    """Handles calls to the model, Riot API, and the GUI."""
    def __init__(self, gui, model): #, model, 
        """Initialises model and GUI to control."""
        self.gui = gui
        self.model = model
        self._set_bindings()

    def __str__(self):
        pass

    def _process_line(self, line):
        """Runs all the methods for getting the data in one row of the
        gui."""
        # Get the values from the GUI
        [summoner_name, champ_name] = self.gui._get_user_values(line)
        # Check region info
        if self.model.region != self.gui._get_region_value():
            self.model.region = self.gui._get_region_value()
            self.model._update()
        # Error checking
        try:
##            self.model._get_champ_stats(summoner_name, champ_name, do_all=False)
            self.model._get_champ_stats(summoner_name, champ_name)
        except:
            print "some error"
            self.gui._show_error_message(self.model.error)
        
        # Update GUI
        if summoner_name in self.model.final_stats:
            print "updating"
            self.gui._set_right_info_row_values(line, self.model.final_stats[summoner_name][champ_name])
        
    def _process_all(self):
        """Runs all methods for getting data for all rows, plus the
        summary stats."""
        self.summoner_names = self.gui._get_all_summoners()
        self.champ_names = self.gui._get_all_champs()

        self.pairs = zip(self.summoner_names, self.champ_names)
        for i, pair in enumerate(self.pairs):
            try:
                self.model._get_champ_stats(pair[0], pair[1])
            except:
                pass
##                self.gui._show_error_message(self.model.error)

            if pair[0] in self.model.final_stats:
                print
                print "Setting values for {s}: {c}.".format(s=pair[0], c=pair[1])
                print "Values are: ", self.model.final_stats[pair[0]][pair[1]]
                print
                self.gui._set_right_info_row_values(i, self.model.final_stats[pair[0]][pair[1]])
                

    def _process_summary(self):
        """Runs the methods for processing the average/summary
        pane."""
        print "in process summary"
        self._process_all()
        print "getting summary stats"
        if len(self.gui._get_all_summoners()) != 0:
            self.model._get_summary_stats(self.gui._get_all_summoners(), self.gui._get_all_champs())
            print "setting summary stats"
            self.gui._set_summary_values(self.model.ave_stats['EWAve'], self.model.ave_stats['Ave'])
        
    def _set_bindings(self):
        """Set bindings for buttons in GUI."""
        for i, button in enumerate(self.gui.row_buttons[0]):
            button.config(command=lambda row=i: self._process_line(row))
        self.gui.go_button.config(command=lambda i=i: self._process_summary())
        self.gui.getall_button.config(command=lambda i=i: self._process_all())

    

##if __name__=="__main__":
##    app = LoLTeamCheckerController()
##    app.gui.mainloop()

# -*- coding: utf-8 -*-

__author__ = "Nicholas Murray"

import klibs
from klibs import P
from klibs.KLUserInterface import any_key
from klibs.KLGraphics import fill, flip
from klibs.KLCommunication import message


# Entire experiment object
class aether_typing_study_experiment(klibs.Experiment):

    # Define all experimental stimuli drawn on the screen
    def setup(self):
        
        # Text to copy for any given written stimulus
        self.text_to_copy = "What did you eat for breakfast today?"

    # Define block order
    def block(self):
        pass

    # Define what kind of trial this is
    def trial_prep(self):
        
        fill()
        message(
            self.text_to_copy, 
            location = P.screen_c, 
            registration = 5 # centered 
        )
        flip()
        any_key()

    # Define trial order of events
    def trial(self):

        

        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number
        }

    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass
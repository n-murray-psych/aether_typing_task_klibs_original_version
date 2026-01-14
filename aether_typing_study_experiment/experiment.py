# -*- coding: utf-8 -*-

__author__ = "Nicholas Murray"

import klibs
from klibs import P

# Entire experiment object
class aether_typing_study_experiment(klibs.Experiment):

    # Define all experimental stimuli drawn on the screen
    def setup(self):
        pass

    # Define block order
    def block(self):
        pass

    # Define what kind of trial this is
    def trial_prep(self):
        pass

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

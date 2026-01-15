# -*- coding: utf-8 -*-

__author__ = "Nicholas Murray"

import klibs
from klibs import P
from klibs.KLUserInterface import any_key
from klibs.KLGraphics import fill, blit, flip
from klibs.KLCommunication import user_queries, query, query_no_backspace, message

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

        left_text = "text for sample"  # whatever your big text is

        def draw_left():
            # left column: top-left, wrapped
            msg = message(left_text, align="left", wrap_width=int(P.screen_x * 0.45), blit_txt=False)
            blit(msg, 1, (int(P.screen_x * 0.05), int(P.screen_y * 0.10)))

        typed_text = query_no_backspace(
            user_queries.experimental[0],
            draw_left_fn=draw_left
        )

        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "typed_response": typed_text
        }

    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass
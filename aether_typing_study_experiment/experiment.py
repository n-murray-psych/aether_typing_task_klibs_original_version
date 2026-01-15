# -*- coding: utf-8 -*-

__author__ = "Nicholas Murray"

import klibs
from klibs import P
from klibs.KLUserInterface import any_key
from klibs.KLGraphics import fill, blit, flip
from klibs.KLCommunication import user_queries, query, query_no_backspace, message
from klibs.KLUtilities import deg_to_px
from klibs.KLJSON_Object import AttributeDict

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

        left_text = """On a quiet morning, the city feels temporarily paused, as if everyone has collectively agreed to sleep a little longer than usual. Streets that are normally busy with traffic remain empty, and the air carries a faint stillness that is rarely noticed during the day. The sounds that do exist become more noticeable: a distant bus braking at an intersection, the rhythmic footsteps of a jogger passing by, or the low hum of heating systems waking up inside nearby buildings. These small details often go unnoticed when life moves quickly, but they shape the texture of everyday experience. People tend to underestimate how much routine influences their perception of time. A familiar schedule can make hours pass without reflection, while a small change can suddenly slow everything down. Taking a different route to work, trying a new food for breakfast, or sitting in a different chair can create a surprising sense of awareness. These moments disrupt habit just enough to draw attention back to the present, reminding us that experience is not only about what happens, but how it is noticed. Technology plays an increasingly central role in shaping attention, often pulling it away from these quieter moments. Notifications, messages, and alerts compete constantly for focus, fragmenting thought into smaller and smaller pieces. While these tools can be useful, they can also make it difficult to stay with a single task for long. Writing, reading, or thinking deeply often requires sustained concentration, something that now feels less natural than it once did. Despite this, many people are rediscovering the value of deliberate focus. Activities like journaling, long-form reading, or practicing a skill without interruption can feel restorative. These practices encourage patience and allow mistakes to happen without immediate correction. Over time, this slower pace can improve accuracy, creativity, and confidence, even when speed is eventually required. In the end, productivity is not only about efficiency, but about balance. Moving quickly has its place, especially when deadlines approach, but slowing down can reveal insights that speed alone cannot provide. Paying attention to small details, allowing thoughts to unfold naturally, and accepting moments of quiet can make everyday tasks feel more intentional and meaningful."""

        def draw_left():
            # left column: top-left, wrapped
            msg = message(left_text, align="left", wrap_width=int(P.screen_x * 0.45), blit_txt=False)
            blit(msg, 1, (int(P.screen_x * 0.05), int(P.screen_y * .84)))

        q = user_queries.experimental[0]

        q.format.positions = AttributeDict({
            "locations": AttributeDict({
                "query": [int(P.screen_x * 0.75), int(P.screen_y * 0.12)],
                "input": [int(P.screen_x * 0.75), int(P.screen_y * 0.22)],
                "error": [int(P.screen_x * 0.75), int(P.screen_y * 0.30)]
            }),
            "registrations": AttributeDict({
                "query": 5,
                "input": 5,
                "error": 5
            })
        })

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
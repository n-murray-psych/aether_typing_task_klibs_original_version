# -*- coding: utf-8 -*-

__author__ = "Nicholas Murray"

import klibs
from klibs import P
from klibs.KLUserInterface import any_key
from klibs.KLGraphics import fill, blit, flip, KLDraw as kld  # kld to draw shapes on the screen
from klibs.KLCommunication import user_queries, query, query_no_backspace, message
from klibs.KLUtilities import deg_to_px
from klibs.KLJSON_Object import AttributeDict
from klibs.KLTime import CountDown
from klibs.KLEventQueue import pump
from klibs.KLGraphics.KLDraw import Rectangle


class aether_typing_study_experiment(klibs.Experiment):

    def setup(self):

        # Define typing task and attach it to self
        def typing_task():

            # Left column text
            left_text = """On a quiet morning, the city feels temporarily paused, as if everyone has collectively agreed to sleep a little longer than usual. Streets that are normally busy with traffic remain empty, and the air carries a faint stillness that is rarely noticed during the day. The sounds that do exist become more noticeable: a distant bus braking at an intersection, the rhythmic footsteps of a jogger passing by, or the low hum of heating systems waking up inside nearby buildings. These small details often go unnoticed when life moves quickly, but they shape the texture of everyday experience. People tend to underestimate how much routine influences their perception of time. A familiar schedule can make hours pass without reflection, while a small change can suddenly slow everything down. Taking a different route to work, trying a new food for breakfast, or sitting in a different chair can create a surprising sense of awareness. These moments disrupt habit just enough to draw attention back to the present, reminding us that experience is not only about what happens, but how it is noticed. Technology plays an increasingly central role in shaping attention, often pulling it away from these quieter moments. Notifications, messages, and alerts compete constantly for focus, fragmenting thought into smaller and smaller pieces. While these tools can be useful, they can also make it difficult to stay with a single task for long. Writing, reading, or thinking deeply often requires sustained concentration, something that now feels less natural than it once did. Despite this, many people are rediscovering the value of deliberate focus. Activities like journaling, long-form reading, or practicing a skill without interruption can feel restorative. These practices encourage patience and allow mistakes to happen without immediate correction. Over time, this slower pace can improve accuracy, creativity, and confidence, even when speed is eventually required. In the end, productivity is not only about efficiency, but about balance. Moving quickly has its place, especially when deadlines approach, but slowing down can reveal insights that speed alone cannot provide. Paying attention to small details, allowing thoughts to unfold naturally, and accepting moments of quiet can make everyday tasks feel more intentional and meaningful."""

            def draw_left():
                msg = message(
                    left_text,
                    align="left",
                    wrap_width=int(P.screen_x * 0.45),
                    blit_txt=False
                )
                blit(msg, 1, (int(P.screen_x * 0.05), int(P.screen_y * 0.84)))

            q = user_queries.experimental[0]

            q.format.positions = AttributeDict({
                "locations": AttributeDict({
                    "query": [int(P.screen_x * 0.75), int(P.screen_y * 0.12)],
                    "input": [int(P.screen_x * 0.75), int(P.screen_y * 0.22)],
                    "error": [int(P.screen_x * 0.75), int(P.screen_y * 0.30)],
                }),
                "registrations": AttributeDict({
                    "query": 5,
                    "input": 5,
                    "error": 5,
                }),
            })

            # Timer for this trial
            self.timer = CountDown(150)  # 150 seconds

            def draw_timer():
                def mmss(seconds):
                    seconds = max(0, int(seconds))
                    return f"{seconds // 60:02d}:{seconds % 60:02d}"

                timer_x = int(P.screen_x * 0.5)
                timer_y = int(P.screen_y * 0.1)

                erase_w, erase_h = 300, 80
                eraser = Rectangle(erase_w, erase_h, fill=(255, 0, 0))
                blit(eraser, 5, (timer_x, timer_y))

                sec_left = int(self.timer.remaining())
                timer_surface = message(mmss(sec_left), blit_txt=False)
                blit(timer_surface, 5, (timer_x, timer_y))

            # Run the query and RETURN the typed text
            typed_text = query_no_backspace(
                user_queries.experimental[0],
                draw_left_fn=draw_left,
                draw_timer_fn=draw_timer
            )

            return typed_text

        self.typing_task = typing_task

    def block(self):
        pass

    def trial_prep(self):
        pass

    def trial(self):

        # Size of entire spatial working memory task array
        array_size_deg = 3 # Create little squares for the array that are 1/9 the size of the whole array
        square_size_deg = array_size_deg / 3
        square_size_px = int(deg_to_px(square_size_deg))

        # Create a white square to base the little squares on
        white_square = Rectangle(
            width = square_size_px, 
            height = square_size_px, 
            fill = (255, 255, 255), # White fill
            stroke = [1, (0,0,0)] # Black border
        )

        # Draw the centre square
        def draw_a_square(square_location=None):
            cx, cy = P.screen_c

            dx, dy = 0, 0
            step = square_size_px

            if square_location == "1": 
                dx = -step
                dy = step
            elif square_location == "2":
                dy = step
            elif square_location == "3":
                dx = step
                dy = step
            elif square_location == "4": 
                dx = -step
            elif square_location == "5": 
                dx = 0
                dy = 0 # centre square
            elif square_location == "6": 
                dx = step
            elif square_location == "7": 
                dx = -step
                dy = -step
            elif square_location == "8": 
                dy = -step
            elif square_location == "9": 
                dx = step
                dy = -step

            blit(
                white_square,
                registration=5,
                location=(cx + dx, cy + dy)
            )

        fill()
        draw_a_square("1")
        draw_a_square("2")
        draw_a_square("3")
        draw_a_square("4")
        draw_a_square("5") # Centre square
        draw_a_square("6")
        draw_a_square("7")
        draw_a_square("8")
        draw_a_square("9")
        flip()
        any_key()

        # Call typing_task and capture the response
        #typed_text = self.typing_task()

        # Set your response variables to NONE when you're testing the development of other tasks.
        typed_text = None
        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "typed_response": typed_text,
        }

    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass

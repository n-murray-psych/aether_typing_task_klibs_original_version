# -*- coding: utf-8 -*-

__author__ = "Nicholas Murray"

import klibs
from klibs import P
from klibs.KLUserInterface import any_key, mouse_pos, get_clicks
from klibs.KLGraphics import fill, blit, flip, KLDraw as kld  # kld to draw shapes on the screen
from klibs.KLCommunication import user_queries, query, query_no_backspace, message
from klibs.KLUtilities import deg_to_px
from klibs.KLJSON_Object import AttributeDict
from klibs.KLTime import CountDown
from klibs.KLEventQueue import pump
from klibs.KLGraphics.KLDraw import Rectangle
import random
from klibs.KLResponseCollectors import CursorResponse 
from klibs.KLConstants import TK_MS
from klibs.KLBoundary import RectangleBoundary, BoundarySet

class aether_typing_study_experiment(klibs.Experiment):

    def setup(self):

        #####################################
        # TYPING TASK: STIMULI AND RESPONSES
        #####################################

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

        #####################################
        # SPATIAL TASK: STIMULI
        #####################################

        def draw_spatial_search_array(target_task_array=None, response_task_array=False):
            """
            Draws a 3x3 spatial search array.

            Parameters
            ----------
            target_task_array : int or str or None
                - None  → all squares white
                - 1–9   → that square is filled black
            """

            # --- Geometry ---
            array_size_deg = 3
            square_size_deg = array_size_deg / 3
            square_size_px = int(deg_to_px(square_size_deg))
            step = square_size_px

            # --- Colours ---
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)

            # Ensure consistent comparison
            if target_task_array is not None:
                target_task_array = str(target_task_array)

            # --- Draw one square ---
            def draw_a_square(square_location):

                fill_colour = BLACK if square_location == target_task_array else WHITE

                single_square = Rectangle(
                    width=square_size_px,
                    height=square_size_px,
                    fill=fill_colour,
                    stroke=[1, (0, 0, 0)]
                )

                cx, cy = P.screen_c
                dx, dy = 0, 0

                if square_location == "1":
                    dx, dy = -step, step
                elif square_location == "2":
                    dy = step
                elif square_location == "3":
                    dx, dy = step, step
                elif square_location == "4":
                    dx = -step
                elif square_location == "5":
                    pass  # centre
                elif square_location == "6":
                    dx = step
                elif square_location == "7":
                    dx, dy = -step, -step
                elif square_location == "8":
                    dy = -step
                elif square_location == "9":
                    dx, dy = step, -step

                blit(single_square, registration=5, location=(cx + dx, cy + dy))

            # --- Draw full array ---
            fill()
            for i in range(1, 10):
                draw_a_square(str(i))
            if response_task_array == True:
                # Instruction message for spatial response phase
                self.spatial_msg = message(
                    "Click the FIRST square in the array which turned black",
                    style="default",
                    align="center",
                    blit_txt=False
                )
                self.spatial_msg_loc = (P.screen_c[0], int(P.screen_y * 0.25))
                blit(
                    self.spatial_msg, 
                    registration = 5,
                    location = self.spatial_msg_loc
                )
            flip()

        self.draw_spatial_search_array = draw_spatial_search_array

        def spatial_search_array_stimuli():

            # Sequence of target squares to show
            targets = ["1", "2", "3", "4"]

            # Optional: initial blank array before sequence
            draw_spatial_search_array()
            flip()

            start_timer = CountDown(1.0)
            while start_timer.counting():
                pump(True)

            for i, target in enumerate(targets):

                # --- SHOW TARGET ARRAY (1 second) ---
                stim_timer = CountDown(1.0)
                while stim_timer.counting():
                    pump(True)
                    draw_spatial_search_array(target)

                # --- INTER-STIMULUS BLANK (200 ms) ---
                if i < len(targets) - 1:
                    isi_timer = CountDown(0.2)
                    while isi_timer.counting():
                        pump(True)
                        draw_spatial_search_array()  # blank array

        self.spatial_search_array_stimuli = spatial_search_array_stimuli

        ################################################
        # SPATIAL TASK: RESPONSE COLLECTION BOUNDARIES
        ################################################
        
        # --- Build 3×3 grid as RectangleBoundary objects ---
        array_size_deg = 3
        square_size_deg = array_size_deg / 3.0
        square_size_px = int(deg_to_px(square_size_deg))
        step = square_size_px
        half = square_size_px / 2.0

        cx, cy = P.screen_c  # screen centre

        # store boundaries here: "1"–"9" -> RectangleBoundary
        self.spatial_boundaries = {}

        for idx in range(1, 10):  # 1..9

            # Grid layout:
            # 1 2 3  -> top row
            # 4 5 6  -> middle row
            # 7 8 9  -> bottom row

            row = (idx - 1) // 3      # 0 (top), 1 (middle), 2 (bottom)
            col = (idx - 1) % 3       # 0 (left), 1 (centre), 2 (right)

            # Centre of each square
            x_c = cx + (col - 1) * step   # -step, 0, +step
            y_c = cy + (1 - row) * step   # +step, 0, -step

            top_left     = (x_c - half, y_c - half)
            bottom_right = (x_c + half, y_c + half)

            label = str(idx)  # "1"–"9"

            # This is basically your button1/button2 pattern:
            # box1 = RectangleBoundary('1', (x1, y1), (x2, y2))
            boundary = RectangleBoundary(label, top_left, bottom_right)
            self.spatial_boundaries[label] = boundary

        #####################################
        # VERBAL TASK: RESPONSE
        #####################################

        def verbal_task_response(word_number=None):

            # Use the verbal query you defined in params.py
            if word_number == "1": 
                q = user_queries.verbal1[0]
            elif word_number == "2": 
                q = user_queries.verbal2[0]
            elif word_number == "3": 
                q = user_queries.verbal3[0] 
            elif word_number == "4": 
                q = user_queries.verbal4[0]   

            # Show the query + timer, let them type
            verbal_response = query(q)

            return verbal_response

        self.verbal_task_response = verbal_task_response

        #####################################
        # VERBAL TASK STIMULI
        #####################################

        def verbal_task_stimuli(words):
            """
            Present a list of 4 words one at a time.

            Args:
                words (list/tuple): 4 strings to present in order.
            """

            # Basic safety: if more than 4 provided, just use the first 4
            words = list(words)[:4]

            # Instruction screen
            instr = message(
                "Remember the following list of words",
                style="default",
                align="center",
                blit_txt=False
            )

            fill()
            blit(instr, registration=5, location=P.screen_c)
            flip()
            any_key()  # wait for participant to be ready

            # Present each word for 1s, with 200ms blank between
            for i, w in enumerate(words):

                # Create the word surface
                word_msg = message(
                    w,
                    style="default",
                    align="center",
                    blit_txt=False
                )

                # --- Show word for 1 second ---
                word_timer = CountDown(1.0)  # 1 second
                while word_timer.counting():
                    # Keep KLibs responsive
                    pump(True)

                    fill()
                    blit(word_msg, registration=5, location=P.screen_c)
                    flip()

                # --- 200 ms blank interval before next word ---
                if i < len(words) - 1:
                    gap_timer = CountDown(0.2)  # 200 ms
                    while gap_timer.counting():
                        pump(True)
                        fill()
                        flip()

        self.verbal_task_stimuli = verbal_task_stimuli
            
    def block(self):
        pass
 
    def setup_response_collector(self):

        # Give participants 2 seconds to respond to each spatial array
        self.rc.terminate_after = [2000, TK_MS]
        self.rc.uses(CursorResponse)

        # draw your spatial array while collecting the response
        # (make sure draw_spatial_search_array() draws the BLANK 3x3 when called with no args)
        self.rc.display_callback = self.draw_spatial_search_array(response_task_array=True)

        listener = self.rc.cursor_listener
        listener.interrupts = True  # end as soon as a valid click happens

        # IMPORTANT: listener.boundaries is an OrderedDict (label -> Boundary)
        # Clear any old ones:
        listener.boundaries.clear()

        # Add our 9 RectangleBoundary objects
        for label, boundary in self.spatial_boundaries.items():
            listener.boundaries[label] = boundary

    def trial_prep(self):
        pass

    def trial(self):

        # Set your response variables to NONE when you're testing the development of other tasks.
        #typed_text = None
        #spatial_response = None
        #verbal_response = None

        # Define the response collector as a function within the trial 
        # so all this code doesn't have to be written over and over again
        # every time you run the response collector.

        def spatial_task_response_collector(): 
            # Configure RC for this trial
            self.setup_response_collector()

            # Run response collection (draws array, waits for click/timeout)
            self.rc.collect()

            # This should be the label of the boundary the click fell inside,
            # i.e., "1"–"9", or None on timeout
            spatial_response = self.rc.cursor_listener.response()

            # Optional: clear the screen after
            fill()
            flip()

            return spatial_response

        # Run spatial search task stimuli
        self.spatial_search_array_stimuli()

        # Call typing_task and capture the response
        typed_text = self.typing_task()

        # Run spatial task response collector
        spatial_response = spatial_task_response_collector()

        # Run verbal task stimuli
        word_list = ["Table", "House", "Garden", "Pencil"]

        self.verbal_task_stimuli(word_list)

        # Call typing_task and capture the response
        typed_text = self.typing_task()

        # Run verbal task response collection
        verbal_response = self.verbal_task_response("1")
        
        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "typed_response": typed_text,
            "spatial_search_task_response": spatial_response,
            "verbal_response": verbal_response
        }

    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass

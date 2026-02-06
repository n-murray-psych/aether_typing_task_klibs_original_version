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
from klibs.KLEventQueue import pump, flush
from klibs.KLGraphics.KLDraw import Rectangle
from klibs.KLResponseCollectors import CursorResponse 
from klibs.KLConstants import TK_MS
from klibs.KLBoundary import RectangleBoundary, BoundarySet
import itertools
import random
from klibs.KLText import add_text_style

class aether_typing_study_experiment(klibs.Experiment):

    def setup(self):

        #####################################
        # TYPING TASK: STIMULI AND RESPONSES
        #####################################

        practice_text = ["""On a quiet morning, the city feels temporarily paused, as if everyone has collectively agreed to sleep a little longer than usual. Streets that are normally busy with traffic remain empty, and the air carries a faint stillness that is rarely noticed during the day. The sounds that do exist become more noticeable: a distant bus braking at an intersection, the rhythmic footsteps of a jogger passing by, or the low hum of heating systems waking up inside nearby buildings. These small details often go unnoticed when life moves quickly, but they shape the texture of everyday experience. People tend to underestimate how much routine influences their perception of time. A familiar schedule can make hours pass without reflection, while a small change can suddenly slow everything down. Taking a different route to work, trying a new food for breakfast, or sitting in a different chair can create a surprising sense of awareness. These moments disrupt habit just enough to draw attention back to the present, reminding us that experience is not only about what happens, but how it is noticed. Technology plays an increasingly central role in shaping attention, often pulling it away from these quieter moments. Notifications, messages, and alerts compete constantly for focus, fragmenting thought into smaller and smaller pieces. While these tools can be useful, they can also make it difficult to stay with a single task for long. Writing, reading, or thinking deeply often requires sustained concentration, something that now feels less natural than it once did. Despite this, many people are rediscovering the value of deliberate focus. Activities like journaling, long-form reading, or practicing a skill without interruption can feel restorative. These practices encourage patience and allow mistakes to happen without immediate correction. Over time, this slower pace can improve accuracy, creativity, and confidence, even when speed is eventually required. In the end, productivity is not only about efficiency, but about balance. Moving quickly has its place, especially when deadlines approach, but slowing down can reveal insights that speed alone cannot provide. Paying attention to small details, allowing thoughts to unfold naturally, and accepting moments of quiet can make everyday tasks feel more intentional and meaningful."""]

        # Unique text samples
        self.left_texts = [
            # Practice is index 0
            """On a quiet morning, the city feels temporarily paused, as if everyone has collectively agreed to sleep a little longer than usual. Streets that are normally busy with traffic remain empty, and the air carries a faint stillness that is rarely noticed during the day. The sounds that do exist become more noticeable: a distant bus braking at an intersection, the rhythmic footsteps of a jogger passing by, or the low hum of heating systems waking up inside nearby buildings. These small details often go unnoticed when life moves quickly, but they shape the texture of everyday experience. People tend to underestimate how much routine influences their perception of time. A familiar schedule can make hours pass without reflection, while a small change can suddenly slow everything down. Taking a different route to work, trying a new food for breakfast, or sitting in a different chair can create a surprising sense of awareness. These moments disrupt habit just enough to draw attention back to the present, reminding us that experience is not only about what happens, but how it is noticed. Technology plays an increasingly central role in shaping attention, often pulling it away from these quieter moments. Notifications, messages, and alerts compete constantly for focus, fragmenting thought into smaller and smaller pieces. While these tools can be useful, they can also make it difficult to stay with a single task for long. Writing, reading, or thinking deeply often requires sustained concentration, something that now feels less natural than it once did. Despite this, many people are rediscovering the value of deliberate focus. Activities like journaling, long-form reading, or practicing a skill without interruption can feel restorative. These practices encourage patience and allow mistakes to happen without immediate correction. Over time, this slower pace can improve accuracy, creativity, and confidence, even when speed is eventually required. In the end, productivity is not only about efficiency, but about balance. Moving quickly has its place, especially when deadlines approach, but slowing down can reveal insights that speed alone cannot provide. Paying attention to small details, allowing thoughts to unfold naturally, and accepting moments of quiet can make everyday tasks feel more intentional and meaningful.""", 
            """Text sample 1A . . . """, # Index 1
            """Text sample 2A . . . """, # Index 2
            """Text Sample 3A . . . """, # Index 3
            """Text sample 1B . . . """, # Index 4
            """Text Sample 2B . . . """, # Index 5
            """Text sample 3B . . . """  # Index 6
        ]
        
        # Set all possible task orders
        task_labels = ["typing", "spatial", "verbal"]
        self.all_task_orders = list(itertools.permutations(task_labels))

        # Define typing task and attach it to self
        def typing_task(text_index):

            add_text_style(label = "timer_text", size = 48)

            # Left column text
            left_text = self.left_texts[text_index]

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
                eraser = Rectangle(erase_w, erase_h, fill=(176, 0, 0))
                blit(eraser, 5, (timer_x, timer_y))

                sec_left = int(self.timer.remaining())
                timer_surface = message(mmss(sec_left), style = "timer_text", blit_txt=False)
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

        # Randomly generate three orders of target appearance
            # (practice, first administration, second administration).
        self.possible_spatial_targets = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] # All possible spatial targets (1-9)
        self.spatial_order = random.sample(population = self.possible_spatial_targets, k = 4)
        self.practice_spatial_order = random.sample(population = self.possible_spatial_targets, k = 4)
        self.first_spatial_order = random.sample(population = self.possible_spatial_targets, k = 4)
        self.second_spatial_order = random.sample(population = self.possible_spatial_targets, k = 4)

        def draw_spatial_grid(target_task_array=None):
            # --- Geometry ---
            array_size_deg = 3
            square_size_deg = array_size_deg / 3
            square_size_px = int(deg_to_px(square_size_deg))
            step = square_size_px

            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)

            if target_task_array is not None:
                target_task_array = str(target_task_array)

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
                    pass
                elif square_location == "6":
                    dx = step
                elif square_location == "7":
                    dx, dy = -step, -step
                elif square_location == "8":
                    dy = -step
                elif square_location == "9":
                    dx, dy = step, -step

                blit(single_square, registration=5, location=(cx + dx, cy + dy))

            # Draw full grid
            fill()
            for i in range(1, 10):
                draw_a_square(str(i))

        self.draw_spatial_grid = draw_spatial_grid

        def draw_spatial_array_with_message(target_task_array=None):
            # 1. Draw the grid (no message)
            self.draw_spatial_grid(target_task_array)

            # 2. Decide which ordinal word to use based on self.n_square_message
            #    Expected values: "first", "second", "third", "fourth"
            #    Default to "first" if it's missing or something unexpected.
            ordinal_key = getattr(self, "n_square_message", "first")

            ordinal_map = {
                "first":  "FIRST",
                "second": "SECOND",
                "third":  "THIRD",
                "fourth": "FOURTH",
            }
            ordinal_word = ordinal_map.get(ordinal_key, "FIRST")

            # 3. Build the instruction text with the correct ordinal
            instr_text = f"Click the {ordinal_word} square in the array which turned black"

            spatial_msg = message(
                instr_text,
                style="default",
                align="center",
                blit_txt=False
            )
            spatial_msg_loc = (P.screen_c[0], int(P.screen_y * 0.25))

            # 4. Draw message and flip
            blit(spatial_msg, registration=5, location=spatial_msg_loc)
            flip()
        
        self.draw_spatial_array_with_message = draw_spatial_array_with_message

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
            response_task_array = response_task_array
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

        def spatial_search_array_stimuli(target_list):

            targets = target_list

            # initial blank
            self.draw_spatial_grid(target_task_array=None)
            flip()

            start_timer = CountDown(1.0)
            while start_timer.counting():
                pump(True)

            for i, target in enumerate(targets):

                # 1 second target
                stim_timer = CountDown(1.0)
                while stim_timer.counting():
                    pump(True)
                    self.draw_spatial_grid(target)
                    flip()

                # 200 ms blank
                if i < len(targets) - 1:
                    isi_timer = CountDown(0.2)
                    while isi_timer.counting():
                        pump(True)
                        self.draw_spatial_grid(None)
                        flip()

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
                verbal_response = query(user_queries.verbal1[0])
            elif word_number == "2": 
                verbal_response = query(user_queries.verbal2[0])
            elif word_number == "3": 
                verbal_response = query(user_queries.verbal3[0])
            elif word_number == "4": 
                verbal_response = query(user_queries.verbal4[0])   

            return verbal_response

        self.verbal_task_response = verbal_task_response

        #####################################
        # VERBAL TASK STIMULI
        #####################################

        self.possible_words = [
            "ridge", "stick", "grain", "hatch", 
            "close", "rim", "pole", "chair", 
            "glass", "stone", "fork", "lamp", 
            "field", "box", "sheet", "brick", 
            "pin", "bell", "step", "card"
        ]

        self.practice_word_list = random.sample(population = self.possible_words, k = 4)
        self.post_practice_words = [w for w in self.possible_words if w not in  self.practice_word_list]
        self.first_word_list = random.sample(population = self.post_practice_words, k = 4)
        self.post_first_word_list = [w for w in self.post_practice_words if w not in  self.first_word_list]
        self.second_word_list = random.sample(population = self.post_first_word_list, k = 4)

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

        ########################################
        # Define the block orders for each task
        ########################################

        def run_typing_block(text_index): 
            typed_text = self.typing_task(text_index)
            return typed_text
        
        self.run_typing_block = run_typing_block
        
        def run_spatial_block():
            self.spatial_search_array_stimuli()
            spatial_responses = []
            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)
            return spatial_responses
        
        self.run_spatial_block = run_spatial_block
            
        def run_verbal_block(word_list): 
            self.verbal_task_stimuli(word_list)
            verbal_responses = []
            for i in range(1, 5):
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)
            return(verbal_responses)
        
        self.run_verbal_block = run_verbal_block

    def block(self):
        pass
 
    def setup_response_collector(self):

        self.rc.terminate_after = [2000, TK_MS]
        self.rc.uses(CursorResponse)

        # draw grid + dynamic message during response collection
        self.rc.display_callback = self.draw_spatial_array_with_message

        listener = self.rc.cursor_listener
        listener.interrupts = True

        listener.boundaries.clear()
        for label, boundary in self.spatial_boundaries.items():
            listener.boundaries[label] = boundary

        flush()
        listener.reset()

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

        def spatial_task_response_collector(which_n):
            """
            which_n: 1, 2, 3, or 4 indicating first/second/third/fourth target
            """

            idx_to_label = {
                1: "first",
                2: "second",
                3: "third",
                4: "fourth",
            }

            # Set the message state on the experiment object
            self.n_square_message = idx_to_label.get(which_n, "first")

            # Now configure and run the response collector
            self.setup_response_collector()
            self.rc.collect()
            spatial_response = self.rc.cursor_listener.response()

            fill()
            flip()

            return spatial_response
        
        self.spatial_task_response_collector = spatial_task_response_collector

        ######################################################
        # Task order counterbalanced
        ######################################################

        # Store all responses to be inspected and saved later
        all_typed = []
        spatial_responses = []
        verbal_responses = []

        ######################################################
        # Control, spatial, verbal
        ######################################################

        if P.condition == "csv": 

            ####################
            # Practice
            ####################

            # Run the typing task (control, no working memory task)
            text_practice = 0
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.practice_spatial_order)

            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)
            
            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.practice_word_list)
            
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)

            ####################
            # First run
            ####################

            # Run the typing task (control, no working memory task)
            text_idx_1 = 1 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)

            text_idx_2 = 2 # Text set 2
            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)
            
            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)
            
            text_idx_3 = 3 # Text set 3
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)    

            ####################
            # Second run
            ####################

            # Run the typing task (control, no working memory task)
            text_idx_4 = 4 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)

            text_idx_5 = 5 # Text set 2
            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)
            
            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)
            
            text_idx_6 = 6 # Text set 3
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)            

        ######################################################
        # Control, verbal, spatial
        ######################################################

        if P.condition == "cvs": 

            ####################
            # Practice
            ####################

            # Run the typing task (control, no working memory task)
            text_practice = 0
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.practice_word_list)

            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)
            
            # Run the spatial task
            self.spatial_search_array_stimuli(self.practice_spatial_order)
            
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            ####################
            # First run
            ####################

            # Run the typing task (control, no working memory task)
            text_idx_1 = 1 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)

            text_idx_2 = 2 # Text set 2
            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)   
            
            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)
            
            text_idx_3 = 3 # Text set 3
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 

            ####################
            # Second run
            ####################

            # Run the typing task (control, no working memory task)
            text_idx_4 = 4 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)

            text_idx_5 = 5 # Text set 2
            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 
            
            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)
            
            text_idx_6 = 6 # Text set 3
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)   

        ######################################################
        # Spatial, verbal, control
        ######################################################

        if P.condition == "svc": 

            ####################
            # Practice
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.practice_spatial_order)

            # Run the typing task (control, no working memory task)
            text_practice = 0
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.practice_word_list)

            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)
            
            # Control task
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            ####################
            # First run
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)

            # Run the typing task (control, no working memory task)
            text_idx_1 = 1 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)

            text_idx_2 = 2 # Text set 2
            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)   
            
            # Control
            text_idx_3 = 3 # Text set 3
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            ####################
            # Second run
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)

            # Run the typing task (control, no working memory task)
            text_idx_4 = 4 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)

            text_idx_5 = 5 # Text set 2
            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 
            
            # Control
            text_idx_6 = 6 # Text set 3
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

        ######################################################
        # Spatial, control, verbal
        ######################################################

        if P.condition == "scv": 

            ####################
            # Practice
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.practice_spatial_order)

            # Run the typing task (control, no working memory task)
            text_practice = 0
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            # Control
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.practice_word_list)
            
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)

            ####################
            # First run
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)

            # Run the typing task (control, no working memory task)
            text_idx_1 = 1 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 

            # Control
            text_idx_2 = 2 # Text set 2
            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)
            
            text_idx_3 = 3 # Text set 3
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)  

            ####################
            # Second run
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)

            # Run the typing task (control, no working memory task)
            text_idx_4 = 4 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            # Control
            text_idx_5 = 5 # Text set 2
            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)
            
            text_idx_6 = 6 # Text set 3
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 

        ######################################################
        # Verbal, spatial, control
        ######################################################

        if P.condition == "vsc": 

            ####################
            # Practice
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.practice_word_list)

            text_practice = 0
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)

            # Run the spatial task
            self.spatial_search_array_stimuli(self.practice_spatial_order)

            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            # Control
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            ####################
            # First run
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)

            text_idx_1 = 1 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)  

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)

            text_idx_2 = 2 # Text set 2
            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 
            
            # Control
            text_idx_3 = 3 # Text set 3
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            ####################
            # Second run
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)

            text_idx_4 = 4 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)

            text_idx_5 = 5 # Text set 2
            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)
            
            # Control
            text_idx_6 = 6 # Text set 3
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

        ######################################################
        # Verbal, control, spatial
        ######################################################

        if P.condition == "vcs": 

            ####################
            # Practice
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.practice_word_list)

            text_practice = 0
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)

            # Control
            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.practice_spatial_order)

            typed = self.run_typing_block(text_practice)
            all_typed.append((text_practice, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            ####################
            # First run
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)

            text_idx_1 = 1 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)  

            # Control
            text_idx_2 = 2 # Text set 2
            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)
            
            text_idx_3 = 3 # Text set 3
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 

            ####################
            # Second run
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)

            text_idx_4 = 4 # Text set to use, set by default to first set
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 

            # Control
            text_idx_5 = 5 # Text set 2
            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)            
            
            text_idx_6 = 6 # Text set 3
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

########################################################   
        # ---- DATA UNPACKING / SAFETY ----
########################################################

        # Typed text assignments and responses
        typed_practice_stimuli = self.left_texts[0]
        typed_practice1 = all_typed[0][1] if len(all_typed) > 0 else None
        typed_practice2 = all_typed[1][1] if len(all_typed) > 1 else None
        typed_practice3 = all_typed[2][1] if len(all_typed) > 2 else None
        typed1 = all_typed[3][1] if len(all_typed) > 3 else None
        typed2 = all_typed[4][1] if len(all_typed) > 4 else None
        typed3 = all_typed[5][1] if len(all_typed) > 5 else None
        typed4 = all_typed[6][1] if len(all_typed) > 6 else None
        typed5 = all_typed[7][1] if len(all_typed) > 7 else None
        typed6 = all_typed[8][1] if len(all_typed) > 8 else None

        # Spatial assignments and responses
        s_practice1_stimuli = self.practice_spatial_order[0]
        s_practice2_stimuli = self.practice_spatial_order[1]
        s_practice3_stimuli = self.practice_spatial_order[2]
        s_practice4_stimuli = self.practice_spatial_order[3]
        s_practice1 = spatial_responses[0][0] if len(spatial_responses) >0 else None
        s_practice2 = spatial_responses[1][0] if len(spatial_responses) >1 else None
        s_practice3 = spatial_responses[2][0] if len(spatial_responses) >2 else None
        s_practice4 = spatial_responses[3][0] if len(spatial_responses) >3 else None
        
        s1_stimuli = self.first_spatial_order[0]
        s2_stimuli = self.first_spatial_order[1]
        s3_stimuli = self.first_spatial_order[2]
        s4_stimuli = self.first_spatial_order[3]  
        s1 = spatial_responses[4][0] if len(spatial_responses) >4 else None
        s2 = spatial_responses[5][0] if len(spatial_responses) >5 else None
        s3 = spatial_responses[6][0] if len(spatial_responses) >6 else None
        s4 = spatial_responses[7][0] if len(spatial_responses) >7 else None
        
        s5_stimuli = self.second_spatial_order[0]
        s6_stimuli = self.second_spatial_order[1]
        s7_stimuli = self.second_spatial_order[2]
        s8_stimuli = self.second_spatial_order[3]  
        s5 = spatial_responses[8][0] if len(spatial_responses) >8 else None
        s6 = spatial_responses[9][0] if len(spatial_responses) >9 else None
        s7 = spatial_responses[10][0] if len(spatial_responses) >10 else None
        s8 = spatial_responses[11][0] if len(spatial_responses) >11 else None
        
        # Verbal responses

        v_practice1_stimuli = self.practice_word_list[0]
        v_practice2_stimuli = self.practice_word_list[1]
        v_practice3_stimuli = self.practice_word_list[2]
        v_practice4_stimuli = self.practice_word_list[3]
        v_practice1 = verbal_responses[0] if len(verbal_responses) >0 else None
        v_practice2 = verbal_responses[1] if len(verbal_responses) >1 else None
        v_practice3 = verbal_responses[2] if len(verbal_responses) >2 else None
        v_practice4 = verbal_responses[3] if len(verbal_responses) >3 else None
        
        v1_stimuli = self.first_word_list[0]
        v2_stimuli = self.first_word_list[1]
        v3_stimuli = self.first_word_list[2]
        v4_stimuli = self.first_word_list[3]
        v1 = verbal_responses[4] if len(verbal_responses) >4 else None
        v2 = verbal_responses[5] if len(verbal_responses) >5 else None
        v3 = verbal_responses[6] if len(verbal_responses) >6 else None
        v4 = verbal_responses[7] if len(verbal_responses) >7 else None
        v5_stimuli = self.second_word_list[0]
        v6_stimuli = self.second_word_list[1]
        v7_stimuli = self.second_word_list[2]
        v8_stimuli = self.second_word_list[3]        
        v5 = verbal_responses[8] if len(verbal_responses) >8 else None
        v6 = verbal_responses[9] if len(verbal_responses) >9 else None
        v7 = verbal_responses[10] if len(verbal_responses) >10 else None
        v8 = verbal_responses[11] if len(verbal_responses) >11 else None
    
        # ---- DATA RETURN ----
        # Here we’re still returning ONE row for this "mega trial".
        # You can unpack or summarize however you like, e.g.:

        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "condition": P.condition, 

            # typed responses (from up to 3 typing blocks)
            "typed_practice_stimuli": typed_practice_stimuli, 
            "typed_practice1": typed_practice1,
            "typed_practice2": typed_practice2,
            "typed_practice3": typed_practice3,
            "typed1": typed1,
            "typed2": typed2,
            "typed3": typed3,
            "typed4": typed4,
            "typed5": typed5,
            "typed6": typed6,

            # spatial responses (4 clicks from the spatial block)
            "s_practice1_stimuli": s_practice1_stimuli, 
            "s_practice2_stimuli": s_practice2_stimuli,
            "s_practice3_stimuli": s_practice3_stimuli,
            "s_practice4_stimuli": s_practice4_stimuli,
            "spatial_practice1": s_practice1, 
            "spatial_practice2": s_practice2,
            "spatial_practice3": s_practice3,
            "spatial_practice4": s_practice4,
            "s1_stimuli": s1_stimuli, 
            "s2_stimuli": s2_stimuli,
            "s3_stimuli": s3_stimuli,
            "s4_stimuli": s4_stimuli,
            "spatial_target1": s1, 
            "spatial_target2": s2, 
            "spatial_target3": s3, 
            "spatial_target4": s4, 
            "s5_stimuli": s5_stimuli, 
            "s6_stimuli": s6_stimuli,
            "s7_stimuli": s7_stimuli,
            "s8_stimuli": s8_stimuli,            
            "spatial_target5": s5, 
            "spatial_target6": s6, 
            "spatial_target7": s7, 
            "spatial_target8": s8, 

            # verbal responses (4 recalls from the verbal block)
            "v_practice1_stimuli": v_practice1_stimuli, 
            "v_practice2_stimuli": v_practice2_stimuli,
            "v_practice3_stimuli": v_practice3_stimuli,
            "v_practice4_stimuli": v_practice4_stimuli,
            "verbal_practice1": v_practice1,
            "verbal_practice2": v_practice2,
            "verbal_practice3": v_practice3,
            "verbal_practice4": v_practice4,
            "v1_stimuli": v1_stimuli, 
            "v2_stimuli": v2_stimuli, 
            "v3_stimuli": v3_stimuli, 
            "v4_stimuli": v4_stimuli, 
            "verbal_target1": v1, 
            "verbal_target2": v2, 
            "verbal_target3": v3, 
            "verbal_target4": v4, 
            "v5_stimuli": v5_stimuli, 
            "v6_stimuli": v6_stimuli, 
            "v7_stimuli": v7_stimuli, 
            "v8_stimuli": v8_stimuli,             
            "verbal_target5": v5, 
            "verbal_target6": v6, 
            "verbal_target7": v7, 
            "verbal_target8": v8, 

        }
    
    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass

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

        # Helper function for centering queries
        def centre_query(q, y_offset_query=-60, y_offset_input=200, y_offset_error=90):
            cx, cy = P.screen_c
            q.format.positions = AttributeDict({
                "locations": AttributeDict({
                    "query": [cx, cy + y_offset_query],
                    "input": [cx, cy + y_offset_input],
                    "error": [cx, cy + y_offset_error],
                }),
                "registrations": AttributeDict({
                    "query": 5,
                    "input": 5,
                    "error": 5,
                }),
            })

        self.centre_query = centre_query

        #####################################
        # TYPING TASK: STIMULI AND RESPONSES
        #####################################

        practice_text = ["""On a quiet morning, the city feels temporarily paused, as if everyone has collectively agreed to sleep a little longer than usual. Streets that are normally busy with traffic remain empty, and the air carries a faint stillness that is rarely noticed during the day. The sounds that do exist become more noticeable: a distant bus braking at an intersection, the rhythmic footsteps of a jogger passing by, or the low hum of heating systems waking up inside nearby buildings. These small details often go unnoticed when life moves quickly, but they shape the texture of everyday experience. People tend to underestimate how much routine influences their perception of time. A familiar schedule can make hours pass without reflection, while a small change can suddenly slow everything down. Taking a different route to work, trying a new food for breakfast, or sitting in a different chair can create a surprising sense of awareness. These moments disrupt habit just enough to draw attention back to the present, reminding us that experience is not only about what happens, but how it is noticed. Technology plays an increasingly central role in shaping attention, often pulling it away from these quieter moments. Notifications, messages, and alerts compete constantly for focus, fragmenting thought into smaller and smaller pieces. While these tools can be useful, they can also make it difficult to stay with a single task for long. Writing, reading, or thinking deeply often requires sustained concentration, something that now feels less natural than it once did. Despite this, many people are rediscovering the value of deliberate focus. Activities like journaling, long-form reading, or practicing a skill without interruption can feel restorative. These practices encourage patience and allow mistakes to happen without immediate correction. Over time, this slower pace can improve accuracy, creativity, and confidence, even when speed is eventually required. In the end, productivity is not only about efficiency, but about balance. Moving quickly has its place, especially when deadlines approach, but slowing down can reveal insights that speed alone cannot provide. Paying attention to small details, allowing thoughts to unfold naturally, and accepting moments of quiet can make everyday tasks feel more intentional and meaningful."""]

        # Unique text samples
        self.left_texts = [
            # Practice is index 0
            """On a quiet morning, the city feels temporarily paused, as if everyone has collectively agreed to sleep a little longer than usual. Streets that are normally busy with traffic remain empty, and the air carries a faint stillness that is rarely noticed during the day. The sounds that do exist become more noticeable: a distant bus braking at an intersection, the rhythmic footsteps of a jogger passing by, or the low hum of heating systems waking up inside nearby buildings. These small details often go unnoticed when life moves quickly, but they shape the texture of everyday experience. People tend to underestimate how much routine influences their perception of time. A familiar schedule can make hours pass without reflection, while a small change can suddenly slow everything down. Taking a different route to work, trying a new food for breakfast, or sitting in a different chair can create a surprising sense of awareness. These moments disrupt habit just enough to draw attention back to the present, reminding us that experience is not only about what happens, but how it is noticed. Technology plays an increasingly central role in shaping attention, often pulling it away from these quieter moments. Notifications, messages, and alerts compete constantly for focus, fragmenting thought into smaller and smaller pieces. While these tools can be useful, they can also make it difficult to stay with a single task for long. Writing, reading, or thinking deeply often requires sustained concentration, something that now feels less natural than it once did. Despite this, many people are rediscovering the value of deliberate focus. Activities like journaling, long-form reading, or practicing a skill without interruption can feel restorative. These practices encourage patience and allow mistakes to happen without immediate correction. Over time, this slower pace can improve accuracy, creativity, and confidence, even when speed is eventually required. In the end, productivity is not only about efficiency, but about balance. Moving quickly has its place, especially when deadlines approach, but slowing down can reveal insights that speed alone cannot provide. Paying attention to small details, allowing thoughts to unfold naturally, and accepting moments of quiet can make everyday tasks feel more intentional and meaningful.""", # Practice
            """Contemporary psychology is a diverse field that is influenced by all of the historical perspectives described in the preceding section. Reflective of the discipline’s diversity is the diversity seen within the American Psychological Association. The American Psychological Association is a professional organization representing psychologists in the United States. They are the largest organization of psychologists in the world, and its mission is to advance and disseminate psychological knowledge for the betterment of people. There are a number of divisions within the Association, representing a wide variety of specialties that range from Societies for the Psychology of Religion and Spirituality to Exercise and Sport Psychology to Behavioural Neuroscience and Comparative Psychology. Reflecting the diversity of the field of psychology itself, members, affiliate members, and associate members span the spectrum from students to doctoral-level psychologists, and come from a variety of places including educational settings, criminal justice, hospitals, the armed forces, and industry. G. Stanley Hall was the first president of the Association. Before he earned his doctoral degree, he was an adjunct instructor at Wilberforce University, a historically black college/university, while serving as faculty at Antioch College. Hall went on to work under William James, earning his PhD. Eventually, he became the first president of Clark University in Massachusetts when it was founded. The Association for Psychological Science was founded in 1988. They seek to advance the scientific orientation of psychology. Its founding resulted from disagreements between members of the scientific and clinical branches of psychology within the American Psychological Association. The Association for Psychological Science publishes five research journals and engages in education and advocacy with funding agencies. A significant proportion of its members are international, although the majority is located in the United States. Other organizations provide networking and collaboration opportunities for professionals of several ethnic or racial groups working in psychology, such as the National Latina/o Psychological Association, the Asian American Psychological Association, the Association of Black Psychologists, and the Society of Indian Psychologists. Most of these groups are also dedicated to studying psychological and social issues within their specific communities.""", # Index 1, Sample 1A
            """Scientific research is a critical tool for successfully navigating our complex world. Without it, we would be forced to rely solely on intuition, other people’s authority, and blind luck. While many of us feel confident in our abilities to decipher and interact with the world around us, history is filled with examples of how very wrong we can be when we fail to recognize the need for evidence in supporting claims. At various times in history, we would have been certain that the sun revolved around a flat earth, that the earth’s continents did not move, and that mental illness was caused by possession. It is through systematic scientific research that we divest ourselves of our preconceived notions and superstitions and gain an objective understanding of ourselves and our world. The goal of all scientists is to better understand the world around them. Psychologists focus their attention on understanding behaviour, as well as the cognitive and physiological processes that underlie behaviour. In contrast to other methods that people use to understand the behaviour of others, such as intuition and personal experience, the hallmark of scientific research is that there is evidence to support a claim. Scientific knowledge is empirical. It is grounded in objective, tangible evidence that can be observed time and time again, regardless of who is observing. While behaviour is observable, the mind is not. If someone is crying, we can see behaviour. However, the reason for the behaviour is more difficult to determine. Is the person crying due to being sad, in pain, or happy? Sometimes we can learn the reason for someone’s behaviour by simply asking a question. However, there are situations in which an individual is either uncomfortable or unwilling to answer the question honestly, or is incapable of answering. For example, infants would not be able to explain why they are crying. In such circumstances, the psychologist must be creative in finding ways to better understand behaviour. This chapter explores how scientific knowledge is generated, and how important that knowledge is in forming decisions in our personal lives and in the public domain. Trying to determine which theories are and are not accepted by the scientific community can be difficult, especially in an area of research as broad as psychology. More than ever before, we have an incredible amount of information at our fingertips, and a simple internet search on any given research topic might result in a number of contradictory studies. """, # Index 2, Sample 2A
            """During the early twentieth century, American psychology was dominated by behaviourism and psychoanalysis. However, some psychologists were uncomfortable with what they viewed as limited perspectives being so influential to the field. They objected to the pessimism and determinism of Freud. They also disliked the reductionism, or simplifying nature, of behaviourism. Behaviourism is also deterministic at its core, because it sees human behaviour as entirely determined by a combination of genetics and environment. Some psychologists began to form their own ideas that emphasized personal control, intentionality, and a true predisposition for good will as important for our self-concept and our behaviour. Thus, humanism emerged. Humanism is a perspective within psychology that emphasizes the potential for good will that is innate to all humans. Two of the most well-known proponents of humanistic psychology are Abraham Maslow and Carl Rogers. Abraham Maslow was an American psychologist who is best known for proposing a hierarchy of human needs in motivating behaviour. Although this concept will be discussed in more detail in a later chapter, a brief overview will be provided here. Maslow asserted that so long as basic needs necessary for survival were met, higher-level needs would begin to motivate behaviour. According to Maslow, the highest-level needs relate to self-actualization, a process by which we achieve our full potential. Obviously, the focus on the positive aspects of human nature that are characteristic of the humanistic perspective is evident. Humanistic psychologists rejected, on principle, the research approach based on reductionist experimentation in the tradition of the physical and biological sciences, because it missed the wholeness of the human being. Beginning with Maslow and Rogers, there was an insistence on a humanistic research program. This program has been largely qualitative not measurement-based, but there exist a number of quantitative research strains within humanistic psychology, including research on happiness, self-concept, meditation, and the outcomes of humanistic psychotherapy. Carl Rogers was also an American psychologist who, like Maslow, emphasized the potential for good will that exists within all people. Rogers used a therapeutic technique known as client-centred therapy in helping his clients deal with problematic issues that resulted in their seeking psychotherapy. Unlike a psychoanalytic approach in which the therapist plays an important role.""", # Index 3, Sample 3A
            """As the name suggests, biopsychology explores how our biology influences our behaviour. While biological psychology is a broad field, many biological psychologists want to understand how the structure and function of the nervous system is related to behaviour. As such, they often combine the research strategies of both psychologists and physiologists to accomplish this goal. The research interests of biological psychologists span a number of domains, including but not limited to, sensory and motor systems, sleep, drug use and abuse, ingestive behaviour, reproductive behaviour, neurodevelopment, plasticity of the nervous system, and biological correlates of psychological disorders. Given the broad areas of interest falling under the purview of biological psychology, it will probably come as no surprise that individuals from all sorts of backgrounds are involved in this research, including biologists, medical professionals, physiologists, and chemists. This interdisciplinary approach is often referred to as neuroscience, of which biological psychology is a component. While biopsychology typically focuses on the immediate causes of behaviour based in the physiology of a human or other animal, evolutionary psychology seeks to study the ultimate biological causes of behaviour. To the extent that a behaviour is impacted by genetics, a behaviour, like any anatomical characteristic of a human or animal, will demonstrate adaption to its surroundings. These surroundings include the physical environment and, since interactions between organisms can be important to survival and reproduction, the social environment. The study of behaviour in the context of evolution has its origins with Charles Darwin, the co-discoverer of the theory of evolution by natural selection. Darwin was well aware that behaviours should be adaptive and wrote multiple books to explore this field. Evolutionary psychology, and specifically, the evolutionary psychology of humans, has enjoyed a resurgence in recent decades. To be subject to evolution by natural selection, a behaviour must have a significant genetic cause. In general, we expect all human cultures to express a behaviour if it is caused genetically, since the genetic differences among human groups are small. The approach taken by most evolutionary psychologists is to predict the outcome of a behaviour in a particular situation based on evolutionary theory and then to make observations, or conduct experiments, to determine whether the results match the theory.""", # Index 4, Sample 1B
            """In these cases, we are witnessing the scientific community going through the process of reaching a consensus, and it could be quite some time before a consensus emerges. For example, the explosion in our use of technology has led researchers to question whether this ultimately helps or hinders us. The use and implementation of technology in educational settings has become widespread over the last few decades. Researchers are coming to different conclusions regarding the use of technology. To illustrate this point, a study investigating a smartphone app targeting surgery residents found that the use of this app can increase student engagement and raise test scores. Conversely, another study found that the use of technology in undergraduate student populations had negative impacts on sleep, communication, and time management skills. Until sufficient amounts of research have been conducted, there will be no clear consensus on the effects that technology has on a student’s acquisition of knowledge, study skills, and mental health. In the meantime, we should strive to think critically about the information we encounter by exercising a degree of healthy skepticism. When someone makes a claim, we should examine the claim from a number of different perspectives. This is especially important when we consider how much information in advertising campaigns and on the internet claims to be based on scientific evidence when in actuality it is a belief or perspective of just a few individuals trying to sell a product or draw attention to their perspectives. We should be informed consumers of the information made available to us because decisions based on this information have significant consequences. One such consequence can be seen in politics and public policy. Imagine that you have been elected as the Premier of your province. One of your responsibilities is to manage the provincial budget and determine how to best spend your constituents’ tax dollars. As the new Premier, you need to decide whether to continue funding early intervention programs. These programs are designed to help children who come from low-income backgrounds, have special needs, or face other disadvantages. These programs may involve providing a wide variety of services to maximize the children’s development and position them for optimal levels of success in school and later in life. While such programs sound appealing, you would want to be sure that they also proved effective before investing additional money in these programs.""", # Index 5, Sample 2B 
            """Humanism has been influential to psychology as a whole. Both Maslow and Rogers are well-known names among students of psychology, and their ideas have influenced many scholars. Furthermore, Rogers’ client-centred approach to therapy is still commonly used in psychotherapeutic settings today. Behaviourism’s emphasis on objectivity and focus on external behaviour had pulled psychologists’ attention away from the mind for a prolonged period of time. The early work of the humanistic psychologists redirected attention to the individual human as a whole, and as a conscious and self-aware being. By the fifties, new disciplinary perspectives in linguistics, neuroscience, and computer science were emerging, and these areas revived interest in the mind as a focus of scientific inquiry. This particular perspective has come to be known as the cognitive revolution. Later, Ulric Neisser published the first textbook, which served as a core text in cognitive psychology courses around the country. Although no one person is entirely responsible for starting the cognitive revolution, Noam Chomsky was very influential in the early days of this movement. Chomsky, an American linguist, was dissatisfied with the influence that behaviourism had had on psychology. He believed that psychology’s focus on behaviour was short-sighted and that the field had to re-incorporate mental functioning into its purview if it were to offer any meaningful contributions to understanding behaviour. Although no one person is entirely responsible for starting the cognitive revolution, Noam Chomsky was very influential in the early days of this movement. Chomsky, an American linguist, was dissatisfied with the influence that behaviourism had had on psychology. He believed that psychology’s focus on behaviour was short-sighted and that the field had to re-incorporate mental functioning into its purview if it were to offer any meaningful contributions to understanding behaviour. Culture has important impacts on individuals and social psychology, yet the effects of culture on psychology are under-studied. There is a risk that psychological theories and data derived from white, American settings could be assumed to apply to individuals and social groups from other cultures, and this is unlikely to be true. One weakness in the field of cross-cultural psychology is that in looking for differences in psychological attributes across cultures, there remains a need to go beyond simple descriptive statistics. In this sense, it has remained a descriptive science."""  # Index 6, Sample 3B
        ]
        
        # Set all possible task orders
        task_labels = ["typing", "spatial", "verbal"]
        self.all_task_orders = list(itertools.permutations(task_labels))

        # Define typing task and attach it to self

        def typing_task(text_index):

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You will now have to copy the text you see on the left side of the screen as accurately as you can.\n" \
                "Remember, the BACKSPACE key is disabled, so you cannot edit what you wrote.\n\n"
                "You will have 2 minutes and 30 seconds to write.\n"
                "Press SPACE to start.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            any_key()  # wait specifically for SPACE

            add_text_style(label = "timer_text", size = 48)

            # Ensure a large text style for the practice banner (only defined once)
            if not hasattr(self, "_practice_style_defined"):
                add_text_style(label="practice_banner", size=48)
                self._practice_style_defined = True

            # Left column text
            left_text = self.left_texts[text_index]

            # Is this the practice passage? (index 0)
            is_practice = (text_index == 0)

            def draw_practice_banner():
                if not is_practice:
                    return
                banner_w, banner_h = 420, 90
                banner = Rectangle(banner_w, banner_h, fill=(176, 0, 0))
                practice_msg = message(
                    "PRACTICE",
                    style="practice_banner",
                    align="center",
                    blit_txt=False,
                )
                banner_x = P.screen_c[0]
                banner_y = int(P.screen_y * 0.9)
                blit(banner, registration=5, location=(banner_x, banner_y))
                blit(practice_msg, registration=5, location=(banner_x, banner_y))

            def draw_left():
                msg = message(
                    left_text,
                    align="left",
                    wrap_width=int(P.screen_x * 0.45),
                    blit_txt=False
                )
                blit(msg, 1, (int(P.screen_x * 0.05), int(P.screen_y * .9)))
                # PRACTICE banner on left-draw frames too
                draw_practice_banner()

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

                timer_x = int(P.screen_x * 0.75)
                timer_y = int(P.screen_y * 0.07)

                erase_w, erase_h = 300, 80
                eraser = Rectangle(erase_w, erase_h, fill=(176, 0, 0))
                blit(eraser, 5, (timer_x, timer_y))

                sec_left = int(self.timer.remaining())
                timer_surface = message(mmss(sec_left), style="timer_text", blit_txt=False)
                blit(timer_surface, 5, (timer_x, timer_y))

                # PRACTICE banner on timer-draw frames
                draw_practice_banner()

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

            # Ensure style for practice banner
            if not hasattr(self, "_practice_style_defined"):
                add_text_style(label="practice_banner", size=48)
                self._practice_style_defined = True

            # Is this the practice sequence?
            is_practice = (targets == self.practice_spatial_order)

            def draw_practice_banner():
                if not is_practice:
                    return
                banner_w, banner_h = 420, 90
                banner = Rectangle(banner_w, banner_h, fill=(176, 0, 0))
                practice_msg = message(
                    "PRACTICE",
                    style="practice_banner",
                    align="center",
                    blit_txt=False,
                )
                banner_x = P.screen_c[0]
                banner_y = int(P.screen_y * 0.9)
                blit(banner, registration=5, location=(banner_x, banner_y))
                blit(practice_msg, registration=5, location=(banner_x, banner_y))

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "Remember in order which four squares turn black.\n\n"
                "Press SPACE to start.",
                align="center",
                blit_txt=False,
            )

            fill()
            self.draw_spatial_grid(target_task_array=None)
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            draw_practice_banner()
            flip()

            any_key()

            # --- Initial blank (1 s) ---
            start_timer = CountDown(1.0)
            while start_timer.counting():
                pump(True)
                self.draw_spatial_grid(target_task_array=None)
                draw_practice_banner()
                flip()

            # --- Target sequence ---
            for i, target in enumerate(targets):

                # 1 second target
                stim_timer = CountDown(1.0)
                while stim_timer.counting():
                    pump(True)
                    self.draw_spatial_grid(target)
                    draw_practice_banner()
                    flip()

                # 200 ms blank
                if i < len(targets) - 1:
                    isi_timer = CountDown(0.2)
                    while isi_timer.counting():
                        pump(True)
                        self.draw_spatial_grid(None)
                        draw_practice_banner()
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

            # Ensure style for practice banner
            if not hasattr(self, "_practice_style_defined"):
                add_text_style(label="practice_banner", size=48)
                self._practice_style_defined = True

            # Is this the practice word list?
            is_practice = (words == self.practice_word_list[:len(words)])

            def draw_practice_banner():
                if not is_practice:
                    return
                banner_w, banner_h = 420, 90
                banner = Rectangle(banner_w, banner_h, fill=(176, 0, 0))
                practice_msg = message(
                    "PRACTICE",
                    style="practice_banner",
                    align="center",
                    blit_txt=False,
                )
                banner_x = P.screen_c[0]
                banner_y = int(P.screen_y * 0.9)
                blit(banner, registration=5, location=(banner_x, banner_y))
                blit(practice_msg, registration=5, location=(banner_x, banner_y))

            # Instruction screen
            instr = message(
                "Remember the following list of words. \n Press SPACE to start.",
                style="default",
                align="center",
                blit_txt=False
            )

            fill()
            blit(instr, registration=5, location=P.screen_c)
            draw_practice_banner()
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
                    pump(True)
                    fill()
                    blit(word_msg, registration=5, location=P.screen_c)
                    draw_practice_banner()
                    flip()

                # --- 200 ms blank interval before next word ---
                if i < len(words) - 1:
                    gap_timer = CountDown(0.2)  # 200 ms
                    while gap_timer.counting():
                        pump(True)
                        fill()
                        draw_practice_banner()
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

        ###################################################
        # Create task demo functions
        ###################################################

        def typing_task_demo():

            # 1) Instruction screen
            instr_text = (
                "For the typing task, you will see some text on the left side of the screen, "
                "and some space on the right side to type.\n\n"
                "Your task is to copy the text you see on the left side, as accurately as you can. \n"
                "Importantly, the backspace key is disabled, so you cannot edit the text you are writing."
            )

            instr_msg = message(
                instr_text,
                align="center",
                wrap_width=int(P.screen_x * 0.8),
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=P.screen_c)
            flip()
            any_key()  # wait for participant to continue

            # 2) Static demo of the practice typing screen layout
            left_demo_text = self.left_texts[0]  # practice passage

            left_demo_msg = message(
                left_demo_text,
                align="left",
                wrap_width=int(P.screen_x * 0.45),
                blit_txt=False,
            )

            right_demo_msg = message(
                "Typed text will appear here in the real task. \n You will see a timer allowing you 2 minutes and 30 seconds to type.",
                align="left",
                blit_txt=False,
            )

            fill()

            # Left-side passage (same position as typing_task)
            blit(
                left_demo_msg,
                registration=1,
                location=(int(P.screen_x * 0.05), int(P.screen_y * 0.84)),
            )

            # Right-side "typing area" demo (approximate position of input)
            blit(
                right_demo_msg,
                registration=5,
                location=(int(P.screen_x * 0.75), int(P.screen_y * 0.22)),
            )

            flip()
            any_key()  # continue into the actual task

        self.typing_task_demo = typing_task_demo

        ######################################################
        # Verbal task demo 
        ######################################################

        def verbal_task_demo():

            verbal_instr_text = (
                "For the word task, you will be asked to look at the centre of the screen, "
                "and read some words as they appear.\n\n"
                "Your task will be to remember the words in order, so that you can recall them later.\n\n"
                "Press SPACE to see an example list of words."
            )

            verbal_instr_msg = message(
                verbal_instr_text,
                align="center",
                wrap_width=int(P.screen_x * 0.8),
                blit_txt=False,
            )

            fill()
            blit(verbal_instr_msg, registration=5, location=P.screen_c)
            flip()

            any_key()

            # Show the four practice words using your existing verbal routine
            self.verbal_task_stimuli(self.practice_word_list)

        self.verbal_task_demo = verbal_task_demo

        ######################################################
        # Spatial task demo
        ######################################################

        def spatial_task_demo():

            spatial_instr_text = (
                "For the grid task, you will be asked to look at a grid at the centre of the screen, "
                "and watch some of the squares in the grid turn black.\n\n"
                "Your task will be to remember which squares turned black in order, "
                "so you can click each square that turned black later.\n\n"
                "Press SPACE to see an example."
            )

            spatial_instr_msg = message(
                spatial_instr_text,
                align="center",
                wrap_width=int(P.screen_x * 0.8),
                blit_txt=False,
            )

            fill()
            blit(spatial_instr_msg, registration=5, location=P.screen_c)
            flip()

            any_key()
            self.spatial_search_array_stimuli(self.practice_spatial_order)

            # --- Show what the response screen looks like ---

        self.spatial_task_demo = spatial_task_demo

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

        ######################################################
        # Task Demo
        ######################################################

        demo_text = (
            "For this study, you will be asked to complete three different tasks. \n We will now show you what each of those three tasks looks like. \n After this tutorial, you will get an opportunity to practice. \n\n Press SPACE to continue."
        )

        demo_msg = message(
            demo_text, 
            align = "center", 
            wrap_width=int(P.screen_x * 0.8),
            blit_txt=False
        )

        fill()
        blit(demo_msg, registration=5, location=P.screen_c)
        flip()
        any_key()

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
        # Set the text order
        ######################################################

        if P.condition in ["1", "2", "3", "4", "5", "6"]:
            # Passage order: 1, 2, 3
            text_idx_1 = 1
            text_idx_4 = 4

            text_idx_2 = 2
            text_idx_5 = 5

            text_idx_3 = 3
            text_idx_6 = 6

            # Save passages
            t1_stimuli = self.left_texts[1]
            t4_stimuli = self.left_texts[4]

            t2_stimuli = self.left_texts[2]
            t5_stimuli = self.left_texts[5]

            t3_stimuli = self.left_texts[3]
            t6_stimuli = self.left_texts[6]

        if P.condition in ["7", "8", "9", "10", "11", "12"]:
            # Passage order: 1, 3, 2
            text_idx_1 = 1
            text_idx_4 = 4

            text_idx_2 = 3
            text_idx_5 = 6

            text_idx_3 = 2
            text_idx_6 = 5

            # Save passages
            t1_stimuli = self.left_texts[1]
            t4_stimuli = self.left_texts[4]

            t2_stimuli = self.left_texts[3]
            t5_stimuli = self.left_texts[6]

            t3_stimuli = self.left_texts[2]
            t6_stimuli = self.left_texts[5]

        if P.condition in ["13", "14", "15", "16", "17", "18"]:
            # Passage order: 2, 1, 3
            text_idx_1 = 2
            text_idx_4 = 5

            text_idx_2 = 1
            text_idx_5 = 4

            text_idx_3 =  3
            text_idx_6 = 6

            # Save passages
            t1_stimuli = self.left_texts[2]
            t4_stimuli = self.left_texts[5]

            t2_stimuli = self.left_texts[1]
            t5_stimuli = self.left_texts[4]

            t3_stimuli = self.left_texts[3]
            t6_stimuli = self.left_texts[6]

        if P.condition in ["19", "20", "21", "22", "23", "24"]:
            # Passage order: 2, 3, 1
            text_idx_1 = 2
            text_idx_4 = 5

            text_idx_2 = 3
            text_idx_5 = 6

            text_idx_3 = 1
            text_idx_6 = 4

            # Save passages
            t1_stimuli = self.left_texts[2]
            t4_stimuli = self.left_texts[5]

            t2_stimuli = self.left_texts[3]
            t5_stimuli = self.left_texts[6]

            t3_stimuli = self.left_texts[1]
            t6_stimuli = self.left_texts[4]

        if P.condition in ["25", "26", "27", "28", "29", "30"]:
            # Passage order: 3, 1, 2
            text_idx_1 = 3
            text_idx_4 = 6

            text_idx_2 = 1
            text_idx_5 = 4

            text_idx_3 = 2
            text_idx_6 = 5

            # Save passages
            t1_stimuli = self.left_texts[3]
            t4_stimuli = self.left_texts[6]

            t2_stimuli = self.left_texts[1]
            t5_stimuli = self.left_texts[4]

            t3_stimuli = self.left_texts[2]
            t6_stimuli = self.left_texts[5]

        if P.condition in ["31", "32", "33", "34", "35", "36"]:
            # Passage order: 3, 2, 1
            text_idx_1 = 3
            text_idx_4 = 6

            text_idx_2 = 2
            text_idx_5 = 5

            text_idx_3 = 1
            text_idx_6 = 4

            # Save passages
            t1_stimuli = self.left_texts[3]
            t4_stimuli = self.left_texts[6]

            t2_stimuli = self.left_texts[2]
            t5_stimuli = self.left_texts[5]

            t3_stimuli = self.left_texts[1]
            t6_stimuli = self.left_texts[4]

        ######################################################
        # Set the task order
        ######################################################

        if P.condition in ["1", "7", "13", "19", "25", "31"]:
            task_order = "csv"

        if P.condition in ["2", "8", "14", "20", "26", "32"]:
            task_order = "cvs"

        if P.condition in ["3", "9", "15", "21", "27", "33"]:
            task_order = "scv"

        if P.condition in ["4", "10", "16", "22", "28", "34"]:
            task_order = "svc"

        if P.condition in ["5", "11", "17", "23", "29", "35"]:
            task_order = "vcs"

        if P.condition in ["6", "12", "18", "24", "30", "36"]:
            task_order = "vsc"

        ######################################################
        # Control, spatial, verbal
        ######################################################

        if task_order == "csv": 

            self.typing_task_demo()
            self.spatial_task_demo()
            self.verbal_task_demo()

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the task demo.\n Press SPACE to begin the practice.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            any_key()  # wait specifically for SPACE

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

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the PRACTICE trials.\n Press SPACE to begin the study.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            ####################
            # First run
            ####################

            # Run the typing task (control, no working memory task)
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)

            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)
            
            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)
            
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)    

            ####################
            # Second run
            ####################

            # Run the typing task (control, no working memory task)
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)

            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)
            
            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)
            
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)            

        ######################################################
        # Control, verbal, spatial
        ######################################################

        if task_order == "cvs": 

            self.typing_task_demo()
            self.verbal_task_demo()
            self.spatial_task_demo()

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the task demo.\n Press SPACE to begin the practice.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            any_key()  # wait specifically for SPACE

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

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the PRACTICE trials.\n Press SPACE to begin the study.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            ####################
            # First run
            ####################

            # Run the typing task (control, no working memory task)
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)

            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)   
            
            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)
            
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 

            ####################
            # Second run
            ####################

            # Run the typing task (control, no working memory task)
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)

            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 
            
            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)
            
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)   

        ######################################################
        # Spatial, verbal, control
        ######################################################

        if task_order == "svc": 

            self.spatial_task_demo()
            self.verbal_task_demo()
            self.typing_task_demo()

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the task demo.\n Press SPACE to begin the practice.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            any_key()  # wait specifically for SPACE

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

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the PRACTICE trials.\n Press SPACE to begin the study.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            ####################
            # First run
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)

            # Run the typing task (control, no working memory task)
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)

            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)   
            
            # Control
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            ####################
            # Second run
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)

            # Run the typing task (control, no working memory task)
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)

            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 
            
            # Control
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

        ######################################################
        # Spatial, control, verbal
        ######################################################

        if task_order == "scv": 

            self.spatial_task_demo()
            self.typing_task_demo()
            self.verbal_task_demo()

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the task demo.\n Press SPACE to begin the practice.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            any_key()  # wait specifically for SPACE

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

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the PRACTICE trials.\n Press SPACE to begin the study.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            ####################
            # First run
            ####################

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)

            # Run the typing task (control, no working memory task)
            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 

            # Control
            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)
            
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
            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

            # Control
            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)
            
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 

        ######################################################
        # Verbal, spatial, control
        ######################################################

        if task_order == "vsc": 

            self.verbal_task_demo()
            self.spatial_task_demo()
            self.typing_task_demo()

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the task demo.\n Press SPACE to begin the practice.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            any_key()  # wait specifically for SPACE

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

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the PRACTICE trials.\n Press SPACE to begin the study.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            ####################
            # First run
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)

            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)  

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)

            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp) 
            
            # Control
            typed = self.run_typing_block(text_idx_3)
            all_typed.append((text_idx_3, typed))

            ####################
            # Second run
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.second_word_list)

            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)

            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)
            
            # Control
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

        ######################################################
        # Verbal, control, spatial
        ######################################################

        if task_order == "vcs": 

            self.verbal_task_demo()
            self.typing_task_demo()
            self.spatial_task_demo()

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the task demo.\n Press SPACE to begin the practice.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            any_key()  # wait specifically for SPACE

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

            # --- Instruction screen over blank grid ---
            instr_msg = message(
                "You have completed the PRACTICE trials.\n Press SPACE to begin the study.",
                align="center",
                blit_txt=False,
            )

            fill()
            blit(instr_msg, registration=5, location=(P.screen_c[0], int(P.screen_y * 0.25)))
            flip()

            ####################
            # First run
            ####################

            # Run the verbal task
            #word_list = ["Table", "House", "Garden", "Pencil"] # Just an example
            self.verbal_task_stimuli(self.first_word_list)

            typed = self.run_typing_block(text_idx_1)
            all_typed.append((text_idx_1, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp)  

            # Control
            typed = self.run_typing_block(text_idx_2)
            all_typed.append((text_idx_2, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.first_spatial_order)
            
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

            typed = self.run_typing_block(text_idx_4)
            all_typed.append((text_idx_1, typed))

            for i in range(1, 5): 
                resp = self.verbal_task_response(str(i))
                verbal_responses.append(resp) 

            # Control
            typed = self.run_typing_block(text_idx_5)
            all_typed.append((text_idx_2, typed))

            # Run the spatial task
            self.spatial_search_array_stimuli(self.second_spatial_order)            
            
            typed = self.run_typing_block(text_idx_6)
            all_typed.append((text_idx_3, typed))

            for n in range(1, 5): 
                resp = self.spatial_task_response_collector(which_n=n)
                spatial_responses.append(resp)

        ###############################################################
        # Survey question queries
        ###############################################################

        q = user_queries.survey1[0]
        self.centre_query(q)
        survey1 = query(q)

        q = user_queries.survey2[0]
        self.centre_query(q)
        survey2 = query(q)

        q = user_queries.survey3[0]
        self.centre_query(q)
        survey3 = query(q)

        q = user_queries.survey4[0]
        self.centre_query(q)
        survey4 = query(q)

########################################################   
        # ---- DATA UNPACKING / SAFETY ----
########################################################

        # Typed text assignments and responses
        typed_practice_stimuli = self.left_texts[0]
        typed_practice1 = all_typed[0][1] if len(all_typed) > 0 else None
        typed_practice2 = all_typed[1][1] if len(all_typed) > 1 else None
        typed_practice3 = all_typed[2][1] if len(all_typed) > 2 else None
        t1_stimuli = t1_stimuli
        typed1 = all_typed[3][1] if len(all_typed) > 3 else None
        t2_stimuli = t2_stimuli
        typed2 = all_typed[4][1] if len(all_typed) > 4 else None
        t3_stimuli = t3_stimuli
        typed3 = all_typed[5][1] if len(all_typed) > 5 else None
        t4_stimuli = t4_stimuli
        typed4 = all_typed[6][1] if len(all_typed) > 6 else None
        t5_stimuli = t5_stimuli
        typed5 = all_typed[7][1] if len(all_typed) > 7 else None
        t6_stimuli = t6_stimuli
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
            "t1_stimuli": t1_stimuli, 
            "typed1": typed1,
            "t2_stimuli": t2_stimuli, 
            "typed2": typed2,
            "t3_stimuli": t3_stimuli, 
            "typed3": typed3,
            "t4_stimuli": t4_stimuli, 
            "typed4": typed4,
            "t5_stimuli": t5_stimuli, 
            "typed5": typed5,
            "t6_stimuli": t6_stimuli, 
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

            "survey1": survey1, 
            "survey2": survey2, 
            "survey3": survey3, 
            "survey4": survey4

        }
    
    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass

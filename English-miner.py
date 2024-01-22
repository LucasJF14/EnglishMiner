# Lukas Flasik
# All images used in this game are from Internet
# This game is inspired by the original "Gold Miner" game.
# Dependency : pygame/gamebox

import pygame
import gamebox
import random
import math

# 0-preparation
# general
camera = gamebox.Camera(1000, 700)
selected_button = 0
score = 0
radins = -70
chain_distance = 30
value_caught = 0
pict_index = 0
speed = 5
weight_letter_caught = speed + 5
counter = 5
level = 1
slova_goal = ["DOKTOR", "POLICAJT", "KABAT", "SUKŇA", "LAMPA", "POSTEĽ", "ZAJAC", "MAČKA", "OTEC", "MAMA", "RUKA", "HLAVA"]
english_goal = ["DOCTOR", "POLICEMAN", "COAT", "SKIRT", "LAMP", "BED", "RABBIT", "CAT", "DAD", "MOTHER", "HAND", "HEAD"]
scene = 0  # scene index: 0 = starting scene 1 = game rule scene 2 = game scene 3 = shop scene 4 = you die
index = 0
popped_up_word_counterdown = 16
sound = gamebox.load_sound("mining_music.wav")
sound.play()

# item references
item_caught = gamebox.from_color(500, 100, "orange", 1, 1)
picture_list = ["picture/background.png", "picture/background2.png", "picture/machinerope.png", "picture/Starting screen.png", "picture/intro.png"]
letter_list = ["picture/Pismena/A.png", "picture/Pismena/B.png","picture/Pismena/C.png", "picture/Pismena/D.png",
               "picture/Pismena/E.png", "picture/Pismena/F.png","picture/Pismena/G.png", "picture/Pismena/H.png",
               "picture/Pismena/I.png", "picture/Pismena/J.png","picture/Pismena/K.png", "picture/Pismena/L.png",
               "picture/Pismena/M.png", "picture/Pismena/N.png","picture/Pismena/O.png", "picture/Pismena/P.png",
               "picture/Pismena/Q.png", "picture/Pismena/R.png","picture/Pismena/S.png", "picture/Pismena/T.png",
               "picture/Pismena/U.png", "picture/Pismena/V.png", "picture/Pismena/W.png","picture/Pismena/X.png",
               "picture/Pismena/Y.png", "picture/Pismena/Z.png"]
letter_values = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
initial_position = []

# animation set up
frame = 0
frame2 = 0
chain = gamebox.load_sprite_sheet("picture/animation1.png", 1, 7)
character2 = gamebox.load_sprite_sheet("picture/character1_1.png", 1, 7)
character3 = gamebox.load_sprite_sheet("picture/character1_2.png", 1, 8)
chainhead = gamebox.from_image(300, 500, chain[frame])
character = gamebox.from_image(475, 50, character2[frame2])

# booleans pre chain
direction_left_to_right = True
chain_thrown_out = False
chain_thrown_out_away = True
chain_thrown_out_catchsomething = False

# items
time = False

# lists
caught_item_indices = []
caught_letters = []

def tick(keys):
    # 1-global-set up all required data
    global radins, score, direction_left_to_right, chain_thrown_out, chain_thrown_out_away, chain_distance, chainhead, caught_word
    global chain_thrown_out_catchsomething, item_caught, weight_letter_caught, speed, background, initial_position, index_in_letter_list, letters
    global value_caught, pict_index, counter, level, frame, frame2, scene, index, english_goal, slova_goal, caught_letters
    global popped_up_word_counterdown, selected_button, captured_letters, letter_values, caught_item_indices, current_word_for_level
    camera.clear('grey')

    # differetiate on scenes
    if scene == 0:
        screen = gamebox.from_image(500, 350, picture_list[3])
        screen.scale_by(0.74)
        camera.draw(screen)
        camera.draw(gamebox.from_text(500, 500, "Stlačte SPACE aby ste mohli začať hru", "arial", 30, "red"))

        # animations
        frame += 1
        if frame == 7:
            frame = 0
        chainhead.rotate(-90)
        chainhead.image = chain[frame]
        if index == 0:
            chainhead = gamebox.from_image(225, 558, chain[frame])
        chainhead.scale_by(0.8)
        chainhead.rotate(90)
        camera.draw(chainhead)

        if pygame.K_LEFT in keys and index == 1:
            index = 0
        if pygame.K_RIGHT in keys and index == 0:
            index = 1
        if pygame.K_SPACE in keys and index == 0:
            scene = 2
            level_generation(level)
        if pygame.K_SPACE in keys and index == 1:
            keys = []
            scene = 1

    if scene == 1:
        picture = gamebox.from_image(500, 350, picture_list[2])
        picture.scale_by(4.5)
        camera.draw(picture)
        if pygame.K_SPACE in keys:
            keys = []
            scene = 0

    counter -= 1
    if scene == 2:
        machine = gamebox.from_image(500, 50, picture_list[2])
        mine = gamebox.from_image(500, 387.5, picture_list[0])
        surface = gamebox.from_image(500, 38.5, picture_list[1])
        surface.scale_by(0.45)

        mine.scale_by(0.71)
        machine.scale_by(0.30)

        camera.draw(mine)
        camera.draw(surface)
        camera.draw(machine)

        # animations
        frame += 1
        if frame == 7:
            frame = 0
        chainhead.image = chain[frame]

        if chain_thrown_out == False:
            character = gamebox.from_image(455, 50, character2[int(frame2)])
            frame2 += 0.5
            if frame2 == 7:
                frame2 = 0
            character.image = character2[int(frame2)]
        else:
            character = gamebox.from_image(455, 50, character3[int(frame2)])
            frame2 += 0.5
            if frame2 == 8:
                frame2 = 0
            character.image = character3[int(frame2)]

        camera.draw(character)

        # 2-when chain available
        # degree regular changes
        if chain_thrown_out == False:
            if popped_up_word_counterdown >= 25:
                if direction_left_to_right == True:
                    radins += 3
                else:
                    radins -= 3

            if radins <= -70:
                direction_left_to_right = True
            if radins >= 70:
                direction_left_to_right = False

            # chain head displays
            chainhead.x = 500 + math.sin(radins / 57.29) * 75
            chainhead.y = 75 + math.cos(radins / 57.29) * 75

            camera.draw(chainhead)

            # chains display
            for i in range(0, 25):
                item = gamebox.from_color(500 + math.sin(radins / 57.29) * 2.5 * i,
                                          75 + math.cos(radins / 57.29) * 2.5 * i, "orange", 5, 5)
                camera.draw(item)

        # 3-chain_thrown_out
        # set up throwing chain
        if pygame.K_DOWN in keys and chain_thrown_out == False and popped_up_word_counterdown >= 16:
            chain_thrown_out = True
            chain_thrown_out_away = True
            chain_thrown_out_catchsomething = False
            chain_distance = 30
            character.scale_by(1.2)

        # chain animation
        if chain_thrown_out == True and chain_thrown_out_away == True:
            chain_distance += speed
            for i in range(1, chain_distance):
                item = gamebox.from_color(500 + math.sin(radins / 57.29) * 2.5 * i,
                                          75 + math.cos(radins / 57.29) * 2.5 * i, "orange", 5, 5)
                camera.draw(item)
            chainhead.x = 500 + math.sin(radins / 57.29) * (10 + 2.5 * chain_distance)
            chainhead.y = 75 + math.cos(radins / 57.29) * (10 + 2.5 * chain_distance)
            camera.draw(chainhead)

        if chain_thrown_out == True and chain_thrown_out_away == False:
            chain_distance -= weight_letter_caught
            for i in range(1, chain_distance):
                item = gamebox.from_color(500 + math.sin(radins / 57.29) * 2.5 * i,
                                          75 + math.cos(radins / 57.29) * 2.5 * i, "orange", 5, 5)
                camera.draw(item)
            chainhead.x = 500 + math.sin(radins / 57.29) * (10 + 2.5 * chain_distance)
            chainhead.y = 75 + math.cos(radins / 57.29) * (10 + 2.5 * chain_distance)
            camera.draw(chainhead)

        # boolans for throw/retriving chains
        if chainhead.x < 0 or chainhead.x > 1000 or chainhead.y > 700:
            chain_thrown_out_away = False

        if chain_distance <= 29 and chain_thrown_out == True:
            if chain_thrown_out_catchsomething == True:
                if value_caught != 0:
                    popped_up_word_counterdown = 1
                score += value_caught
                chain_thrown_out_catchsomething = False
            chain_thrown_out = False
            character.scale_by(0.833)
            frame2 = 0  # prevent "out of range" error
            weight_letter_caught = speed + 5

        # 4-golds processing
        # catching items
        # In your tick function
        zoz = []
        for let, letter_value in letters.items():
            if let.touches(chainhead) and chain_thrown_out_catchsomething == False:
                chain_thrown_out_away = False
                chain_thrown_out_catchsomething = True
                weight_letter_caught = speed - 2
                pict_index = 1
                value_caught = 1

                # Update the position of the caught letter to follow the chainhead
                let.x = chainhead.x
                let.y = chainhead.y

                # Check if the chain returns to its starting point
                if chain_thrown_out_away == False:
                    # Iterate through the caught letters
                    for caught_let in letters:
                        # Check if the caught letter is within a certain range of the chainhead
                        if caught_let.touches(chainhead):
                            # Remove the caught letter
                            zoz.append(caught_let)

                caught_letters.append(letter_value)


        # Remove caught letters from the original letters dictionary
        for i in zoz:
            del letters[i]

        print(caught_letters, letters)

        # Draw the caught letters
        for letter_value in caught_letters:
            item = gamebox.from_image(500 + math.sin(radins / 57.29) * 2.5 * (chain_distance + 10),
                                      75 + math.cos(radins / 57.29) * 2.5 * (chain_distance + 10),
                                      letter_list[letter_values.index(letter_value)])
            camera.draw(item)

        # Draw the remaining letters
        for let in letters:
            camera.draw(let)

        # 6-score/time/environments display
        camera.draw(
            gamebox.from_text(750, 10, "Level: " + str(level) + " Slovo ktoré treba preložiť do angličtiny: " + slova_goal[level - 1], "arial",
                              24, "white"))
        caught_word = ''.join(caught_letters)
        if len(caught_letters) == 0:
            camera.draw(gamebox.from_text(135, 25, "Slovo: ", "arial", 24, "yellow"))
        else:
            camera.draw(gamebox.from_text(135, 25, "Slovo: " + caught_word, "arial", 24, "yellow"))
        print("Caught Word:", caught_word)

        if counter > 0:
            camera.draw(gamebox.from_text(145, 55, "Ostávajúci čas: " + str(int(counter / 15)), "arial", 22, "black"))
        camera.draw(gamebox.from_color(500, 75, "orange", 40000, 10))

        # Adding letters together
        popped_up_word_counterdown += 1
        if popped_up_word_counterdown <= 15:
            if value_caught > 0:
                camera.draw(gamebox.from_text(300, 25, "+" + str(value_caught), "arial", 30, "green", bold=True))
            else:
                camera.draw(gamebox.from_text(300, 25, str(value_caught), "arial", 30, "red", bold=True))

        elif popped_up_word_counterdown == 16:
            value_caught = 0

        # 7 transition/ after timeout
        if counter == 0:
            if caught_word.lower() == english_goal[level - 1].lower():
                level += 1
                # Reset caught_word to an empty string
                caught_word = ''
                # set value to default
                level_generation(level)
                speed = 5
                scene = 3
                chain_thrown_out_catchsomething = False
                chain_thrown_out = False
                character.scale_by(0.833)
                frame2 = 0  # prevent "out of range" error
                weight_letter_caught = speed + 5
            else:
                scene = 4

    # scene 3 : posun v v leveli
    if scene == 3:
        camera.draw(gamebox.from_text(500, 200, "Continue", "arial", 30, "red"))
        camera.draw(gamebox.from_text(500, 250, "Quit Game", "arial", 30, "red"))
        camera.draw(gamebox.from_text(500, 300, "The correct word was " + english_goal[level - 2], "arial", 30, "red"))

        camera.draw(gamebox.from_text(430, 200 + selected_button * 50, ">", "arial", 30, "red"))

        if pygame.K_UP in keys:
            selected_button = max(selected_button - 1, 0)
            keys = []
        if pygame.K_DOWN in keys:
            selected_button = min(selected_button + 1, 1)
            keys = []
        if pygame.K_RETURN in keys:
            if selected_button == 0:
                # Restart the game
                caught_letters.clear()
                scene = 2
                level_generation(level)
                keys = []
            elif selected_button == 1:
                # Quit the game
                pygame.quit()
                quit()

    # scena 4 = prehral si
    if scene == 4:
        camera.draw(gamebox.from_text(500, 350, "SLOVÍČKO BOLO NESPRÁVNE ZLOŽENE - PREHRAL SI !!", "arial", 40, "red"))
        camera.draw(gamebox.from_text(500, 400, "Restart", "arial", 30, "red"))
        camera.draw(gamebox.from_text(500, 450, "Quit Game", "arial", 30, "red"))

        # Draw arrows next to the selected button
        camera.draw(gamebox.from_text(430, 400 + selected_button * 50, ">", "arial", 30, "red"))

        if pygame.K_UP in keys:
            selected_button = max(selected_button - 1, 0)
            keys = []
        if pygame.K_DOWN in keys:
            selected_button = min(selected_button + 1, 1)
            keys = []
        if pygame.K_RETURN in keys:
            if selected_button == 0:
                # Restart the game
                caught_letters.clear()
                level = 1
                scene = 0
                level_generation(level)
            elif selected_button == 1:
                # Quit the game
                pygame.quit()
                quit()


    camera.display()

def get_level_data(level):
    # Word for the current level
    word_for_level = english_goal[level - 1]

    # Letters for the current level
    letters_for_level = []
    for letter in word_for_level:
        if letter.isalpha() and letter.isupper():
            letter_index = ord(letter) - ord('A')
            if 0 <= letter_index < len(letter_list):
                letters_for_level.append(letter_list[letter_index])

    return word_for_level, letters_for_level
def level_generation(level):
    global counter, letters, initial_position, caught_word
    caught_word = ""
    letters = {}
    initial_position = []

    # item evaluation
    if time == True:
        counter = 1500
    else:
        counter = 1500

    word_for_level, letters_for_level = get_level_data(level)

    # Add letters from the word to letter
    print(f"Lettter for level: {letters_for_level}")
    for i in letters_for_level:
        print(i[16])

    for letter_image in letters_for_level:
        item = gamebox.from_image(random.randint(50, 950), random.randint(200, 690), letter_image)
        letters[item] = letter_image[16]
        initial_position.append((item.x, item.y))
        print(f"{item}: {initial_position}")

    # Add random letters for levels
    for i in range(2):
        random_letter_index = random.randint(0, 24)
        letter_image = letter_list[random_letter_index]
        item = gamebox.from_image(random.randint(50, 950), random.randint(200, 690), letter_image)

        # Assign a letter value to the item based on the random letter index
        item_value = letter_values[random_letter_index]

        letters[item] = item_value
        initial_position.append((item.x, item.y))

ticks_per_second = 40
# keep this line the last one in your program
gamebox.timer_loop(ticks_per_second, tick)
import pygame
from pygame.locals import *
import os
import math
from config import *
import json



# Define helper functions
def load_image(name, colorkey = None):
    fullname = os.path.join('data/img/', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()

    return image # , image.get_rect()


def exit_game(screen):
    # clear the screen
    screen.fill(BACKGROUND)
    pygame.display.update()

    pause = 0
    
    # pause music / sfx
    pygame.mixer.pause()

    # display message to confirm exit
    exit_msg = game_font.render('Quitting ... ', False, INTERFACE_SEC)
    question_msg = game_font.render('Are You Sure?', False, INTERFACE_SEC)
    confirm_msg = game_font.render('(Y/N)', False, INTERFACE_SEC)
   
    exit_msg_pos = (SCREENSIZE[0] // 2 - (exit_msg.get_width() // 2),
                        SCREENSIZE[1] // 2 - (exit_msg.get_height() // 2))
    
    question_msg_pos = (SCREENSIZE[0] // 2 - (question_msg.get_width() // 2),
                        SCREENSIZE[1] // 2 - (question_msg.get_height() // 2)+ exit_msg.get_height()) 
   
    confirm_msg_pos = (SCREENSIZE[0] // 2 - (confirm_msg.get_width() // 2),
                        SCREENSIZE[1] // 2 - (confirm_msg.get_height() // 2) + exit_msg.get_height() + question_msg.get_height() )
    
    screen.blit(exit_msg, exit_msg_pos)
    screen.blit(question_msg, question_msg_pos)
    screen.blit(confirm_msg, confirm_msg_pos)
    pygame.display.update()

    # wait for player to confirm exit or not
    while pause == 0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_y:
                    exit()
                if event.key == K_n:
                    pause = -1

    # resume music ifplayer not exiting
    pygame.mixer.unpause()


def pause_game(screen):
    pause = 0
    
    # pause music / sfx
    pygame.mixer.pause()

    # display message that game is paused
    pause_msg = game_font.render('GAME PAUSED', False, INTERFACE_SEC)
    confirm_msg = game_font.render('PRESS \'P\' TO RESUME', False, INTERFACE_SEC)
    pause_msg_pos = (SCREENSIZE[0] // 2 - (pause_msg.get_width() // 2),
                        SCREENSIZE[1] // 2 - (pause_msg.get_height() // 2))
    confirm_msg_pos = (SCREENSIZE[0] // 2 - (confirm_msg.get_width() // 2),
                        SCREENSIZE[1] // 2 - (confirm_msg.get_height() // 2) + pause_msg.get_height())
    screen.blit(pause_msg, pause_msg_pos)
    screen.blit(confirm_msg, confirm_msg_pos)
    pygame.display.update()

    # wait for player to un-pause
    while pause == 0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause = -1

    # resume music
    pygame.mixer.unpause()


def distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def check_collisions(missile_list, explosion_list, city_list):
    score = 0

    for explosion in explosion_list:
        for missile in missile_list[:]:
            if explosion.get_radius() > distance(explosion.get_center(), missile.get_pos()):
                score += missile.get_points() * explosion.get_points_multiplier()
                missile_list.remove(missile)
        for city in city_list[:]:
            if explosion.get_radius() > distance(explosion.get_center(), city.get_pos()):
                city.set_destroyed(True)    # might not be needed if I just remove city from list
                city_list.remove(city)

    return score


def load_scores(file):
    # open a json file containing scores and return dict
    with open(file) as f:
        return json.load(f)
    

def update_high_scores(score, name, high_scores):
    # check if score made it into the top 10 and determine position
    score_pos = check_high_score(score, high_scores)
    
    # if it did make top 10, re-order the records
    if score_pos > 0:
        max_pos = 10
        
        # loop from max_pos up until I get to score_pos
        for pos in range(max_pos, score_pos, -1):
            # move the score down a pos
            if pos <= max_pos and pos > 1:
                high_scores[str(pos)]["name"] = high_scores[str(pos - 1)]["name"]
                high_scores[str(pos)]["score"] = high_scores[str(pos - 1)]["score"]

        # insert the new score
        high_scores[str(score_pos)]["name"] = name
        high_scores[str(score_pos)]["score"] = int(score)
        
    return high_scores


def check_high_score(score, high_scores):
    score_pos = 0

    # check if score made it into the top 10 and determine position
    for pos, record in high_scores.items():
        if score > int(record["score"]) and score_pos == 0:
            score_pos = int(pos)
    
    return score_pos

    
def save_high_scores(file, high_scores):
    # save high-scores to file
    j = json.dumps(high_scores)
    f = open(file, "w")
    f.write(j)
    f.close()


def show_high_scores(screen, high_scores):
    # clear the screen
    screen.fill(BACKGROUND)
    pygame.display.update()

    pause = 0

    # generate heading msg, position, blit
    high_score_heading = game_font.render('HIGH SCORES', False, INTERFACE_PRI)
    text_height = high_score_heading.get_height()
    text_y_pos_multiplier = 7
    wide_score = 0
    high_score_heading_pos = (SCREENSIZE[0] // 2 - (high_score_heading.get_width() // 2),
                            SCREENSIZE[1] // 2 - (text_height * text_y_pos_multiplier))
    screen.blit(high_score_heading, high_score_heading_pos)
    text_y_pos_multiplier -= 2

    # loop through dict 'high_scores'
    for pos, record in high_scores.items():
        if len(pos) == 1:
            pos = " " + pos
        record["score"] = str(record["score"])
        if wide_score <= len(record["score"]):
            wide_score = len(record["score"])
        else:
            record["score"] = (" " * (wide_score - len(record["score"]))) + record["score"]
        score_text = game_font.render(pos + " " + record["name"] + " " + record["score"], False, INTERFACE_SEC)
        score_text_pos = (SCREENSIZE[0] // 2 - (score_text.get_width() // 2),
                            SCREENSIZE[1] // 2 - (text_height * text_y_pos_multiplier))
        screen.blit(score_text, score_text_pos)
        text_y_pos_multiplier -= 1
    
    # generate instruction msg, position, blit
    text_y_pos_multiplier -= 1
    high_score_msg = game_font.render('PRESS \'SPACE\' TO CONTINUE', False, INTERFACE_SEC)
    high_score_msg_pos = (SCREENSIZE[0] // 2 - (high_score_msg.get_width() // 2),
                            SCREENSIZE[1] // 2 - (text_height * text_y_pos_multiplier))
    screen.blit(high_score_msg, high_score_msg_pos)

    # update the display
    pygame.display.update()

    # infinite loop to listen / wait for continue
    while pause == 0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pause = -1
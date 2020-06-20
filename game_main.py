#!/usr/bin/env python3

import random

import pygame
import winsound

class game_env:
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255,255,0)
        self.BLUE = (3, 248, 252)
        self.ORANGE = (247, 165, 0)
        self.LIME = (0, 247, 66)
        self.PURPLE = (155, 46, 201)
        self.TEAL = (0,128,128)
        pygame.init()
        pygame.mixer.init(22050, -8, 16, 65536 )
        self.size = (530, 700)
        self.block_size = 30
        self.screen = pygame.display.set_mode(self.size)
        self.block_list = []
        self.collision_list = []
        self.new_block = True
        self.block_call = [self.long_block, self.square_block, self.right_L, self.left_L, self.right_S, self.left_S, self.t_block]
        self.block_index = random.randint(0,len(self.block_call)-1)
        self.block_index_next = random.randint(0,len(self.block_call)-1)
        self.rot_pos = 0
        self.long_blocks = []
        self.RL_blocks = []
        self.LL_blocks = []
        self.RS_blocks = []
        self.LS_blocks = []
        self.t_blocks = []
        self.dead = False
        self.start_down = 0
        self.slow_speed = 600
        self.fast_speed = 80
        self.start_y = 78
        self.DARK_BLUE = (3, 86, 252)
        self.move_down_time = self.slow_speed
        pygame.display.set_caption("PyTetris")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        self.rect_x = 250
        self.rect_y = self.start_y
        self.rect_change_y = 2
        self.start_right = pygame.time.get_ticks()
        self.start_left = pygame.time.get_ticks()
        self.pause = False
        self.pts = 0
        self.move_left = False
        self.move_right = False


        pygame.mixer.music.load('airtone.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        while not done:
            font = pygame.font.Font('freesansbold.ttf', 15) 
  
            # create a text suface object, 
            # on which text is drawn on it. 
            pts_string = 'Score: ' +str(self.pts)
            text = font.render( pts_string,True, self.WHITE, self.BLACK) 

            # create a rectangular object for the 
            # text surface object 
            textRect = text.get_rect()  

            # set the center of the rectangular object. 
            textRect.center = (440, 270) 
            self.block_dict = {0:self.long_blocks, 1:None, 2: self.RL_blocks, 3: self.LL_blocks, 4: self.RS_blocks, 5: self.LS_blocks, 6:self.t_blocks}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.move_left = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.move_right = True
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.rotate()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.move_down_time = self.fast_speed
                    elif event.key == pygame.K_p:
                        if not self.pause:
                            self.pause = True
                            self.paused()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.move_down_time = self.slow_speed
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                         self.move_left = False
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.move_right = False                    
            if self.move_left:
                can_move = self.checkLeft()
                if can_move:
                    if pygame.time.get_ticks() - self.start_left >= 75:
                        self.rect_x -= self.block_size
                        self.start_left = pygame.time.get_ticks()
            if self.move_right:
                can_move = self.checkRight()
                if can_move:
                    if pygame.time.get_ticks() - self.start_right >= 75:
                        self.rect_x += self.block_size
                        self.start_right = pygame.time.get_ticks()             
            self.screen.fill(self.BLACK)
            self.screen.blit(text,textRect)
            pygame.draw.rect(self.screen, self.WHITE, [98, 48, 304, 602])
            pygame.draw.rect(self.screen, self.BLACK, [100, 50, 300, 598])
            if self.new_block == True:
                self.block_index = self.block_index_next
                self.block_index_next = random.randint(0,len(self.block_call)-1)
                self.new_block = False
            self.show_block()
            self.checkTop()
            if pygame.time.get_ticks() - self.start_down > self.move_down_time:
                self.rect_y += 30
                self.start_down = pygame.time.get_ticks()
            self.block_call[self.block_index]()

            
            for item in self.block_list:
                pygame.draw.rect(self.screen, item[2], [item[0],
                                item[1], self.block_size, self.block_size])
            #self.checkBounds() 
            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()

    def square_block(self):
        pygame.draw.rect(self.screen, self.YELLOW, [self.rect_x, self.rect_y, self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.YELLOW, [self.rect_x+self.block_size, self.rect_y, self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.YELLOW, [self.rect_x+self.block_size, self.rect_y+self.block_size, self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.YELLOW, [self.rect_x, self.rect_y+self.block_size, self.block_size, self.block_size])
        #self.rect_y += self.rect_change_y
        overlap = False
        y_overlap = None
        for item in self.block_list:
            if self.rect_y+2*self.block_size >= item[1] and self.rect_y+2*self.block_size < item[1]+self.block_size and (self.rect_x == item[0] or self.rect_x+self.block_size == item[0]):
                overlap = True
                y_overlap = item[1]-2*self.block_size
        if self.rect_y+2*self.block_size >= 648 or overlap == True:
            if not y_overlap:
                y_overlap = 648-2*self.block_size
            self.block_list.append((self.rect_x, y_overlap, self.YELLOW))
            self.block_list.append((self.rect_x+self.block_size, y_overlap+self.block_size, self.YELLOW))
            self.block_list.append((self.rect_x, y_overlap+self.block_size, self.YELLOW))
            self.block_list.append((self.rect_x+self.block_size, y_overlap, self.YELLOW))
            self.rect_y = self.start_y
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            self.checkTetris()
    def long_block(self):
        first = True
        for i in range(0,2):
            if self.rot_pos == 0 or self.rot_pos == 2:
                self.long_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x, self.rect_y+self.block_size), 
                                    (self.rect_x, self.rect_y+2*self.block_size), 
                                    (self.rect_x, self.rect_y+3*self.block_size)]
            else:
                self.long_blocks = [(self.rect_x-self.block_size, self.rect_y), 
                                    (self.rect_x, self.rect_y), 
                                    (self.rect_x+self.block_size, self.rect_y),
                                    (self.rect_x+2*self.block_size, self.rect_y)]
            if first:
                self.checkBounds()
                first = False
        pygame.draw.rect(self.screen, self.TEAL, [self.long_blocks[0][0], self.long_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.TEAL, [self.long_blocks[1][0], self.long_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.TEAL, [self.long_blocks[2][0], self.long_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.TEAL, [self.long_blocks[3][0], self.long_blocks[3][1], self.block_size, self.block_size])
        #self.rect_y += self.rect_change_y
        overlap = False
        y_overlap = None
        for block in self.long_blocks:
            for item in self.block_list:
                if block[1]+self.block_size >= item[1] and block[1] <= item[1] and block[0] == item[0]:
                    y_overlap = item[1]-4*self.block_size
                    overlap = True
            if block[1]+self.block_size >= 648:
                overlap = True
        if overlap == True:
            self.block_list.append((self.long_blocks[0][0], self.long_blocks[0][1], self.TEAL))
            self.block_list.append((self.long_blocks[1][0], self.long_blocks[1][1], self.TEAL))
            self.block_list.append((self.long_blocks[2][0], self.long_blocks[2][1], self.TEAL))
            self.block_list.append((self.long_blocks[3][0], self.long_blocks[3][1], self.TEAL))
            self.rect_y = self.start_y
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            self.checkTetris()
            return 0 
    def right_L(self):
        first = False
        for i in range(0,2):
            if self.rot_pos == 0:
                self.RL_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y), 
                                    (self.rect_x-2*self.block_size, self.rect_y), 
                                    (self.rect_x, self.rect_y+-self.block_size)]
            elif self.rot_pos == 1:
                self.RL_blocks = [(self.rect_x, self.rect_y-self.block_size), 
                                    (self.rect_x, self.rect_y), 
                                    (self.rect_x, self.rect_y+self.block_size),
                                    (self.rect_x+self.block_size, self.rect_y+self.block_size)]
            elif self.rot_pos == 2:
                self.RL_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y+self.block_size), 
                                    (self.rect_x-self.block_size, self.rect_y),
                                    (self.rect_x+self.block_size, self.rect_y)]
            elif self.rot_pos == 3:
                self.RL_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y-self.block_size), 
                                    (self.rect_x, self.rect_y-self.block_size),
                                    (self.rect_x, self.rect_y+self.block_size)]
            if first:
                self.checkBounds()
                first = False
        pygame.draw.rect(self.screen, self.ORANGE, [self.RL_blocks[0][0], self.RL_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.ORANGE, [self.RL_blocks[1][0], self.RL_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.ORANGE, [self.RL_blocks[2][0], self.RL_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.ORANGE, [self.RL_blocks[3][0], self.RL_blocks[3][1], self.block_size, self.block_size])
        #self.rect_y += self.rect_change_y
        overlap = False
        y_overlap = None
        for block in self.RL_blocks:
            for item in self.block_list:
                if block[1]+self.block_size >= item[1] and block[1] <= item[1] and block[0] == item[0]:
                    y_overlap = item[1]-4*self.block_size
                    overlap = True
            if block[1]+self.block_size >= 648:
                overlap = True
        if overlap == True:
            self.block_list.append((self.RL_blocks[0][0], self.RL_blocks[0][1], self.ORANGE))
            self.block_list.append((self.RL_blocks[1][0], self.RL_blocks[1][1], self.ORANGE))
            self.block_list.append((self.RL_blocks[2][0], self.RL_blocks[2][1], self.ORANGE))
            self.block_list.append((self.RL_blocks[3][0], self.RL_blocks[3][1], self.ORANGE))
            self.rect_y = self.start_y
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            self.checkTetris()
            return 0     
    def left_L(self):
        first = True
        one_sec = False
        for i in range(0,2):
            if self.rot_pos == 0:
                self.LL_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x+self.block_size, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y-self.block_size)]
            elif self.rot_pos == 1:
                self.LL_blocks = [(self.rect_x, self.rect_y+self.block_size), 
                                    (self.rect_x, self.rect_y), 
                                    (self.rect_x, self.rect_y-self.block_size),
                                    (self.rect_x+self.block_size, self.rect_y-self.block_size)]
            elif self.rot_pos == 2:
                self.LL_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x+self.block_size, self.rect_y+self.block_size), 
                                    (self.rect_x-self.block_size, self.rect_y),
                                    (self.rect_x+self.block_size, self.rect_y)]
            elif self.rot_pos == 3:
                self.LL_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y+self.block_size), 
                                    (self.rect_x, self.rect_y+self.block_size),
                                    (self.rect_x, self.rect_y-self.block_size)]
            if first:
                self.checkBounds()
                first = False
        pygame.draw.rect(self.screen, self.BLUE, [self.LL_blocks[0][0], self.LL_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.LL_blocks[1][0], self.LL_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.LL_blocks[2][0], self.LL_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.LL_blocks[3][0], self.LL_blocks[3][1], self.block_size, self.block_size])
        #self.rect_y += self.rect_change_y
        overlap = False
        y_overlap = None
        for block in self.LL_blocks:
            for item in self.block_list:
                if block[1]+self.block_size >= item[1] and block[1] <= item[1] and block[0] == item[0]:
                    y_overlap = item[1]-4*self.block_size
                    overlap = True
            if block[1]+self.block_size >= 648 and one_sec == False:
                self.clock.tick(30)
                one_sec = True
            elif block[1]+self.block_size >=648:
                overlap = True
        if overlap == True:
            self.block_list.append((self.LL_blocks[0][0], self.LL_blocks[0][1], self.BLUE))
            self.block_list.append((self.LL_blocks[1][0], self.LL_blocks[1][1], self.BLUE))
            self.block_list.append((self.LL_blocks[2][0], self.LL_blocks[2][1], self.BLUE))
            self.block_list.append((self.LL_blocks[3][0], self.LL_blocks[3][1], self.BLUE))
            self.rect_y = self.start_y
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            self.checkTetris()
            return 0        
    def right_S(self):
        if self.rot_pos == 0 or self.rot_pos == 2:
            self.RS_blocks = [(self.rect_x, self.rect_y), 
                                (self.rect_x-self.block_size, self.rect_y), 
                                (self.rect_x, self.rect_y-self.block_size), 
                                (self.rect_x+self.block_size, self.rect_y-self.block_size)]
        elif self.rot_pos == 1 or self.rot_pos == 3:
            self.RS_blocks = [(self.rect_x, self.rect_y-self.block_size), 
                                (self.rect_x, self.rect_y), 
                                (self.rect_x+self.block_size, self.rect_y),
                                (self.rect_x+self.block_size, self.rect_y+self.block_size)]
                                
        pygame.draw.rect(self.screen, self.LIME, [self.RS_blocks[0][0], self.RS_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.LIME, [self.RS_blocks[1][0], self.RS_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.LIME, [self.RS_blocks[2][0], self.RS_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.LIME, [self.RS_blocks[3][0], self.RS_blocks[3][1], self.block_size, self.block_size])
        #self.rect_y += self.rect_change_y
        overlap = False
        y_overlap = None
        for block in self.RS_blocks:
            for item in self.block_list:
                if block[1]+self.block_size >= item[1] and block[1] <= item[1] and block[0] == item[0]:
                    y_overlap = item[1]-4*self.block_size
                    overlap = True
            if block[1]+self.block_size >= 648:
                overlap = True
        if overlap == True:
            self.block_list.append((self.RS_blocks[0][0], self.RS_blocks[0][1], self.LIME))
            self.block_list.append((self.RS_blocks[1][0], self.RS_blocks[1][1], self.LIME))
            self.block_list.append((self.RS_blocks[2][0], self.RS_blocks[2][1], self.LIME))
            self.block_list.append((self.RS_blocks[3][0], self.RS_blocks[3][1], self.LIME))
            self.rect_y = self.start_y
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            self.checkTetris()
            return 0        
    def left_S(self):
        if self.rot_pos == 0 or self.rot_pos == 2:
            self.LS_blocks = [(self.rect_x, self.rect_y), 
                                (self.rect_x+self.block_size, self.rect_y), 
                                (self.rect_x, self.rect_y-self.block_size), 
                                (self.rect_x-self.block_size, self.rect_y-self.block_size)]
        elif self.rot_pos == 1 or self.rot_pos == 3:
            self.LS_blocks = [(self.rect_x, self.rect_y+self.block_size), 
                                (self.rect_x, self.rect_y), 
                                (self.rect_x+self.block_size, self.rect_y),
                                (self.rect_x+self.block_size, self.rect_y-self.block_size)]
        pygame.draw.rect(self.screen, self.RED, [self.LS_blocks[0][0], self.LS_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.RED, [self.LS_blocks[1][0], self.LS_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.RED, [self.LS_blocks[2][0], self.LS_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.RED, [self.LS_blocks[3][0], self.LS_blocks[3][1], self.block_size, self.block_size])
        #self.rect_y += self.rect_change_y
        overlap = False
        y_overlap = None
        for block in self.LS_blocks:
            for item in self.block_list:
                if block[1]+self.block_size >= item[1] and block[1] <= item[1] and block[0] == item[0]:
                    y_overlap = item[1]-4*self.block_size
                    overlap = True
            if block[1]+self.block_size >= 648:
                overlap = True
        if overlap == True:
            self.block_list.append((self.LS_blocks[0][0], self.LS_blocks[0][1], self.RED))
            self.block_list.append((self.LS_blocks[1][0], self.LS_blocks[1][1], self.RED))
            self.block_list.append((self.LS_blocks[2][0], self.LS_blocks[2][1], self.RED))
            self.block_list.append((self.LS_blocks[3][0], self.LS_blocks[3][1], self.RED))
            self.rect_y = self.start_y
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            self.checkTetris()
            return 0        
    def t_block(self):
        first = True
        for i in range(0,2):
            if self.rot_pos == 0:
                self.t_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x+self.block_size, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y), 
                                    (self.rect_x, self.rect_y-self.block_size)]
            elif self.rot_pos == 1:
                self.t_blocks = [(self.rect_x, self.rect_y+self.block_size), 
                                    (self.rect_x, self.rect_y), 
                                    (self.rect_x, self.rect_y-self.block_size),
                                    (self.rect_x+self.block_size, self.rect_y)]
            elif self.rot_pos == 2:
                self.t_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x+self.block_size, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y),
                                    (self.rect_x, self.rect_y+self.block_size)]
            elif self.rot_pos == 3:
                self.t_blocks = [(self.rect_x, self.rect_y), 
                                    (self.rect_x-self.block_size, self.rect_y), 
                                    (self.rect_x, self.rect_y+self.block_size),
                                    (self.rect_x, self.rect_y-self.block_size)]
            if first:
                self.checkBounds()
                first = False
        pygame.draw.rect(self.screen, self.PURPLE, [self.t_blocks[0][0], self.t_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.PURPLE, [self.t_blocks[1][0], self.t_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.PURPLE, [self.t_blocks[2][0], self.t_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.PURPLE, [self.t_blocks[3][0], self.t_blocks[3][1], self.block_size, self.block_size])
        #self.rect_y += self.rect_change_y
        overlap = False
        y_overlap = None
        for block in self.t_blocks:
            for item in self.block_list:
                if block[1]+self.block_size >= item[1] and block[1] <= item[1] and block[0] == item[0]:
                    y_overlap = item[1]-4*self.block_size
                    overlap = True
            if block[1]+self.block_size >= 648:
                overlap = True
        if overlap == True:
            self.block_list.append((self.t_blocks[0][0], self.t_blocks[0][1], self.PURPLE))
            self.block_list.append((self.t_blocks[1][0], self.t_blocks[1][1], self.PURPLE))
            self.block_list.append((self.t_blocks[2][0], self.t_blocks[2][1], self.PURPLE))
            self.block_list.append((self.t_blocks[3][0], self.t_blocks[3][1], self.PURPLE))
            self.rect_y = self.start_y
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            self.checkTetris()
            return 0        
    def rotate(self):
        if self.rot_pos == 3:
            self.rot_pos = 0
        else:
            self.rot_pos+=1
    def checkLeft(self):
        if self.block_index == 1:
            if self.rect_x == 100:
                return False
            else:
                for block_placed in self.block_list:
                    if self.rect_x - self.block_size == block_placed[0] and (self.rect_y == block_placed[1] or self.rect_y-self.block_size == block_placed[1]):
                        return False
                return True
        else:
            for block in self.block_dict[self.block_index]:
                if(block[0]<=100):
                    return False
            return True
    def checkRight(self):
        if self.block_index == 1:
            if self.rect_x+2*self.block_size >= 400:
                return False
            else:
                for block_placed in self.block_list:
                    if self.rect_x+3*self.block_size == block_placed[0] and (self.rect_y == block_placed[1] or self.rect_y-self.block_size == block_placed[1]):
                        return False
                return True
        else:
            for block in self.block_dict[self.block_index]:
                if(block[0]==370):
                    return False
                for block_placed in self.block_list:
                    if block[0]+self.block_size == block_placed[0] and block[1] == block_placed[1]:
                        return False
            return True
    def checkTop(self):
        if self.block_index == 1:
            if self.rect_y < self.start_y - 31:
                self.dead = True
                self.deadLog()
            else:
                return False
        else:
            for index, block in enumerate(self.block_list):
                for index2, block2 in enumerate(self.block_list):
                    if block[0] == block2[0] and block[1] == block2[1] and index != index2: 
                        self.dead = True
                        self.deadLog()

    def paused(self):
        pygame.mixer.music.pause()
        while self.pause:
            pos = pygame.mouse.get_pos()
            if pos[0] >= 200 and pos[0] <= 300 and pos[1] >= 300 and pos[1] <= 340:
                button_color = self.DARK_BLUE
            else:
                button_color = self.BLUE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause=False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if button_color == self.DARK_BLUE:
                        self.pause = False
            pygame.draw.rect(self.screen, self.WHITE, [98, 48, 304, 602])
            pygame.draw.rect(self.screen, self.BLACK, [100, 50, 300, 598])
            pygame.draw.rect(self.screen, self.WHITE, [150,200,200,200])
            pygame.draw.rect(self.screen, button_color, [200,300, 100, 40])
            font = pygame.font.Font('freesansbold.ttf', 15) 
  
            # create a text suface object, 
            # on which text is drawn on it. 
            text = font.render("Paused", True, self.BLACK, self.WHITE)
            #pts_string = 'Score: ' +str(self.pts)
            #text2 = font.render( pts_string,True, self.BLACK, self.WHITE) 
            text3 = font.render("Continue", True, self.BLACK, button_color)
            # create a rectangular object for the 
            # text surface object 
            textRect = text.get_rect()
            #textRect2 = text2.get_rect()  
            textRect3 = text3.get_rect()

            # set the center of the rectangular object. 
            textRect.center = (250, 220) 
            #textRect2.center = (250, 240)
            textRect3.center = (250, 320)
            self.screen.blit(text,textRect)
            #self.screen.blit(text2,textRect2)
            self.screen.blit(text3, textRect3)
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)
        pygame.mixer.music.unpause()
    def deadLog(self):
        winsound.PlaySound("dead.wav", 1)
        pygame.mixer.music.pause()
        while self.dead:
            pos = pygame.mouse.get_pos()
            if pos[0] >= 200 and pos[0] <= 300 and pos[1] >= 300 and pos[1] <= 340:
                button_color = self.DARK_BLUE
            else:
                button_color = self.BLUE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.block_list = []
                        self.dead = False
                        self.move_down_time = self.slow_speed
                        self.move_left = False
                        self.move_right = False
                        self.pts = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    if button_color == self.DARK_BLUE:
                        self.block_list = []
                        self.dead = False
                        self.move_down_time = self.slow_speed
                        self.move_left = False
                        self.move_right = False
                        self.pts = 0                  
            pygame.draw.rect(self.screen, self.WHITE, [98, 48, 304, 602])
            pygame.draw.rect(self.screen, self.BLACK, [100, 50, 300, 598])
            pygame.draw.rect(self.screen, self.WHITE, [150,200,200,200])
            pygame.draw.rect(self.screen, button_color, [200,300, 100, 40])
            font = pygame.font.Font('freesansbold.ttf', 15) 
  
            # create a text suface object, 
            # on which text is drawn on it. 
            text = font.render("You Lost!", True, self.BLACK, self.WHITE)
            pts_string = 'Score: ' +str(self.pts)
            text2 = font.render( pts_string,True, self.BLACK, self.WHITE) 
            text3 = font.render("Play Again", True, self.BLACK, button_color)
            # create a rectangular object for the 
            # text surface object 
            textRect = text.get_rect()
            textRect2 = text2.get_rect()  
            textRect3 = text3.get_rect()

            # set the center of the rectangular object. 
            textRect.center = (250, 220) 
            textRect2.center = (250, 240)
            textRect3.center = (250, 320)
            self.screen.blit(text,textRect)
            self.screen.blit(text2,textRect2)
            self.screen.blit(text3, textRect3)
            pygame.display.flip()
        pygame.mixer.music.unpause()
    def checkTetris(self):
        block_cnt = {}
        for item in self.block_list:
            if item[1] not in block_cnt.keys():
                block_cnt[item[1]]=1
            else:
                block_cnt[item[1]]+=1
        row_cnt = 0
        row_list = []
        for key in block_cnt.keys():
            if block_cnt[key] == 10:
                row_cnt += 1
                row_list.append(key)
        if row_cnt>=1:
            if row_cnt == 1:
                self.pts += 40
            elif row_cnt == 2:
                self.pts += 100
            elif row_cnt == 3:
                self.pts += 300
            elif row_cnt == 4:
                self.pts == 1200
            for row in sorted(row_list):
                self.deleteRow(row)
    def deleteRow(self, row_val):
        pop_list = []
        winsound.PlaySound("remove.wav", 1)
        for index, item in enumerate(self.block_list):
            if item[1] == row_val:
                pop_list.append(index)
            if item[1] < row_val:
                self.block_list[index] = (item[0], item[1]+self.block_size, item[2])
        for index in sorted(pop_list, reverse=True):
            self.block_list.pop(index)
    def show_block(self):
        pygame.draw.rect(self.screen, self.WHITE, [410, 48, 104, 180])
        pygame.draw.rect(self.screen, self.BLACK, [412, 50, 100, 176])
        x_pos = 450
        y_pos = 85
        if self.block_index_next == 0:
            blocks = [(x_pos, y_pos), 
                                (x_pos, y_pos+self.block_size), 
                                (x_pos, y_pos+2*self.block_size), 
                                (x_pos, y_pos+3*self.block_size)]    
            pygame.draw.rect(self.screen, self.TEAL, [blocks[0][0], blocks[0][1], self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.TEAL, [blocks[1][0], blocks[1][1], self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.TEAL, [blocks[2][0], blocks[2][1], self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.TEAL, [blocks[3][0], blocks[3][1], self.block_size, self.block_size])   
        elif self.block_index_next == 1:
            pygame.draw.rect(self.screen, self.YELLOW, [x_pos, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.YELLOW, [x_pos+self.block_size, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.YELLOW, [x_pos+self.block_size, y_pos+self.block_size, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.YELLOW, [x_pos, y_pos+self.block_size, self.block_size, self.block_size])
        elif self.block_index_next == 2:
            pygame.draw.rect(self.screen, self.ORANGE, [x_pos, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.ORANGE, [x_pos+self.block_size, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.ORANGE, [x_pos-self.block_size, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.ORANGE, [x_pos-self.block_size, y_pos-self.block_size, self.block_size, self.block_size])
        elif self.block_index_next == 3:
            pygame.draw.rect(self.screen, self.BLUE, [x_pos, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.BLUE, [x_pos-self.block_size, y_pos-self.block_size, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.BLUE, [x_pos-self.block_size, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.BLUE, [x_pos+self.block_size, y_pos, self.block_size, self.block_size])
        elif self.block_index_next == 5:
            pygame.draw.rect(self.screen, self.RED, [x_pos, y_pos, self.block_size, self.block_size])   
            pygame.draw.rect(self.screen, self.RED, [x_pos, y_pos-self.block_size, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.RED, [x_pos-self.block_size, y_pos-self.block_size, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.RED, [x_pos+self.block_size, y_pos, self.block_size, self.block_size])
        elif self.block_index_next == 4:
            pygame.draw.rect(self.screen, self.LIME, [x_pos, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.LIME, [x_pos-self.block_size, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.LIME, [x_pos+self.block_size, y_pos-self.block_size, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.LIME, [x_pos, y_pos-self.block_size, self.block_size, self.block_size])
        elif self.block_index_next == 6:
            pygame.draw.rect(self.screen, self.PURPLE, [x_pos, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.PURPLE, [x_pos+self.block_size, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.PURPLE, [x_pos-self.block_size, y_pos, self.block_size, self.block_size])
            pygame.draw.rect(self.screen, self.PURPLE, [x_pos, y_pos-self.block_size, self.block_size, self.block_size])
    def checkBounds(self):
        if self.block_index != 1:
            for item in self.block_dict[self.block_index]:
                if item[0] >= 400:
                    self.rect_x -= 30
                    print("over")
                    break
                elif item[0] <= 70:
                    self.rect_x += 30
                    break
def main():
    game = game_env()

if __name__ == "__main__":
    main()
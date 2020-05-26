import pygame
from random import randint
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
        pygame.init()
        self.size = (500, 700)
        self.block_size = 30
        self.screen = pygame.display.set_mode(self.size)
        self.block_list = []
        self.collision_list = []
        self.new_block = True
        self.block_index = None
        self.block_call = [self.long_block, self.square_block, self.right_L, self.left_L, self.right_S, self.left_S, self.t_block]
        self.rot_pos = 0
        self.long_blocks = []
        self.RL_blocks = []
        self.LL_blocks = []
        self.RS_blocks = []
        self.LS_blocks = []
        self.t_blocks = []
        self.dead = False
        pygame.display.set_caption("My Game")+

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        self.rect_x = 250
        self.rect_y = 82
        self.rect_change_y = 2
        self.start_right = pygame.time.get_ticks()
        self.start_left = pygame.time.get_ticks()
        self.pause = False
        self.pts = 0
        while not done:
            font = pygame.font.Font('freesansbold.ttf', 10) 
  
            # create a text suface object, 
            # on which text is drawn on it. 
            pts_string = 'Points: ' +str(self.pts)
            text = font.render( pts_string,True, self.WHITE, self.BLACK) 

            # create a rectangular object for the 
            # text surface object 
            textRect = text.get_rect()  

            # set the center of the rectangular object. 
            textRect.center = (420, 400) 
            self.block_dict = {0:self.long_blocks, 1:None, 2: self.RL_blocks, 3: self.LL_blocks, 4: self.RS_blocks, 5: self.LS_blocks, 6:self.t_blocks}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        can_move = self.checkLeft()
                        if can_move:
                            if pygame.time.get_ticks() - self.start_left >= 60:
                                self.rect_x -= self.block_size
                                self.start_left = pygame.time.get_ticks()
                    elif event.key == pygame.K_RIGHT:
                        can_move = self.checkRight()
                        if can_move:
                            if pygame.time.get_ticks() - self.start_right >= 60:
                                self.rect_x += self.block_size
                                self.start_right = pygame.time.get_ticks()
                    elif event.key == pygame.K_UP:
                        self.rotate()
                    elif event.key == pygame.K_DOWN:
                        self.rect_change_y = 10
                    elif event.key == pygame.K_p:
                        if not self.pause:
                            self.pause = True
                            self.paused()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.rect_change_y = 2
            self.screen.fill(self.BLACK)
            self.screen.blit(text,textRect)
            pygame.draw.rect(self.screen, self.WHITE, [98, 48, 304, 602])
            pygame.draw.rect(self.screen, self.BLACK, [100, 50, 300, 598])
            if self.new_block == True:
                self.block_index = randint(0,len(self.block_call)-1)
                self.new_block = False
            self.block_call[self.block_index]()
            #self.checkTop()
            self.checkTetris()
            for item in self.block_list:
                pygame.draw.rect(self.screen, item[2], [item[0],
                                item[1], self.block_size, self.block_size])
            
            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()

    def square_block(self):
        pygame.draw.rect(self.screen, self.YELLOW, [self.rect_x, self.rect_y, self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.YELLOW, [self.rect_x+self.block_size, self.rect_y, self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.YELLOW, [self.rect_x+self.block_size, self.rect_y+self.block_size, self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.YELLOW, [self.rect_x, self.rect_y+self.block_size, self.block_size, self.block_size])
        self.rect_y += self.rect_change_y
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
            self.rect_y = 82
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
    def long_block(self):
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
        pygame.draw.rect(self.screen, self.BLUE, [self.long_blocks[0][0], self.long_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.long_blocks[1][0], self.long_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.long_blocks[2][0], self.long_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.long_blocks[3][0], self.long_blocks[3][1], self.block_size, self.block_size])
        self.rect_y += self.rect_change_y
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
            self.block_list.append((self.long_blocks[0][0], self.long_blocks[0][1], self.BLUE))
            self.block_list.append((self.long_blocks[1][0], self.long_blocks[1][1], self.BLUE))
            self.block_list.append((self.long_blocks[2][0], self.long_blocks[2][1], self.BLUE))
            self.block_list.append((self.long_blocks[3][0], self.long_blocks[3][1], self.BLUE))
            self.rect_y = 82
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            return 0 
    def right_L(self):
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
        pygame.draw.rect(self.screen, self.ORANGE, [self.RL_blocks[0][0], self.RL_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.ORANGE, [self.RL_blocks[1][0], self.RL_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.ORANGE, [self.RL_blocks[2][0], self.RL_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.ORANGE, [self.RL_blocks[3][0], self.RL_blocks[3][1], self.block_size, self.block_size])
        self.rect_y += self.rect_change_y
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
            self.rect_y = 82
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            return 0     
    def left_L(self):
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
        pygame.draw.rect(self.screen, self.BLUE, [self.LL_blocks[0][0], self.LL_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.LL_blocks[1][0], self.LL_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.LL_blocks[2][0], self.LL_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.BLUE, [self.LL_blocks[3][0], self.LL_blocks[3][1], self.block_size, self.block_size])
        self.rect_y += self.rect_change_y
        overlap = False
        y_overlap = None
        for block in self.LL_blocks:
            for item in self.block_list:
                if block[1]+self.block_size >= item[1] and block[1] <= item[1] and block[0] == item[0]:
                    y_overlap = item[1]-4*self.block_size
                    overlap = True
            if block[1]+self.block_size >= 648:
                overlap = True
        if overlap == True:
            self.block_list.append((self.LL_blocks[0][0], self.LL_blocks[0][1], self.BLUE))
            self.block_list.append((self.LL_blocks[1][0], self.LL_blocks[1][1], self.BLUE))
            self.block_list.append((self.LL_blocks[2][0], self.LL_blocks[2][1], self.BLUE))
            self.block_list.append((self.LL_blocks[3][0], self.LL_blocks[3][1], self.BLUE))
            self.rect_y = 82
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
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
        self.rect_y += self.rect_change_y
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
            self.rect_y = 82
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
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
        self.rect_y += self.rect_change_y
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
            self.rect_y = 82
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
            return 0        
    def t_block(self):
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
        pygame.draw.rect(self.screen, self.RED, [self.t_blocks[0][0], self.t_blocks[0][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.RED, [self.t_blocks[1][0], self.t_blocks[1][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.RED, [self.t_blocks[2][0], self.t_blocks[2][1], self.block_size, self.block_size])
        pygame.draw.rect(self.screen, self.RED, [self.t_blocks[3][0], self.t_blocks[3][1], self.block_size, self.block_size])
        self.rect_y += self.rect_change_y
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
            self.block_list.append((self.t_blocks[0][0], self.t_blocks[0][1], self.RED))
            self.block_list.append((self.t_blocks[1][0], self.t_blocks[1][1], self.RED))
            self.block_list.append((self.t_blocks[2][0], self.t_blocks[2][1], self.RED))
            self.block_list.append((self.t_blocks[3][0], self.t_blocks[3][1], self.RED))
            self.rect_y = 82
            self.rect_x = 250
            self.new_block = True
            self.rot_pos = 0
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
                return True
        else:
            for block in self.block_dict[self.block_index]:
                if(block[0]==370):
                    return False
            return True
    def checkTop(self):
        if self.block_index == 1:
            if self.rect_y <= 48:
                return True
            else:
                return False
        else:
            for block in self.block_dict[self.block_index]:
                if(block[1]<=50):
                    return False
            self.dead = True
            self.deadLog()
    def paused(self):
        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause=False

            pygame.display.update()
            self.clock.tick(60)
    def deadLog(self):
        while self.dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.block_list = []
                        self.dead = False
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
            for row in row_list:
                self.deleteRow(row)
    def deleteRow(self, row_val):
        for index, item in enumerate(self.block_list):
            if item[1] == row_val:
                self.block_list.pop(index)
            elif item[1] < row_val:
                self.block_list[index] = (item[0], item[1]+self.block_size, item[2])


def main():
    game = game_env()

if __name__ == "__main__":
    main()
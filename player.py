from board import *
from random import Random
import statistics
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError

class MyPlayer(Player):
    def __init__(self):
        self.value = 0
        self.trigger_dis = 0
        self.trigger_bomb = 0
        self.best_sets_1 = []
        self.best_sets_2 = []
        self.check_discard = 0
        self.discard_nums = 10
        self.bomb_nums = 5
        self.case_1 = True
        self.case_2 = False
        self.bomb_pending = False

        
    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)


    def calculate_single_column_height(self, board, x): #x shoule be between 0 and 9
        for y in range(board.height):
            if (x,y) in board.cells:
                return board.height-y
            
        return 0 #no column in this x position



    def get_column_height_list(self, board):
        column_list = []
        for x in range(board.width):
            val = self.calculate_single_column_height(board,x)
            column_list.append(val)
        return column_list
    
    def sum_column_height(self,board, column_list): #First assesment: Total height
        #column_list = self.get_column_height_list(board)
        return sum(column_list)
    
    def var_column_height(self,board, column_list): #Second assesment: Bumpness
        #column_list = self.get_column_height_list(board)
        bumpness = 0
        for i in range(board.width - 1):
            bumpness = bumpness + (column_list[i] - column_list[i+1]) ** 2

        return bumpness
    


    def is_hole(self,x,y,board):
        if x > 0:
            left = (x-1,y) in board.cells
        else:
            left = True
        
        if x < 9:
            right = (x+1,y) in board.cells
        else:
            right = True
        
        return left and right
    
    def get_well(self,board):
        well = 0
        for x in range(board.width):
            search = 1
            for y in range(board.height):
                if search == 1 and ((x,y) not in board.cells) and self.is_hole(x,y,board) == True:
                    well = well + 1
                elif((x,y) in board.cells):
                    search = 0

        return well
    
    def get_blocked_cells(self, board, height):
        cells = 0
        #height = self.get_column_height_list(board)
        for x in range(board.width):
            search = 0
            for y in range(height[x]):
                Y = 24 - y
                if (x,Y) not in board.cells and self.is_hole(x,Y, board) == True:
                    search = 1
                if search == 1 and (x,Y) in board.cells:
                    cells = cells + 1
                

        return cells
    
    def get_max_height(self,board):
        height = 0
        for y in range(board.height):
            for x in range(board.width):
                if (x,y) in board.cells:
                    return board.height - y
        return 0
    
    def get_air_exposure(self, board):
        count = 0
        for y in range(board.height):
            for x in range(board.width):
                if(x>0) and (x<9) and (y>0) and (y<24) and (x,y) in board.cells:
                    if(x+1,y) not in board.cells:
                        count = count + 1
                    if(x,y+1) not in board.cells:
                        count = count + 1
                    if(x-1,y) not in board.cells:
                        count = count + 1
                    if(x,y-1) not in board.cells:
                        count = count + 1
        return count
    
    def get_row_transition(self, board):
        tran = 0
        for y in range(board.height):
            for x in range(9):
                if ((x,y) in board.cells and (x+1,y) in board.cells) or   ((x,y) not in board.cells and (x+1,y) not in board.cells):
                    continue
                else:
                    tran = tran + 1
        return tran
    

    def get_col_transition(self, board):
        tran = 0
        for x in range(board.width):
            for y in range(23):
                if ((x,y) in board.cells and (x,y+1) in board.cells) or   ((x,y) not in board.cells and (x,y+1) not in board.cells):
                    continue
                else:
                    tran = tran + 1
        return tran
                





    
    def check_holes(self,board): #Third assesment: Holes
        holes = 0
        for x in range(board.width):
            search = 0
            for y in range(board.height):
                if(x,y) in board.cells:
                    search = 1
                
                if search == 1 and (x,y) not in board.cells:
                    holes = holes + 1

        return holes

            
    
    def check_elinmating(self,clone_board, original_board): #Fourth assesment: Lines elimnation
        gap = clone_board.score - original_board.score
        if gap > 1600:
            return 1000.0
        elif gap > 400:
            return -10.0
        elif gap > 100:
            return -8.0
        elif gap > 24:
            return -10.0
        
        return 0.0
    
    def check_first_col(self,board,height):
        #height = self.calculate_single_column_height(board,0)
        if(height[0] == 0):
            return 1.0
        else:
            return -1.0
        
    def check_row(self,board,y):
        for x in range(1,10):
            if (x,y) not in board.cells:
                return False
        return True
    
    def get_full_row(self, board):
        full_row = 0
        for y in range(24):
            if self.check_row(board, y) == True:
                full_row = full_row + 1
            else:
                full_row = 0

            if full_row > 3:
                return 5.0
            elif full_row > 2:
                return 2.0
            elif full_row > 1:
                return 1.0
        return 0.0
            



        
    


    def rotate_board(self,board,time): #This function will rotate the board and return the command sets
        try:
            if time == 0:
                board.move(None)
                return [None]
            elif time == 1:
                board.rotate(Rotation.Clockwise)
                return [Rotation.Clockwise]
            elif time == 2:
                board.rotate(Rotation.Clockwise)
                board.rotate(Rotation.Clockwise)
                return [Rotation.Clockwise,Rotation.Clockwise]
            elif time == 3:
                board.rotate(Rotation.Anticlockwise)
                return [Rotation.Anticlockwise]
            else:
                raise IndexError("Index out of range")
        except Exception:
            return []

    def direction_board_left(self, board, step):
        try:
            return_list = []
            if step == 0:
                return_list.append(None)
                return return_list
            for i in range(step):
                board.move(Direction.Left)
                return_list.append(Direction.Left)
            return return_list
        except Exception:
            return []
    

    def direction_board_right(self, board, step):
        try:
            return_list = []
            if step == 0:
                return_list.append(None)
                return return_list
            for i in range(step):
                board.move(Direction.Right)
                return_list.append(Direction.Right)
            return return_list
        except Exception:
            return []
    
    def Drop_board(self,board):
        try:
            board.move(Direction.Drop)
            return [Direction.Drop]
        except Exception:
            return []
    
    def discard_board(self,board):
        board.discard()
        return [Action.Discard]
    
    def bomb_board(self, board):
        board.bomb()
        return [Action.Bomb]
    

    def choose_action(self, board):

        score_1 = 0
        score_2 = 0
        best_score_1 = -1000
        best_score = -1000
        clone_0 = board.clone()

        if self.case_2 == True:
            return Action.Bomb

        if self.case_1 == True:
            for i in range(4):
                clone_1 = clone_0.clone()
                rotate_sets_1 = self.rotate_board(clone_1, i)
                for j in range(11):
                    clone_2 = clone_1.clone()
                    if j < 6:
                        actoin_sets_1 = self.direction_board_left(clone_2, j)
                    else:
                        actoin_sets_1 = self.direction_board_right(clone_2, j-5)
                    drop_sets_1 = self.Drop_board(clone_2)
                    sets_1 = rotate_sets_1 + actoin_sets_1 + drop_sets_1
                    list_1 = self.get_column_height_list(clone_2)
                    score_1 = (
                        #- 0.625 * self.sum_column_height(clone_2, list_1)#aggreate height 0.510066
                        + 2.0 * self.check_elinmating(clone_2,clone_0)#line elinmination
                        - 25.0 * self.check_holes(clone_2)#holes
                        - 1.0 * self.var_column_height(clone_2, list_1)#bumpiness 0.184483
                        #- 0.05 * self.get_blocked_cells(next_clone_2, list)#cells above the hole
                        - 1.0 * self.get_max_height(clone_2)#highest height
                        #- 1.0 * self.get_row_transition(clone_2)
                        #- 1.0 * self.get_col_transition(clone_2)
                        #+ 1.0 * self.check_first_col(clone_2, list_1)#height of first column
                        #+ 6.0 * self.get_full_row(clone_2)#continued full row except the first column
                    )
                    if(score_1 > best_score_1):
                        best_score_1 = score_1
                        best_sets_1 = sets_1
                    for q in range(4):
                        next_clone_1 = clone_2.clone()
                        next_clone_1.next = next_clone_1.falling
                        rotate_sets_2 = self.rotate_board(next_clone_1, q)
                        for p in range(11):
                            next_clone_2 = next_clone_1.clone()
                            if p < 6:
                                actoin_sets_2 = self.direction_board_left(next_clone_2, p)
                            else:
                                actoin_sets_2 = self.direction_board_right(next_clone_2, p-5)                            
                            drop_sets_2 = self.Drop_board(next_clone_2)
                            list = self.get_column_height_list(next_clone_2)
                            score_2 = (
                                #- 0.625 * self.sum_column_height(next_clone_2, list)#aggreate height
                                + 2.0 * self.check_elinmating(next_clone_2,clone_2)#line elinmination
                                - 25.0 * self.check_holes(next_clone_2)#holes
                                - 1.0 * self.var_column_height(next_clone_2, list)#bumpiness
                                #- 0.05 * self.get_blocked_cells(next_clone_2, list)#cells above the hole
                                - 1.0 * self.get_max_height(next_clone_2)#highest height
                                #- 1.0 * self.get_row_transition(next_clone_2)
                                #- 1.0 * self.get_col_transition(next_clone_2)
                                #+ 1.0 * self.check_first_col(next_clone_2, list)#height of first column
                                #+ 6.0 * self.get_full_row(next_clone_2)#continued full row except the first column
                                + score_1
                            )
                            if(score_2 > best_score):
                                best_score = score_2
                                self.best_sets_1 = sets_1
            return self.best_sets_1
        





SelectedPlayer = MyPlayer

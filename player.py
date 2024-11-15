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
    
    def sum_column_height(self,board): #First assesment: Total height
        column_list = self.get_column_height_list(board)
        return sum(column_list)
    
    def var_column_height(self,board): #Second assesment: Bumpness
        column_list = self.get_column_height_list(board)
        bumpness = 0
        for i in range(board.width - 1):
            bumpness = bumpness + abs(column_list[i] - column_list[i+1])

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
    
    def get_blocked_cells(self, board):
        cells = 0
        height = self.get_column_height_list(board)
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
            return 50.0
        elif gap > 400:
            return 10.0
        elif gap > 200:
            return 5.0
        elif gap > 50:
            return 0.0
        
        return 0.0
    
    def check_first_col(self,board):
        height = self.calculate_single_column_height(board,0)
        if(height == 0):
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

    def direction_board_left(self, board, step):
        return_list = []
        if step == 0:
            return_list.append(None)
            return return_list
        for i in range(step):
            board.move(Direction.Left)
            return_list.append(Direction.Left)
        return return_list
    

    def direction_board_right(self, board, step):
        return_list = []
        if step == 0:
            return_list.append(None)
            return return_list
        for i in range(step):
            board.move(Direction.Right)
            return_list.append(Direction.Right)
        return return_list
    
    def Drop_board(self,board):
        board.move(Direction.Drop)
        return [Direction.Drop]
    
    def discard_board(self,board):
        board.discard()
        return [Action.Discard]
    
    def bomb_board(self, board):
        board.bomb()
        return [Action.Bomb]
    

    def choose_action(self, board):

        if(self.best_sets_2):
            tmp_sets = self.best_sets_2
            self.best_sets_2 = []
            return tmp_sets


        best_score = -1000
        best_sets = []
        
        for i in range(4):
            clone_1 = board.clone()
            rotate_sets_1 = self.rotate_board(clone_1, i)
            for j in range(11):
                clone_2 = clone_1.clone()

                if j < 6:
                    actoin_sets_1 = self.direction_board_left(clone_2, j)
                else:
                    actoin_sets_1 = self.direction_board_right(clone_2, j-5)

            
                drop_sets_1 = self.Drop_board(clone_2)


                if(clone_2.falling is None):
                    return Direction.Down


                for q in range(4):
                    next_clone_1 = clone_2.clone()
                    rotate_sets_2 = self.rotate_board(next_clone_1, q)

                    for p in range(11):
                        next_clone_2 = next_clone_1.clone()
                        if p < 6:
                            actoin_sets_2 = self.direction_board_left(next_clone_2, p)
                        else:
                            actoin_sets_2 = self.direction_board_right(next_clone_2, p-5)

                        if(next_clone_2.falling is None):
                            return Direction.Down

                        drop_sets_2 = self.Drop_board(next_clone_2)

                        sets_1 = rotate_sets_1 + actoin_sets_1 + drop_sets_1
                        sets_2 = rotate_sets_2 + actoin_sets_2 + drop_sets_2

                        score = (
                            -0.510066*self.sum_column_height(next_clone_2)#aggreate height
                            +0.760666*self.check_elinmating(next_clone_2,board)#line elinmination
                            -0.5*self.check_holes(next_clone_2)#holes
                            -0.184483*self.var_column_height(next_clone_2)#bumpiness
                            - 0.05 * self.get_blocked_cells(next_clone_2)#cells above the hole
                            - 0.05 * self.get_max_height(next_clone_2)#highest height
                            - 0.05 * self.get_row_transition(next_clone_2)
                            - 0.05 * self.get_col_transition(next_clone_2)
                            #- 0.05 * self.calculate_single_column_height(next_clone_2,0)#height of first column
                            #+ 0.05 * self.get_full_row(next_clone_2)#continued full row except the first column
                        )

                        if(score > best_score):
                            best_score = score
                            self.best_sets_1 = sets_1
                            self.best_sets_2 = sets_2
                            tmp = next_clone_2

        if(self.sum_column_height(tmp) > 100):
            self.best_sets_1 = []
            self.best_sets_2 = []
            return Action.Bomb

        
        return self.best_sets_1

                        





SelectedPlayer = MyPlayer

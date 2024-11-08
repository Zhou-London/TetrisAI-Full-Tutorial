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
        elif gap > 100:
            return 3.0
        elif gap > 28:
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
        best_score = -1000
        best_sets = []
        tmp = 0

        for rot in range(9):
            if board.falling is None:
                return Direction.Down
            
            if (rot >= 0) and (rot <= 3):
                rotate_sets = []
                discard_sets = []
                bomb_sets = []
                clone_1 = board.clone()
                rotate_sets = self.rotate_board(clone_1,rot)
            elif(rot >= 4) and (rot <= 7) and self.trigger_dis == 1 and board.discards_remaining > 0:
                rotate_sets = []
                discard_sets = []
                bomb_sets = []
                clone_1 = board.clone()
                discard_sets = self.discard_board(clone_1)
                rotate_sets = self.rotate_board(clone_1,rot-4)
            elif(rot == 8) and self.trigger_bomb == 1:
                rotate_sets = []
                discard_sets = []
                bomb_sets = []
                clone_1 = board.clone()
                bomb_sets = self.bomb_board(clone_1)

            else:
                break


            if clone_1.falling is None:
                return Direction.Down
            

            step = 0
            while step < 11:
                dir_sets = []
                clone_2 = clone_1.clone()

                if (step >= 0) and (step<6):
                    dir_sets = []
                    dir_sets = self.direction_board_left(clone_2,step)
                elif(step >= 6) and (step <11):
                    dir_sets = []
                    dir_sets = self.direction_board_right(clone_2,step - 5)
                step = step + 1

                sets = []

                if clone_2.falling is None:
                    return Direction.Down
                drop_sets = self.Drop_board(clone_2)
                sets = bomb_sets + discard_sets + rotate_sets + dir_sets + drop_sets

                score =  (-0.510066 * self.sum_column_height(clone_2)
                          + 0.760666 * self.check_elinmating(clone_2, board)
                          - 0.35663 * self.check_holes(clone_2) #0.35663
                          - 0.184483 * self.var_column_height(clone_2)
                          #- 0.05 * self.get_well(clone_2)
                          - 0.05 * self.get_blocked_cells(clone_2)
                          - 0.05 * self.get_max_height(clone_2)
                          - 0.05 * self.get_row_transition(clone_2)
                          - 0.05 * self.get_col_transition(clone_2)
                          + 0.05 * self.calculate_single_column_height(clone_2,0)
                          #+ 1.0 * self.check_first_col(clone_2)
                          )
                
                if score > best_score:
                    tmp = clone_2
                    best_score = score
                    best_sets = sets

        if tmp.score > 8000:
            self.trigger_dis = 1

        if self.sum_column_height(tmp) > 0:
            self.trigger_bomb = 1
        #time.sleep(3)
        print(self.calculate_single_column_height(tmp,0))

        return best_sets







SelectedPlayer = MyPlayer

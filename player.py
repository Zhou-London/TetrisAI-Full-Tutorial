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

    
    def check_holes(self,board): #Third assesment: Holes
        column_list = self.get_column_height_list(board)
        num_of_holes = 0
        for x in range(board.width):
            if column_list[x] == 0:
                continue
            for y in range(column_list[x]):
                Y = board.height - y
                if (x,Y) not in board.cells:
                    if self.is_hole(x,Y,board) == True:
                        num_of_holes = num_of_holes + 1
        return num_of_holes




            
    
    def check_elinmating(self,clone_board, original_board): #Fourth assesment: Lines elimnation
        gap = clone_board.score - original_board.score
        if gap > 1600:
            return 20.0
        elif gap > 400:
            return 3.0
        elif gap > 100:
            return 0.5
        elif gap > 28:
            return -7.4 #-5.0(stable 15008),-7.0(stable16537), -7.2(19728), -7.40625(20041)
        
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
                          )
                
                if score > best_score:
                    tmp = clone_2
                    best_score = score
                    best_sets = sets

        if tmp.score > 10000:
            self.trigger_dis = 1

        if self.sum_column_height(tmp) > 0:
            self.trigger_bomb = 1

        return best_sets







SelectedPlayer = MyPlayer

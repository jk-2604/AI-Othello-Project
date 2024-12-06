#Othello Board Game. 

#Importing the necessary libraries. 
import numpy as np 
import random 
import time 
import math 

directions=[
    (-1,1), #left-up   
    (1,1), #right-up

    (0,1), #down 
    (0,-1), #up 

    (-1,0), #right
    (1,0), #left 

    (-1,-1), #left-down
    (1,-1), #right-down 
]

#Defining a class called Othello. 
class Othello(): 
    def __init__(self, board): 
        self.board=board
        self.player=1 #Black. 
        self.opponent=-1 #White. 
        self.current_player=self.player 
        self.current_opponent=self.opponent
        self.max_depth=3 #For the minimax algorithm. 
    
    #Printing the start position for the board. 
    def start_pos(self): 
        for i in range(8): 
            for j in range(8): 
                self.board[i][j]=0
        self.board[3][4]=self.board[4][3]=self.player
        self.board[4][4]=self.board[3][3]=self.opponent
        return self.board 
    
    #Function to display the board. 
    def display_board(self): 
        for i in range(8): #Printing the column coordinates. 
            if i==0: 
                print(" ",i, end='  ') 
            else:
                print(i, end='  ') 
        print() 
        for i in range (8): 
            print(i, end=' ') #Printing the row coordinates. 
            for j in range(8): 
                if self.board[i][j]==self.player: 
                    print("⚫", end=' ') 
                elif self.board[i][j]==self.opponent: 
                    print("⚪", end=' ') 
                else: 
                    print("🟩", end=' ') 
            print() #Printing a new line at the end of each row.
    
    #Printing the available moves for a given player. 
    def available_moves(self, player, board): 
        available_moves=[]
        for i in range(8) : 
            for j in range(8): 
                if board[i][j]==0 and self.valid_move(i,j, player, board)==True:
                    available_moves.append((i,j))
        return available_moves
    
   #Function to play the game. 
    def play(self, choice):  
        if (choice=="1"):
            print("""Choose the situations: 
                    1 - Greedy Search H1 vs Greedy Search H2, 
                    2 - Greedy Search H1 vs Simulated Annealing,
                    3 - Greedy Search H2 vs Simulated Annealing,
                    4 - Greedy Search H2 vs Minimax,
                    5 - Greedy Search H1 vs Minimax,
                    6 - Simulated Annealing vs Minimax,     """) 
            level=input()
            if (level=="1"):
                print("Player 1 is ⚫ and Player 2 is ⚪, Greedy Search H1 vs Greedy Search H2 ")
                while self.game_over()==False:
                    self.greedy_search_H1(self.player)  
                    self.greedy_search_H2(self.opponent)
                self.game_result()
            elif (level=="2"): 
                print("Player 1 is ⚫ and Player 2 is ⚪, Greedy Search H1 vs Simulated Annealing")
                while self.game_over()==False: 
                    self.greedy_search_H1(self.player)
                    self.simulated_annealing(self.opponent)
                self.game_result()
            elif (level=="3"): 
                print("Player 1 is ⚫ and Player 2 is ⚪, Greedy Search H2 vs Simulated Annealing")
                while self.game_over()==False: 
                    self.greedy_search_H2(self.player)
                    self.simulated_annealing(self.opponent)
                self.game_result()
            elif (level=="4"): 
                print("Player 1 is ⚫ and Player 2 is ⚪, Greedy Search H2 vs Minimax")
                while self.game_over()==False: 
                    self.greedy_search_H2(self.player)
                    self.minimax(self.opponent)
                self.game_result()
            elif (level=="5"): 
                print("Player 1 is ⚫ and Player 2 is ⚪, Greedy Search H1 vs Minimax")
                while self.game_over()==False: 
                    self.greedy_search_H1(self.player)
                    self.minimax(self.opponent)
                self.game_result() 
            elif (level=="6"): 
                print("Player 1 is ⚫ and Player 2 is ⚪, Greedy Search H1 vs Minimax")
                while self.game_over()==False: 
                    self.simulated_annealing(self.player)
                    self.minimax(self.opponent)
                self.game_result()

        else:
            print("Player 1 is ⚫ and Player 2 is ⚪") 
            while self.game_over()==False: 
                self.player_move(self.player) 
                self.player_move(self.opponent)
            self.game_result() 
            
    #Function to perform the player's move:
    def player_move(self, player):
        self.start_move(player)
        available_moves=self.available_moves(self.current_player, self.board) 
        self.print_moves(available_moves)
        (x,y) = map(int,input("Enter your move:").split(','))
        print("\n")
        if self.valid_move(x,y, self.current_player, self.board)==True:
            self.make_move(x,y, self.current_player, self.board) 
            self.swap()
        else: 
            print("Invalid move! Try again.") 
            self.player_move(self.current_player) 

    #Function to declare the turn: 
    def turn(self):
        if self.current_player==1:   
            return 1 
        else:
            return -1

    #Function to swap the turn: 
    def swap(self):
        self.current_player, self.current_opponent = self.current_opponent, self.current_player

    #Function to count the number of opponent pieces flipped H1. 
    def count_flips(self, x, y, player): 
        self.current_player=player
        self.current_opponent=-player 
        if self.board[x][y]!=0: 
            return False 
        opponents_flipped=0
        for direction in directions: 
            dx , dy = direction
            nx, ny = x + dx, y + dy 
            flips=0
            while 0<=nx<8 and 0<=ny<8 and self.board[nx][ny]==self.current_opponent: 
                flips+=1 
                nx, ny= nx + dx, ny + dy 
            if 0<=nx<8 and 0<=ny<8 and self.board[nx][ny]==self.current_player: 
                opponents_flipped+=flips
        return opponents_flipped 

    #Function to make a move. 
    def make_move(self,x,y, player, board):
        current_player=player
        current_opponent=-player
        board[x][y]=current_player
        for direction in directions: 
            nx=x 
            ny=y
            dx = direction[0] 
            dy = direction[1]
            nx+=dx 
            ny+=dy
            pieces_to_flip=[]
            while 0<=nx<8 and 0<=ny<8 and board[nx][ny]==current_opponent: 
                pieces_to_flip.append((nx,ny))
                nx+=direction[0]
                ny+=direction[1]
                if 0<=nx<8 and 0<=ny<8 and board[nx][ny]==current_player: 
                    for i, j in pieces_to_flip: 
                        board[i][j]=current_player
        return board 

    #Creating a function that checks the validity of the move. 
    def valid_move(self,x,y,player, board):
        current_player=player
        current_opponent=-player
        if board[x][y]!=0: 
            return False 
        list_of_opponents=[]
        valid=False
        for direction in directions:
            nx=x 
            ny=y
            dx = direction[0] 
            dy = direction[1]
            nx+=dx 
            ny+=dy
            found_opponent=False
            while 0<=nx<8 and 0<=ny<8 :
                if board[nx][ny]==current_opponent:  
                    nx+=direction[0]
                    ny+=direction[1]
                    found_opponent=True
                elif board[nx][ny]==current_player and found_opponent: 
                    list_of_opponents.append((nx-direction[0],ny-direction[1]))
                    valid=True
                    break
                else: 
                    break 
        return valid
    
    #Function to start each move: 
    def start_move(self, player): 
        self.current_player=player
        self.current_opponent=-player
        black_score, white_score=self.score(self.board) 
        print("⚫ score", black_score, ", ⚪ score", white_score)
        self.display_board() 
        turn=self.turn()
        if turn==1:   
            print("It is ⚫'s turn") 
        else:
            print("It is ⚪'s turn")

    #Function to determine the score. 
    def score(self, board): 
        black_score=np.sum(board == 1)
        white_score=np.sum(board == -1)
        return black_score, white_score

    def get_winner(self):
        player1_score = np.sum(self.board == 1)
        player2_score = np.sum(self.board == -1)
        if player1_score > player2_score:
            return 1
        elif player2_score > player1_score:
            return -1
        else:
            return 0  # Draw
    
    #Function to declare the winner. 
    def game_result(self):
        if self.game_over()==True: 
            print("Game over!") 
            self.display_board()
            winner=self.get_winner()
            if winner==1:
                print("winner is ⚫")
            elif winner==-1: 
                print("winner is ⚪")
            else: 
                print("It is a tie!")

    #Function to check if the game is over. 
    def game_over(self):
        for i in range(8):
            for j in range(8):
                available_moves=self.available_moves(self.current_player, self.board)
                if self.board[i][j]==0 and self.valid_move(i,j, self.current_player, self.board):
                    return False 
                elif available_moves!=[]: 
                    return False
                else: 
                    return True 
        
    #Algorithms to perform the computer moves. 

    #Greedy Search. 
    #Function to perform greedy search move with H1. 
    def greedy_search_H1(self, player): 
        self.start_move(player)
        print("Greedy search is making a move")
        time.time()
        most_tempting=None
        most_flips=0
        available_moves=self.available_moves(player, self.board) 
        self.print_moves(available_moves)
        for move in available_moves: 
            if move == (0,0) or move == (0,7) or move == (7,0) or move == (7,7):
                most_tempting=move
                break
            else:
                flips=self.count_flips(move[0], move[1], self.current_player) 
                if flips>most_flips :
                    most_flips=flips
                    most_tempting=move
        if most_tempting!=None and self.valid_move(most_tempting[0], most_tempting[1], player, self.board)==True:
            self.make_move(most_tempting[0], most_tempting[1], player, self.board)
        self.swap()

    #Function to perform greedy search move with H2. 
    def greedy_search_H2(self, player): 
        self.start_move(player)
        #Defining the weights for each tile on the board, H2. 
        weights= np.array([
        [ 4,  -3,   2,   2,   2,   2,  -3,   4 ],
        [-3,  -4,  -1,  -1,  -1,  -1,  -4,  -3 ],
        [ 2,  -1,   1,   0,   0,   1,  -1,   2 ],
        [ 2,  -1,   0,   1,   1,   0,  -1,   2 ],
        [ 2,  -1,   0,   1,   1,   0,  -1,   2 ],
        [ 2,  -1,   1,   0,   0,   1,  -1,   2 ],
        [-3,  -4,  -1,  -1,  -1,  -1,  -4,  -3 ],
        [ 4,  -3,   2,   2,   2,   2,  -3,   4 ]
        ])
        print("Greedy search is making a move")
        time.time()
        most_tempting=None
        weight=-math.inf
        available_moves=self.available_moves(player, self.board) 
        self.print_moves(available_moves)
        for move in available_moves: 
            if weights[move[0]][move[1]]>weight:
                weight=weights[move[0]][move[1]] 
                most_tempting=move
        if most_tempting!=None and self.valid_move(most_tempting[0], most_tempting[1], player, self.board)==True:
            self.make_move(most_tempting[0], most_tempting[1], player, self.board)
    
    #Simulated Annealing.

    # Simulated Annealing to find optimal move:
    def simulated_annealing(self, player):
        self.start_move(player)
        temperature = 1.0 #Defining the parameters. 
        cooling_rate = 0.6
        available_moves = self.available_moves(self.current_player, self.board)
        self.print_moves(available_moves)
        if available_moves:
            current_move = random.choice(available_moves) #Randomly choosing a move, and begin the process. 
            current_score = self.count_flips(current_move[0], current_move[1], self.current_player)

            while temperature > 0.01: #As long as the temperature is greater than 0.01, the process continues. 
                new_move = random.choice(available_moves)
                new_score = self.count_flips(new_move[0], new_move[1], self.current_player)
                score_diff = new_score - current_score

                if score_diff > 0 or math.exp(score_diff / temperature) > random.random(): #Perform metropolis criterion if condition met. 
                    current_move, current_score = new_move, new_score

                temperature *= cooling_rate
            
            if current_move!=None and self.valid_move(current_move[0], current_move[1], self.current_player, self.board)==True:
                self.make_move(current_move[0], current_move[1], self.current_player, self.board)
                self.swap() 
    
    #Minimax. 

    #Function to perform Minimax move. 
    def minimax(self, player): 
        self.start_move(player)
        available_moves=self.available_moves(self.current_player, self.board) 
        self.print_moves(available_moves)
        best_move = self.minimax_decision(player)
        if best_move:
            x, y = best_move
            self.make_move(x, y, self.current_player, self.board) 
        self.swap() 

    # Minimax decision function
    def minimax_decision(self, player):
        current_player=player 
        current_opponent=-player
        weights= np.array([
        [ 4,  -3,   2,   2,   2,   2,  -3,   4 ],
        [-3,  -4,  -1,  -1,  -1,  -1,  -4,  -3 ],
        [ 2,  -1,   1,   0,   0,   1,  -1,   2 ],
        [ 2,  -1,   0,   1,   1,   0,  -1,   2 ],
        [ 2,  -1,   0,   1,   1,   0,  -1,   2 ],
        [ 2,  -1,   1,   0,   0,   1,  -1,   2 ],
        [-3,  -4,  -1,  -1,  -1,  -1,  -4,  -3 ],
        [ 4,  -3,   2,   2,   2,   2,  -3,   4 ]
        ])
        best_move = None
        best_value = float('-inf')
        available_moves=self.available_moves(current_player, self.board) 
        if available_moves:
            for move in available_moves: #Testing out all the moves. 
                temp_board = np.copy(self.board) 
                self.make_move(move[0], move[1], current_player, temp_board) 
                value= self.minimax_value(1, move, temp_board, current_opponent, original_turn=self.turn(), current_turn=self.turn()) 
                move_value= weights[move[0]][move[1]]+value
                if move_value > best_value: 
                    best_value = move_value 
                    best_move = move 
            return best_move
        else:
            return False

    #Defining the Minimax Value function:
    def minimax_value(self, depth, move, board, player, original_turn, current_turn): 
        current_player=player 
        current_opponent=-player

        if depth==self.max_depth or self.game_over():
            return self.heuristic(board, player)  
        else:
            available_moves=self.available_moves(current_player, board) 
            if available_moves:
                if current_turn!=original_turn:
                    best_move_value = float('-inf')
                else: 
                    best_move_value = float('inf')

                for move in available_moves:
                    temp_board = np.copy(board)
                    self.make_move(move[0], move[1], player, temp_board) 
                    self.temp_swap(current_player, current_opponent, temp_board) 
                    current_turn = -current_turn
                    value = self.minimax_value(depth + 1, move, temp_board, current_opponent, original_turn, current_turn)
                    if original_turn== current_turn: 
                        best_move_value = max(best_move_value, value) 
                    else: 
                        best_move_value = min(best_move_value, value)
                return best_move_value
            else: #If no available moves, then skip to the next player. 
                return self.minimax_value(depth + 1, move, self.board, current_opponent, original_turn, current_turn)

    def temp_swap(self, player, opponent, board): 
        player, opponent = opponent, player 
        
    #Function to define the heuristic. 
    def heuristic(self, board, player): 
        p, o =self.score(board)
        if player==self.player:
            return p-o
        else:
            return o-p 

    #Function to print available moves. 
    def print_moves(self, available_moves):
        if available_moves:
            print("Available moves are:")
        else: 
            print("No avilable moves for the current player.")
        for move in available_moves:
            print(move, "opponent coin flips:", self.count_flips(move[0], move[1], self.current_player))
        print("\n")

board=np.zeros((8,8)) 
game=Othello(board) 
print("Welcome to Othello!") 
play=True
while play: 
    game.start_pos()
    print("Would you like to play against the computer or another player? Enter 1 or 2") 
    choice=input()
    game.play(choice) 
    print("Would you like to play again? 1-yes, press any key to exit") 
    choice=input() 
    if choice=="1":
        continue
    else:
        play=False
print("Thank you for playing!") 

'''
Game Rule:
  -> Given the 11 x 11 board, the user is given two options: 
      1. Player vs Self 2. Player vs Bot
  -> The maximum amount of play in total would be 121 Steps, assuming the fact no player have reached five-in-a-row
  -> The only way to win the game is by placing 5 pieces in a sequence(Horizontally, Vertically, Diagonally).
  -> First player to reach the sequence win.
'''

# Define Game Board
# Game Board Size: 11 x 11
Game_Board = [[' ' for _ in range(11)] for _ in range(11)]
gameTurn = [0, 1] * 60

# Define Player Token
Player = 'O'
Guest = 'X'
player_dict = {0: 'O', 1: 'X'}
player_name = {0: 'Player', 1: 'Guest'}

# Define Win Condition
class check_win():
      matchWinner = ''
  
      def __init__(self, playerID, row, column):
          self.playerID = int(playerID)  
          self.row = int(row)
          self.col = int(column)
        
      def check_row_column(self):
            rowID = self.row
            colID = self.col
            Game_Board_Row = Game_Board[rowID]
            Game_Board_Col = [Game_Board[rowID][colID] for rowID in range(0, 11)]
            
            for scanID in range(11 - 4): 
                combinedRowChar = ''.join(Game_Board_Row[scanID:scanID+5])
                combinedColChar = ''.join(Game_Board_Col[scanID:scanID+5]) 
                if combinedRowChar == player_dict[self.playerID] * 5 or combinedColChar == player_dict[self.playerID] * 5:
                    self.matchWinner = player_name[self.playerID]

      def check_diagonal(self):
            # Diagonal Positive Slope
            row = self.row
            col = self.col

            # Define points on positive slope
            rightUpCord = []
            leftDownCord = []

            # Right Up
            rightUpRange = 0
            if abs(col - 10) > 10 - row: # If more space to go side than up
                rightUpRange = abs(col - 10)
            if abs(col - 10) < 10 - row:
                rightUpRange = 10 - col    
            for _ in range(rightUpRange):
                # Moving in up-right direction
                row = row - 1
                col = col + 1
                if row < 0:
                   continue
                rightUpCord.append([row, col])
              
            # Left Down
            leftDownRange = 0
            if 10 - row > col:
                leftDownRange = col
            if 10 - row < col:
                leftDownRange = 10 - row
            for _ in range(leftDownRange):
                row = row + 1
                col = col - 1
                if row < 0:
                   continue
                leftDownCord.append([row, col])

            # Convert the two lists to sets
            rightUpSet = set(tuple(x) for x in rightUpCord)
            rightDownSet = set(tuple(x) for x in leftDownCord)

            # Combine the two sets and convert back to a list
            combined_set = rightDownSet.union(rightUpSet)
            combined_list = [list(x) for x in combined_set]
            poscombined_list = sorted(combined_list, key=lambda x: x[0])

            # Diagonal Negative Slope
            row = self.row
            col = self.col
            
            # Define points on positive slope
            leftUpCord = []
            rightDownCord = []
        
            # Left Up 
            leftUpRange = 0
            if row > col:
                leftUpRange = col
            if row < col:
                leftUpRange = row
            for _ in range(leftUpRange):
                row = row - 1
                col = col - 1
                if row < 0:
                  continue
                leftUpCord.append([row, col])

            # Right Down
            rightDownRange = 0
            if 10 - row > 10 - col:
                rightDownRange = 10 - col
            if 10 - row < 10 - col:
                rightDownRange = 10 - row
            for _ in range(rightDownRange):
                row = row + 1
                col = col + 1
                if row < 0:
                    continue
                rightDownCord.append([row, col])

            # Convert the two lists to sets
            leftUpCord = set(tuple(x) for x in leftUpCord)
            rightDownCord = set(tuple(x) for x in rightDownCord)

            # Combine the two sets and convert back to a list
            combined_set = leftUpCord.union(rightDownCord)
            combined_list = [list(x) for x in combined_set]
            negcombined_list = sorted(combined_list, key=lambda x: x[0])

            # Define Player
            current_player = player_name[self.playerID]

            # Define lists to store point value
            posSlopeVal = [Game_Board[cord[0]][cord[1]] for cord in poscombined_list]
            negSLopeVal = [Game_Board[cord[0]][cord[1]] for cord in negcombined_list]
            for scanID in range(11 - 4):
                combinedRowChar = ''.join(posSlopeVal[scanID:scanID+5])
                if combinedRowChar == player_dict[self.playerID] * 5:
                    self.matchWinner = current_player
            for scanID in range(11 - 4): 
                combinedRowChar = ''.join(negSLopeVal[scanID:scanID+5]) 
                if combinedRowChar == player_dict[self.playerID] * 5:
                    self.matchWinner = player_name[self.playerID]

# Display Board
def display_board(board):
    num_cols = len(board[0])
    num_rows = len(board)
    
    # Print column numbers
    col_num_str = '    '
    for col in range(num_cols):
        col_num_str += f' {col}  '
    print(col_num_str)
    
    # Print top border
    print('   ' + '-' * (num_cols * 4 + 1))
    
    # Print rows
    for row in range(num_rows):
        if row < 10:
            row_str = f'{row}  |'
        else:
            row_str = f'{row} |'
        for col in range(num_cols):
            row_str += ' {} |'.format(board[row][col])
        print(row_str)
        
        # Print bottom border
        print('   ' + '-' * (num_cols * 4 + 1))

def clearBoard():
    global Game_Board
    Game_Board = [[' '] * 11] * 11

def play_move(player):
    global Game_Board
    move = input('{}, Select a location: '.format(player_name[player]))
    move_cord = move.split(',')
    if ''.join(move_cord) == move:
        print("Input not valid")
        return play_move(player)
    row = int(move_cord[0])
    col = int(move_cord[1])
    if Game_Board[row][col] == ' ':
        Game_Board[row][col] = player_dict[player]
        return move_cord
    if Game_Board[row][col] != ' ':
        print("Location already taken.")
        return play_move(player)

def GamePlay():
    global gameTurn
    gameTurn = [0, 1] * 60
    display_board(Game_Board)
    for playerID in gameTurn:  # 0, 1, 0, 1
        moveCord = play_move(playerID)  # Coordinate of user's piece
        display_board(Game_Board)
        # Check Win Condition\
        checkWin = check_win(playerID, moveCord[0], moveCord[1])
        checkWin.check_row_column()
        checkWin.check_diagonal()
        if checkWin.matchWinner != '':
            clearBoard()
            print("{} Wins!".format(checkWin.matchWinner))
            rematch = input("Do you want to play again?: ")
            if rematch in ['Yes', 'yes', 'ye', 'y']:
                return GamePlay()
            if rematch in ['No', 'no', 'nah', 'n']:
                GameMenu() 
            print('---------------Game Over---------------')
            break 
    if checkWin.matchWinner == '':
        clearBoard()
        print("Tie Game!")
        rematch = input("Do you want to play again?: ")
        if rematch in ['Yes', 'yes', 'ye', 'y']:
            return GamePlay()
        if rematch in ['No', 'no', 'nah', 'n']:
            GameMenu() 
        print('---------------Game Over---------------')

def GameMenu():
    print("1. Local Play\n2. Quit\n")
    userInp = input("Select an option: ")
    if userInp in ['1', '2']:
        if userInp == '1':
            GamePlay()
        if userInp == '2':
            quit()
    else:
        print("Please input a valid option")
        return GameMenu()

print("Welcome to the Five-in-a-Row Game")
GameMenu()

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

# Define Match Winner
matchWinner = ''

# Define Win Condition
class check_win():
      # playerID: 0 or 1
      # player_cord = [3,4] 
      def check_row(playerID: int, player_cord: list):
            global matchWinner
            current_player = player_name[playerID]
            rowID = int(player_cord[0]) # the Y-value of the piece
            Game_Board_Row = Game_Board[rowID]
            
            # Iterate through the row array and combine 5 characters at a time and verify
            for scanID in range(11 - 4): # len(Game_Board_Row) == 11
                combinedRowChar = ''.join(Game_Board_Row[scanID:scanID+5]) # len(combinedRowChar) == 5
                if combinedRowChar == player_dict[playerID] * 5:
                    matchWinner = current_player

      def check_column(playerID: int, player_cord: list):
            global matchWinner
            current_player = player_name[playerID]
            colID = int(player_cord[1])

            # Obtain all the values on the vertical line 
            Game_Board_Col = [Game_Board[rowID][colID] for rowID in range(0, 11)]
            for scanID in range(11 - 4): # len(Game_Board_Row) == 11
                combinedColChar = ''.join(Game_Board_Col[scanID:scanID+5]) # len(combinedColChar) == 5
                if combinedColChar == player_dict[playerID] * 5:
                    matchWinner = current_player

      def diagonal_positiveSlope(playerID: int, player_cord: list):
            row = int(player_cord[0]) # Y-value 
            col = int(player_cord[1]) # X-value 

            # Define points on positive slope
            rightUpCord = []
            leftDownCord = []

            # Right Up
            if abs(col - 10) > 10 - row: # If more space to go side than up
                for _ in range(abs(col - 10)):
                    # Moving in up-right direction
                    row = row - 1
                    col = col + 1
                    if row < 0:
                       continue
                    rightUpCord.append([row, col])
            if abs(col - 10) < 10 - row:
                for _ in range(10 - col): 
                    # Moving in up-right direction
                    row = row - 1
                    col = col + 1
                    if row < 0:
                       continue
                    rightUpCord.append([row, col])
            # Left Down
            if 10 - row > col:
               for _ in range(col):
                   row = row + 1
                   col = col - 1
                   if row < 0:
                      continue
                   leftDownCord.append([row, col])
            if 10 - row < col:
               for _ in range(10 - row):
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
            return poscombined_list

      def diagonal_negativeSlope(playerID: int, player_cord: list):
            row = int(player_cord[0]) # Y-value 
            col = int(player_cord[1]) # X-value 
            
            # Define points on positive slope
            leftUpCord = []
            rightDownCord = []
            # Left Up 
            if row > col:
               for _ in range(col):
                   row = row - 1
                   col = col - 1
                   if row < 0:
                      continue
                   leftUpCord.append([row, col])
            if row < col:
               for _ in range(row):
                   row = row - 1
                   col = col - 1
                   if row < 0:
                      continue
                   leftUpCord.append([row, col])

            # Right Down
            if 10 - row > 10 - col:
               for _ in range(10 - col):
                   row = row + 1
                   col = col + 1
                   if row < 0:
                      continue
                   rightDownCord.append([row, col])
            if 10 - row < 10 - col:
               for _ in range(10 - row):
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
            return negcombined_list
      
      def check_diagonal(playerID: int, player_cord: list):
            global matchWinner
            # Lists contained all coordiantes for the points
            posSlopeArr = check_win.diagonal_positiveSlope(playerID, player_cord)
            negSlopeArr = check_win.diagonal_negativeSlope(playerID, player_cord)

            # Define Player
            current_player = player_name[playerID]

            # Define lists to store point value
            posSlopeVal = [Game_Board[cord[0]][cord[1]] for cord in posSlopeArr]
            negSLopeVal = [Game_Board[cord[0]][cord[1]] for cord in negSlopeArr]
            for scanID in range(11 - 4):
                combinedRowChar = ''.join(posSlopeVal[scanID:scanID+5])
                if combinedRowChar == player_dict[playerID] * 5:
                    matchWinner = current_player
            for scanID in range(11 - 4): 
                combinedRowChar = ''.join(negSLopeVal[scanID:scanID+5]) 
                if combinedRowChar == player_dict[playerID] * 5:
                    matchWinner = current_player

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
        # Check Win Condition
        check_win.check_row(playerID, moveCord)
        check_win.check_column(playerID, moveCord)
        check_win.check_diagonal(playerID, moveCord)
        if matchWinner != '':
            clearBoard()
            print("{} Wins!".format(matchWinner))
            print('-------------------------------')
            break 
    if matchWinner == '':
        clearBoard()
        print("Tie Game!")
        print('-------------------------------')

GamePlay()

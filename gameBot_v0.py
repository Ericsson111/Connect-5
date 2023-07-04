# Python 3.8.6
# 2023/06/27
"""
Python Connect-5 Bot 
    -> Identify possible routes: Given the player's latest input coordinates, you aim to find all 
        possible routes (arrays) in different directions, such as horizontal, vertical, and diagonal.

    -> Sort arrays by the number of player's pieces: You suggest sorting these arrays based on the number 
        of player's pieces present. Sorting them in descending order would allow you to prioritize routes 
        with more player's pieces, potentially indicating a higher chance of success.

    -> Find the optimized array: By selecting the array with the most player's pieces, 
        you identify a potentially advantageous position. This optimized array becomes the focus for the bot's next move.
        Ensure the array contains the least amount of Bot's pieces.

    -> Find the two end-points: With the optimized array in hand, you extract the 
        two end-points (e.g., [0, 0, x, x, 0, 0]) to determine the potential move that would lead to a win.

    -> Evaluate potential moves recursively: You propose using recursion to evaluate the possible 
        moves from the two end-points. By analyzing the subsequent board positions resulting from different moves, 
        you aim to identify the move that offers the player a higher chance of winning.

    -> Place a piece on the chosen coordinate: Based on the evaluation, the bot would place its 
        piece on the coordinate that offers the best chance of success.
"""

import random 
random.seed()

class GameBot():

    # First Move by the Bot
    def Bot_Starting_Move(playerCoordinate: list): 
        # The game is designed for the Player to always go first
        # The Bot will randomly select the Player's piece's surronding and place it's piece

        playerRow, playerCol = playerCoordinate

        BotPiecePlacement = random.randint(1, 4)
        
        if BotPiecePlacement == 1:  # Horizontal
            playerRow += random.choice([-1, 1])
        elif BotPiecePlacement == 2:  # Vertical
            playerCol += random.choice([-1, 1])
        elif BotPiecePlacement == 3:  # Positive Slope Diagonal
            playerCol += 1
            playerRow += random.choice([-1, 1])
        else:  # Negative Slope Diagonal
            playerCol -= 1
            playerRow += random.choice([-1, 1])
        
        return [playerRow, playerCol] 


    # Identify possible routes
    """
    check_win() object from main.py provides arrays containing all possible routes of the Player's piece
        -> Obtain the arrays from the check_row_column() and check_diagonal() function 
    """
    # Determine which route the Player has the highest chance winning (Horizontal, Vertical, Diagonal)
    def Identify_Player_Possible_Routes(empty, horizontalArray, verticalArray, positiveDiagonalArray, negativeDiagonalArray, playerCoordinate):
        # positiveDiagonalArray is the diagonal line with positive slope
        # negativeDiagonalArray is the diagonal line with negative slope
        
        # Objective: Classify arrays based on the value(amount of Player's piece) it contain
        """
        Visual Representation of "possibleArrays" and "possibleArraysValue"
        CoordinatesArrayName = {0: [[3, 0], [4, 1], [5, 2], [6, 3], [7, 4], [8, 5], [9, 6], [10, 7]], 1: [...], ...}
        ArraysCoordinates = {[[3, 0], [4, 1], [5, 2], [6, 3], [7, 4], [8, 5], [9, 6], [10, 7]]: [' ', ' ', ' ', ' ', 'X', 'O', 'O', ' ', ' ', 'X', ' '], ...}
        possibleArrays = [[' ', ' ', ' ', ' ', 'X', 'O', 'O', ' ', ' ', 'X', ' '], [...], [...], [...]]
        possibleArraysValue = {[' ', ' ', ' ', ' ', 'X', 'O', 'O', ' ', ' ', 'X', ' ']: 2, [...]: 3, [...]: 3, [...]: 3}
        """
        possibleArrays = [horizontalArray, verticalArray, positiveDiagonalArray, negativeDiagonalArray] # 2-D Matrix
        possibleArraysName = ["Horizontal", "Vertical", "PositiveDiagonal", "NegativeDiagonal"] # Only purpose is to be used while displaying the message
        CoordinatesArrayName = {} # possibleArrays Index correspond with the array's coordinates
        ArraysCoordinates = {} # array's coordinates correspond with it's actual representation(original array)
        possibleArraysValue = {} # array correspond with it's Player's piece value
        # Step: Adding the array and it's corresponding number of Player's pieces into the "possibleArrayValue" dictionary
        for routeArrayID in range(len(possibleArrays)):
            routeArrayVal = len(list(filter(lambda x: x == 'O', possibleArrays[routeArrayID]))) # Remove all Bot's pieces from the array
            possibleArraysValue[routeArrayID] = routeArrayVal
            CoordinatesOfArray = Find_Coordinates_Of_Arrays(playerCoordinate, possibleArraysName[routeArrayID])
            CoordinatesArrayName[routeArrayID] = CoordinatesOfArray
            CoordinatesOfArray = str(CoordinatesOfArray)
            ArraysCoordinates[CoordinatesOfArray] = possibleArrays[routeArrayID]
        print("CoordinatesArrayName:",CoordinatesArrayName)
        print("ArraysCoordinates:",ArraysCoordinates)
        print("-" * 50)
        
        for arrayID in range(4):
            print(possibleArraysName[arrayID],":",possibleArrays[arrayID])
        
        # Objective: Sort arrays by the numberof Player's pieces it contains

        # Step: If Player's piece is less or equal to 2 on every array
        # Step: The move is considered un-threatening 
        # Step: Find the next coordinate placement for the bot to win the match

        # Step: Ensure the "highestArrayValue" is unique, so no repetitive value exist in the dictionary
        if len(list(dict.fromkeys(possibleArraysValue))) < len(possibleArraysValue): # If there are duplicated values accross different arrays
            
            # Step: Loop through the amount of duplicated arrays 
            # Step: Find the array with least amount of Bot's pieces -> Lower the chance for Player to win the game
            # Objective: Return the specific target array 

            # Step: Remove the array that does not have the highest value(Player's pieces)
            highestArrayValue = sorted([arrayVal for arrayVal in possibleArraysValue.values()])[-1] # The highest from the sorted values

            for arrayType, arrayVal in possibleArraysValue.items():
                if arrayVal < highestArrayValue: # If the array is not equal to the highestArrayValue, it will not be considered as an option
                    # Remove the array from the "possibleArraysValue" dictionary
                    del possibleArraysValue[arrayType]

        # Find the array with maximum amount of Player's pieces
        maximumArray = []
        maximumArrayVal = sorted([arrayVal for arrayVal in possibleArraysValue.values()])[-1]
        for arrayID, arrayVal in possibleArraysValue.items():
            print("arrayID:",arrayID, " | ", "arrayVal:",arrayVal, " | ", "array:", possibleArrays[arrayID])
            if arrayVal == maximumArrayVal:
                maximumArray.append(possibleArrays[arrayID])
        
        if len(maximumArray) == 1: # No duplication on the maximum Player's pieces val
            # Use the given maximum array to find the two end point
            pass 

        else:
        
            # If no duplication arrays
            # Step: Now the dictionary only consists of the values with maximum amount of Player's pieces in an array
            #       -> possibleArraysValue dictionary has been cleaned
            # Step: Determine the array with least amount of Bot's pieces

            # minimumBotPiecesCount = Number(Least amount of Bot's pieces in one array)
            minimumBotPiecesCount = [len(list(filter(lambda x: x == 'X', maximumArray[arrayScanID]))) for arrayScanID in range(len(maximumArray))][0]

            # Step: Since the maximumArray contains arrays with the most amount of Player's pieces, now we find the one with least amount of Bot's pieces
            minimumBotPiecesArray = []
            for arrayScanID in range(len(maximumArray)): # The amount of array that must be passed through
                BotPiecesCount = len(list(filter(lambda x: x == 'X', maximumArray[arrayScanID]))) 
                if BotPiecesCount == minimumBotPiecesCount:
                    minimumBotPiecesArray.append(maximumArray[arrayScanID])

            # If both array contains the same amount of Player's pieces and Bot's pieces
            # Step: Determine which array consists more threats -> Find the array with greatest section connection
            
            
            if len(minimumBotPiecesArray) > 1:
                maximumSectionLength = 0
                maximumSectionLengthArray = []
                for arrayScanID in range(len(minimumBotPiecesArray)):
                    targetArray = []
                    targetArrayCoordinates = []
                    for coordinates, array in ArraysCoordinates.items(): # Find the coordinates of the given array
                        if array == minimumBotPiecesArray[arrayScanID]:
                            targetArray = str(array)
                            targetArrayCoordinates = coordinates


                    currentArray = minimumBotPiecesArray[arrayScanID]
                    maximumLength = 0 
                    startingPoint = []
                    endingPoint = [] 

                    targetArray = eval(targetArray)
                    targetArrayCoordinates = eval(targetArrayCoordinates)

                    for arrayScanID in range(len(targetArray)):
                        if targetArray[arrayScanID] == 'O':  # If it's Player's piece
                            phaseLength = 0
                            for playerScanID in range(arrayScanID, len(targetArray)):
                                if targetArray[playerScanID] == 'O':
                                    phaseLength += 1
                                elif targetArray[playerScanID] == 'X' or targetArray[playerScanID] == ' ':
                                    if phaseLength > maximumLength:
                                        maximumLength = phaseLength
                                        startingPoint = targetArrayCoordinates[arrayScanID]
                                        endingPoint = targetArrayCoordinates[playerScanID - 1]
                                    break
        
                            print("phaseLength:", phaseLength, " | ", "maximumLength:", maximumLength)
                            print("Starting:", startingPoint, " | ", "endingPoint:", endingPoint)
                            print("-"*50)

                print("minimumBotPiecesArray:", minimumBotPiecesArray)
            

            else: # Only one array left
                maximumLength = 0 
                startingPoint = []
                endingPoint = [] 
                for charScanID in range(len(currentArray)):

                    if currentArray[charScanID] == 'O': # If it's Player's piece
                        phaseLength = 0
                        for playerScanID in range(charScanID, len(currentArray)):
                            if currentArray[playerScanID] == 'O':
                                phaseLength += 1
                            elif currentArray[playerScanID] == 'X' or currentArray[playerScanID] == ' ':
                                if phaseLength > maximumLength: 
                                    maximumLength = phaseLength
                                    startingPoint = targetArrayCoordinates[charScanID]
                                    endingPoint = targetArrayCoordinates[playerScanID-1]
                                break
        
            # Objective: Determine the two coordinates of the two end-point
            # Step: Given the array with minimum amount of the Bot's Pieces
            # Step: Find the two coordinates on end of Player's pieces within the array

            targetArrayName = possibleArraysName[list(ArraysCoordinates.keys()).index(str(targetArrayCoordinates))] # Find the name of the line(horizontal, vertical, etc)
            print("-" * 50)
            print("targetArray:", targetArray, type(targetArray))
            print("targetArrayCoordinates:", targetArrayCoordinates, type(targetArrayCoordinates))
            print("targetArrayName:",targetArrayName)

            print("Starting point:", startingPoint)
            print("Ending point:", endingPoint)

            # Now, given the two end-points of the Player's pieces
            # Step: Determine the two coordinates the Bot could place it's piece on
            BotInterceptionPoint1 = targetArrayCoordinates.index(startingPoint) - 1 # The point before the Player's connection begins
            BotInterceptionPoint2 = targetArrayCoordinates.index(endingPoint) + 1 # The point after the Player's connection begin
            potentialBotPiecesPlacement = [targetArrayCoordinates[BotInterceptionPoint1], targetArrayCoordinates[BotInterceptionPoint2]]
            
            if targetArrayCoordinates[BotInterceptionPoint1] == "X": 
                # If starting point has been occupied by Bot's piece
                # The otherside(end-point) should be empty
                potentialBotPiecesPlacement.remove(targetArrayCoordinates[BotInterceptionPoint1]) # Remove from possible move
            if targetArrayCoordinates[BotInterceptionPoint2] == "X":
                potentialBotPiecesPlacement.remove(targetArrayCoordinates[BotInterceptionPoint2]) # Remove from possible move

            # Objective: Determine the most opimized coordinate for Bot's piece placement
            if len(potentialBotPiecesPlacement) == 1:
                return potentialBotPiecesPlacement[0]
            elif len(potentialBotPiecesPlacement) > 1:
                choiceID = random.randint(0, 1)
                print("potentialBotPiecesPlacement[choiceID]:",potentialBotPiecesPlacement[choiceID])
                return potentialBotPiecesPlacement[choiceID]
                """
                InterceptionArrays1 = [] # For starting point
                InterceptionArrays2 = [] # For ending point
                
                possibleArraysName.remove(targetArrayName)

                for checkPointID in range(3): # There will be three arrays to check once the current array is removed
                    InterceptionArrays1.append(Find_Coordinates_Of_Arrays(potentialBotPiecesPlacement[0], possibleArraysName[checkPointID]))
                    InterceptionArrays2.append(Find_Coordinates_Of_Arrays(potentialBotPiecesPlacement[1], possibleArraysName[checkPointID]))
                """
    
def Find_Coordinates_Of_Arrays(PlayerCoordinate: list, ArrayType: str):
    # Array = [' ', ' ', ' ', ' ', 'X', 'O', 'O', ' ', ' ', 'X', ' ']
    # PlayerCoordinate = [4, 5]
    # ArrayType = Horizontal, Vertical, Diagonal

    # Goal: Determine all the coordinates of the array based on the "PlayerCoordinate" and "ArrayType"
    # Ste: Given the "PlayerCoordinate", it is possible to find the nearby coordinates based on the
    #       "ArrayType" pattern. The coordinates can be extrapolated and will be remsembled in a new array
    #       The array that will be returned would look somewhat like this:
    #       coordinateArray = [[2,0], [2,1], [2,2], [2,3], ...] 
    rowVal, colVal = PlayerCoordinate
    rowVal, colVal = int(rowVal), int(colVal)
    if ArrayType == "Horizontal":
        # Given the "ArrayType" of "Horizontal"
        # The coordinates could simply be found with the "row" value provided within the "PlayerCoordinate"
        coordinateArray = [[rowVal, colVal] for colVal in [i for i in range(1, 11)]]
    elif ArrayType == "Vertical":
        coordinateArray = [[rowVal, colVal] for rowVal in [i for i in range(1, 11)]]
    elif ArrayType == "PositiveDiagonal":
        rightUpCord = []
        leftDownCord = []

        # Right Up
        rightUpRange = min(abs(colVal - 10), 10 - rowVal)
        for _ in range(rightUpRange):
            # Moving in up-right direction
            rowVal -= 1
            colVal += 1
            if rowVal < 0:
                continue
            rightUpCord.append([rowVal, colVal])

        # Left Down
        leftDownRange = min(10 - rowVal, colVal)
        for _ in range(leftDownRange):
            rowVal += 1
            colVal -= 1
            if rowVal < 0:
                continue
            leftDownCord.append([rowVal, colVal])

        # Convert the two lists to sets
        rightUpSet = set(tuple(x) for x in rightUpCord)
        rightDownSet = set(tuple(x) for x in leftDownCord)

        # Combine the two sets and convert back to a list
        combined_set = rightDownSet.union(rightUpSet)
        coordinateArray = sorted([list(x) for x in combined_set], key=lambda x: x[0])
    elif ArrayType == "NegativeDiagonal":
        leftUpCord = []
        rightDownCord = []

        # Left Up
        leftUpRange = min(rowVal, colVal)
        for _ in range(leftUpRange):
            rowVal -= 1
            colVal -= 1
            if rowVal < 0:
                continue
            leftUpCord.append([rowVal, colVal])

        # Right Down
        rightDownRange = min(10 - rowVal, 10 - colVal)
        for _ in range(rightDownRange):
            rowVal += 1
            colVal += 1
            if rowVal < 0:
                continue
            rightDownCord.append([rowVal, colVal])

        # Convert the two lists to sets
        leftUpCord = set(tuple(x) for x in leftUpCord)
        rightDownCord = set(tuple(x) for x in rightDownCord)

        # Combine the two sets and convert back to a list
        combined_set = leftUpCord.union(rightDownCord)
        coordinateArray = sorted([list(x) for x in combined_set], key=lambda x: x[0])
    return coordinateArray

Gamebot = GameBot()

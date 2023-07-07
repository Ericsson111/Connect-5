# Python 3.9.6 64-bit

import random

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
        coordinateArray = [[rowVal, colVal] for colVal in [i for i in range(0, 11)]]
    elif ArrayType == "Vertical":
        coordinateArray = [[rowVal, colVal] for rowVal in [i for i in range(0, 11)]]
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

def GameBot_Move(Game_Board: list, allArrays: list, playerCoordinate: list):
    arrayNames = ["Horizontal", "Vertical", "PositiveDiagonal", "NegativeDiagonal"]
    # allArrays consists all the arrays that passes through "playerCoordinate"
    # Horizontal, Vertical, Positive/Negative Diagonal
    ArrayCoordinates = {} # Array: Coordinates -> Used to match up with the correct set of coordinates
    CoordinatesArrayID = {} # ID: Coordinates -> Used to match up with the correct array

    # arrayDictID: Iteration use and the only purpose is to update the data into the dictionary
    for arrayDictID in range(len(arrayNames)):
        possibleArraysCoordinates = Find_Coordinates_Of_Arrays(playerCoordinate, arrayNames[arrayDictID])
        ArrayCoordinates[str(allArrays[arrayDictID])] = possibleArraysCoordinates
        CoordinatesArrayID[arrayDictID] = possibleArraysCoordinates
    print("Allarrays:", allArrays)

    """ ###### Connection-Streak Verification ###### """
    # How many Player's pieces on a line does not matter, how many are connected matters more
    connectionStreakValueDict = {}
    connectionStreakCoordinateDict = {}

    for arrayCSVID in range(len(allArrays)): # CSV: Connection-Streak Verification

        currentArray = allArrays[arrayCSVID]
        currentArrayCoordinates = CoordinatesArrayID[arrayCSVID]
        maximumLength = 0 
        startingPoint = None 
        endingPoint = None
        for charScanID in range(len(currentArray)):

            if currentArray[charScanID] == 'O': # If it's Player's piece
                phaseLength = 0
                for playerScanID in range(charScanID, len(currentArray)):
                    if currentArray[playerScanID] == 'O':
                        phaseLength += 1
                    elif currentArray[playerScanID] == 'X' or currentArray[playerScanID] == ' ':
                        if phaseLength > maximumLength: 
                            maximumLength = phaseLength
                            startingPoint = currentArrayCoordinates[charScanID]
                            endingPoint = currentArrayCoordinates[playerScanID-1]
                        break
        
        connectionStreakValueDict[arrayCSVID] = maximumLength
        connectionStreakCoordinateDict[arrayCSVID] = [startingPoint, endingPoint]

    availableArrays = {}

    # Check the arrays that the Player can actually connect 5 pieces
    # Meaning the connection-streak and the enarby empty slots adds up to 5

    # arraySSID: Array Surronding Scan ID
    for arraySSID in range(len(allArrays)):
        # Check both side of the array with "startingPoint" and "endingPoint"
        currentArray = allArrays[arraySSID]
        currentArrayCoordinates = ArrayCoordinates[str(currentArray)]
        startingPoint, endingPoint = connectionStreakCoordinateDict[arraySSID]
        startingPointInd = ArrayCoordinates[str(currentArray)].index(startingPoint)
        endingPointInd = ArrayCoordinates[str(currentArray)].index(endingPoint)

        playerRemainingPieceToWin = 5 - connectionStreakValueDict[arraySSID] 

        """ 
        The Player would have between 1 - 3 pieces on an array for most of the time
        
        """
        
        print("currentArray:",currentArray)
        print("startingPoint:",startingPoint, "startingPointInd:", startingPointInd)
        print("endingPoint:",endingPoint, "endingPointInd:",endingPointInd)
        print("playerRemainingPieceToWin:",playerRemainingPieceToWin)

        # Check in front of the startingPoint of Player's Connection-Streak
        startScanIssueID = [startScanID for startScanID in range(startingPointInd, 0, -1) if currentArray[startScanID] == 'X']
        endScanIssueID = [endScanID for endScanID in range(endingPointInd, len(currentArray), 1) if currentArray[endScanID] == 'X']
        print("startScanIssueID:",startScanIssueID, "endScanIssueID:",endScanIssueID)

        if len(startScanIssueID) >= 1 and len(endScanIssueID) >= 1:
            # There are Bot pieces both in front and behind the Player's connection-streak
            print("len(startScanIssueID) >= 1 and len(endScanIssueID) >= 1") 

            if endScanIssueID[0] - startScanIssueID[0] > 5:
                availableArrays[str(currentArray)] = (endScanIssueID[0] - startScanIssueID[0]) - 1
            else:
                print("currentArray1:",currentArray, " is not available")

        elif len(startScanIssueID) == 0 and len(endScanIssueID) > 0: 
            # The Bot pieces are on the right side of the Player's connection-streak
            # The Player could only expand on it's left
            print("len(startScanIssueID) == 0")

            if (endScanIssueID[0] - 1) >= 5:
                # Enough empty slots to build 5 connections
                availableArrays[str(currentArray)] = (endScanIssueID[0] - 1)
            else:
                print("currentArray2:",currentArray, " is not available")

        elif len(startScanIssueID) > 0 and len(endScanIssueID) == 0:
            # The Bot pieces are on the left side of the Player's connection-streak
            # The Player could only expand on it's right
            print("len(endScanIssueID) == 0")

            if 10 - startScanIssueID[0] > 5:
                availableArrays[str(currentArray)] = 10 - startScanIssueID[0]
        
        elif len(startScanIssueID) == 0 and len(endScanIssueID) == 0:
            print("# There are completely no Bot pieces at all on the current choosen array")
            availableArrays[str(currentArray)] = len(currentArray) 

        print("-"*50)

    print("availableArrays:",availableArrays)

GameBot_Move(
    Game_Board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' '], 
                  [' ', ' ', ' ', ' ', 'X', ' ', 'X', 'O', ' ', ' ', 'X'], 
                  [' ', ' ', ' ', ' ', 'X', 'O', 'O', 'O', ' ', ' ', ' '], 
                  [' ', ' ', ' ', 'X', 'O', 'O', 'O', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']],
    allArrays = [[' ', ' ', ' ', ' ', 'X', ' ', 'X', 'O', ' ', ' ', 'X'],
                 [' ', 'X', ' ', 'O', 'O', ' ', ' ', 'X', ' ', ' ', ' '],
                 [' ', ' ', 'X', 'O', 'O', 'O', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', 'O', ' ', ' ', ' ']],
    playerCoordinate = [3,7])

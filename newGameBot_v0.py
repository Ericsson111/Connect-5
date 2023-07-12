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

def GameBot_Move(Game_Board:list, allArrays: list, playerCoordinate: list):
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

    print("connectionStreakValueDict:",connectionStreakValueDict)
    print("connectionStreakCoordinateDict:",connectionStreakCoordinateDict)

    availableArrays = {}
    availableArraysID = {}
    availableArraysIssueID = {}
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
        
        print("currentArray:",currentArray)
        print("startingPoint:",startingPoint, "startingPointInd:", startingPointInd)
        print("endingPoint:",endingPoint, "endingPointInd:",endingPointInd)
        print("playerRemainingPieceToWin:",playerRemainingPieceToWin)

        # Check in front of the startingPoint of Player's Connection-Streak
        startScanIssueID = [startScanID for startScanID in range(startingPointInd, -1, -1) if currentArray[startScanID] == 'X']
        endScanIssueID = [endScanID for endScanID in range(endingPointInd, len(currentArray), 1) if currentArray[endScanID] == 'X']
        print("startScanIssueID:",startScanIssueID, "endScanIssueID:",endScanIssueID)


        """ ######Objective: Check if the array contains enough empty space to build up to 5 or more ######"""
        if len(startScanIssueID) >= 1 and len(endScanIssueID) >= 1:
            # There are Bot pieces both in front and behind the Player's connection-streak
            print("len(startScanIssueID) >= 1 and len(endScanIssueID) >= 1")

            if endScanIssueID[0] - startScanIssueID[0] > 5:
                availableArraysIssueID[arraySSID] = [startScanIssueID, endScanIssueID]
                availableArraysID[arraySSID] = [startingPointInd-1, endingPointInd+1]
                availableArrays[str(currentArray)] = (endScanIssueID[0] - startScanIssueID[0]) - 1
            else:
                print("currentArray1:",currentArray, " is not available")

        elif len(startScanIssueID) == 0 and len(endScanIssueID) > 0: 
            # The Bot pieces are on the right side of the Player's connection-streak
            # The Player could only expand on it's left
            print("len(startScanIssueID) == 0")

            if (endScanIssueID[0] - 1) >= 5:
                availableArraysIssueID[arraySSID] = [startScanIssueID, endScanIssueID]
                availableArraysID[arraySSID] = [startingPointInd-1, endingPointInd+1]
                availableArrays[str(currentArray)] = (endScanIssueID[0] - 1)
            else:
                print("currentArray2:",currentArray, " is not available")

        elif len(startScanIssueID) > 0 and len(endScanIssueID) == 0:
            # The Bot pieces are on the left side of the Player's connection-streak
            # The Player could only expand on it's right
            print("len(endScanIssueID) == 0")

            if 10 - startScanIssueID[0] > 5:
                availableArraysIssueID[arraySSID] = [startScanIssueID, endScanIssueID]
                availableArraysID[arraySSID] = [startingPointInd-1, endingPointInd+1]
                availableArrays[str(currentArray)] = 10 - startScanIssueID[0]
            else:
                print("currentArray3:",currentArray, " is not available")
        
        elif len(startScanIssueID) == 0 and len(endScanIssueID) == 0:
            print("# There are completely no Bot pieces at all on the current choosen array")
            availableArraysIssueID[arraySSID] = [startScanIssueID, endScanIssueID]
            availableArraysID[arraySSID] = [startingPointInd-1, endingPointInd+1]
            availableArrays[str(currentArray)] = len(currentArray) 

        print("-"*50)

    print("availableArrays:",availableArrays)
    print("availableArraysID:",availableArraysID)
    print("availableArraysIssueID:",availableArraysIssueID)

    if len(availableArrays) > 1: 
        """
        The player now has a variety of options to try and line up five pieces in a row.
        The Bot has to determine the array that poses the most significant threat.
        The threat could be identified by the Bot pieces next to the Player's connection-streak.

        The player would typically find it challenging and nearly impossible to complete this task 
        in the case of " XOOO "(case 1) because it only takes one Bot piece to break the streak.

        However if the Bot does nothing about this connection-streak in the instance of "X OOO" (case 2), 
        the Player would have a 100% win rate. ("X OOOO " <- Next phase of case 2)

        Therefore, it is crucial for the Bot to recognize the various threat levels among the lists 
        while evaluating which array is most optimized. This will allow the Bot to choose the most 
        optimal set and execute the manoeuvre that will be most effective.
        """
        

        """ ###### Objective: Find the array with Bot pieces on the side of Player's connection-streak ###### """
 
        availableArraysThreatLevel = {}
        for ArraysThreatScanID in availableArraysID.keys():
            startIssueID, endIssueID = availableArraysIssueID[ArraysThreatScanID]

            """ ###### Objective: Threat Level Identification ###### """ # Establish Bot decision structure for future use
            if len(startIssueID) == 0 and len(endIssueID) == 1 or len(startIssueID) == 1 and len(endIssueID) == 0:
                availableArraysThreatLevel[ArraysThreatScanID] = 1
            elif len(startIssueID) == 0 and len(endIssueID) == 0:
                availableArraysThreatLevel[ArraysThreatScanID] = 2
            elif len(startIssueID) == 1 and len(endIssueID) == 1:
                availableArraysThreatLevel[ArraysThreatScanID] = 3 
            """
            Now there would be three potential scenarios:
                -> The left side of the connection-streak will have a Bot piece.
                -> The right side of the connection-streak will have a Bot piece.
                -> Both side of the connection-streak will have a Bot piece.
            
            Threat Level Identification: (O is player and X is Bot)
                #1 Bot piece is found only on one side of the connection-streak (contain either startIssueID or endIssueID) -> (" OOX " or " OO X ") # Make sure to enclose Player's attempt
                #2 No Bot piece on the array (empty startIssueID and endIssueID) -> Mostly the line with very limited amount of Player's piece(" O ") # Block one side minimum
                #3 Bot piece on both side of the connection-streak (contain both startIssueID and endIssueID) -> (" XOOO  X " or "X  OO    x") # Further block Player's attempt
            """
        print("availableArraysThreatLevel:",availableArraysThreatLevel)

        PlayerConnectionStreak = [connectionStreakValueDict[availableArraysScanID] for availableArraysScanID in availableArraysID.keys()]
        equalThreatLevel = list(dict.fromkeys([threatLevel for threatLevel in availableArraysThreatLevel.values()]))
        print("PlayerConnectionStreak:",PlayerConnectionStreak)
        print("equalThreatLevel:",equalThreatLevel)

        """
        Now we must return the "Best Array" that is found to encounter Player's move.
        According to our "Threat Level Identification", the following code will allow
        the Bot to fully understand the actions that are required to taken under
        certain circumstances.
        """

        selectedArray = None 
        availableArraysBotVal = {} # array: Number of Bot pieces directly on the side of Player's connection-streak
        """ Objective: Check if the Bot pieces are directly next to the Player connection-streak ###### """
        for availableArraysScanID in range(len(availableArrays)):
            pass


'''
def Finding_Optimized_Bot_Placement(availableArrays: list, connectionStreakCoordinateDict:list, availableArraysCoordinatesID: list, allCoordinates: list): 
    for availableArraysScanID in range(len(PlayerConnectionStreak)):
        currentArray = availableArrays[availableArraysScanID]
        currentArrayThreatLevel = PlayerConnectionStreak[availableArraysScanID]
        PlayerConnectionStreak = connectionStreakCoordinateDict[availableArraysScanID]
        startingPointInd, endingPointInd = availableArraysID[availableArraysScanID]
        startIssueID, endIssueID = availableArraysIssueID[availableArraysScanID]
        '''
"""
            Bot Actions:
                #1 Determine which connection-streak is the greatest. Then deploy interception Bot piece to prevent Player from winning the game.
                    -> If all connection-streak are measured with equal length, the (#2 Threat) will be activated and determined to be the threat.
                        -> No Bot piece on each side possess greater threat than any other under the condition of equal streak length.
                    -> If (#2 Threat) cannot be activated due to the undetectable Bot piece.
                        -> (#1 Threat) will be considered as priority rather than (#3 Threat)
                    -> If (#2 Threat) cannot be activated and only one of the threat level remains while having 2 arrays.
                        -> If (#1 Threat)
                            -> Identify the one interception coordinate from each array
                            -> Use this coordinate to find the other three lines(arrays) other than the current one
                            -> Find the maximum Player connection-streak length
                            -> Compare the length on each coordinate and the winner takes on
                            -> If tied -> rd.randint(0,1)
                        -> If (#3 Threat)
                            -> Identify the two interception coordinates from each array
                            -> Use this coordinates to find the other three lines(arrays) other than the current one
                            -> Find the maximum Player connection-streak length
                            -> Compare the length on each coordinate and the winner takes on
                            -> If tied -> rd.randint(0,1)
                    -> If (#3 Threat) connection-streak is the greatest, replace with the next level threat unlessthe streak is at 4"""
'''            # Check if all "Threat Level" are the same 
            if len(equalThreatLevel) == 1: # Duplication
                if equalThreatLevel[0] == 1: # All arrays are considered (#1 Threat)
                    # Find which connection-streak is greater
                    # If tie, find the other three arrays
                    pass
                elif equalThreatLevel[0] == 2: # All arrays are considered (#2 Threat)
                    # Find which connection-streak is greater
                    # If tie, find the other three arrays
                    pass
                elif equalThreatLevel[0] == 3: # All arrays are considered (#3 Threat)
                    # Find which connection-streak is greater
                    # If tie, find the other three arrays
                    pass

            else: # No duplication
                # Find the highest connection-streak first
                pass 
'''
            
def Finding_Optimized_Bot_Placement(availableArrays: list, availableArraysCoordinatesID: list, allCoordinates: list):
    """
    availableArrays and allCoordinates are matching by it's index in the list

    Given all the arrays and the coordinates of our target, we must decide which coordinate to go with.
    First of all, we would need to use "Find_Coordinates_Of_Arrays()" to find the other three arrays for
    every coordinate, excluding the current given one. Second, we extract these arrays and find the highest
    Player connection-streak and store it in a dictionary for future comparison. Then, we would extract 
    these values and compare which ever coordinate have the highest Player connection-streak, and that 
    coordinate would be returned as Bot's final move.
    """

    """ ###### Connection-Streak Verification ###### """
    # How many Player's pieces on a line does not matter, how many are connected matters more
    connectionStreakValueDict = {}
    connectionStreakCoordinateDict = {}

    for arrayCSVID in range(len(availableArrays)): # CSV: Connection-Streak Verification

        currentArray = availableArrays[arrayCSVID]
        currentArrayCoordinates = availableArraysCoordinatesID[arrayCSVID]
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

        

GameBot_Move(
    Game_Board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', 'O', 'X', 'O', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', 'X', 'O', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', 'X', 'O', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']],
    allArrays = [[' ', ' ', ' ', ' ', 'O', 'X', 'O', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', 'O', 'X', 'X', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', 'O', ' ', ' ', ' ', ' '],
                 [' ', 'X', ' ', 'O', 'O', ' ', ' ', 'X', ' ', ' ']],
    playerCoordinate = [3,4])

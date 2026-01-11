import math
import numpy as np
import os
import random 
import sys
import re
import copy as cp

class Knowledge:
    def __init__(self, booleanStates, holesWompuses, arrows, query, test):
        self.booleanStates = cp.deepcopy(booleanStates); #  this boolean states array contains 
        # booleans variables on the following data: 
        # 0) safe, 1) unsafe, 2) breeze, 3) stench, 4) given
        
        self.arrows = arrows # number of potential wompuses
        
        self.query = query # cell we are testing
        
        self.test = test # integer indicating to test not unsafe (0) or not safe (1)
        
        self.holesWompuses = cp.deepcopy(holesWompuses); #     # creates an initial array of:
        # 0) there could be a hole 1) there could be a wompus
        # 2) there is a hole 3) there is a wompus

        arraysShape = booleanStates.shape
        
        hazardsShape = holesWompuses.shape
        
        self.rows = arraysShape[1] # number of rows in map
        self.columns = arraysShape[2] # number of columns in map
        
        self.possibleWompuses = (self.rows * self.columns)
        
        self.clausesArray = [] # record created clauses (strings)
        
        self.clausesQueue = [] # clauses to be unified/resolved/evaluated, combined with unification (if possible) or 'and-ing' together
        
        self.runCount = 0
        
        
        
        # EXPLANATION OF VARIABLES AND CONSTANTS:
        # (A state refers to any boolean value)
        # 0. the 'given' state is always a constant
        # 1. All states associated with given cells are constants
        # 2. Safe, Unsafe, Breeze, Stench, Given are all constant if set True
        # and variables if false AND not given
        # 3. There could be a hole, there could be a wompus are both variables 
        # unless set False, at which point they are constants
        # 4. There is a wompus, there is a hole are both variables 
        # unless set True, at which point they are constants
        # 5. raw True and False values are constants
        # 6. anything containing a to-be-simplied function is a variable
        # 7. if there are no more wompuses, then all 'there is a wompus' values are constant
        
        # NOTE: WE SHOULD CONSIDER TRACKING CONSTANTS AND VARIABLES IN THE PROGRAM
        # OR: WE CAN DEFINE METHODS TO DETERMINE "VARIABLE" OR "CONSTANT" FROM THESE
        # RULES FOR ANY VALUE IN ANY CELL (likely easier, actually)
        
        # IF NO MORE VARIABLES CAN BE SIMPLIFIED, RESOLVED, OR UNIFIED THEN WE 
        # ARE DONE. WE EXTRACT WHAT WE CAN FROM COMPLETED LOGIC
        
        # !!! DUE TO THE NATURE OF THE VARIABLES AS THEY RELATE TO THE KNOWLEDGE BASE, TRACKING VARIABLE/CONSTANT
        # IS LIKELY COMPLETELY UNNECESSARY!!!
        
        # OUTPUT METHODS -------------------------------------------------
    def getClausesArray(self):
        return self.clausesArray
    def getBooleanStates(self):
        return self.booleanStates
    def getHolesWompuses(self):
        return self.holesWompuses
    def getKnowledgeBase(self):
        return self.clausesQueue
    def getNumberOperations(self):
        return self.runCount
    def getClausesQueue(self):
        return self.clausesQueue
    def getRunCount(self):
        return self.runCount
        
    
        # END OUTPUT METHODS -------------------------------------------------
    
        # GET-DATA METHODS -------------------------------------------------
    def hasStench(self, cell): # CODE: 'HS' // Constant: if True
        row = cell[0]
        column = cell[1]
        hasStench = False
        if (self.booleanStates[3][row][column] == True):
            hasStench = True
        return hasStench
    
    
    def hasBreeze(self, cell): # CODE: 'HB' // Constant: if True
        row = cell[0]
        column = cell[1]
        hasBreeze = False
        if (self.booleanStates[2][row][column] == True):
            hasBreeze = True
        return hasBreeze
               
    def isGiven(self, cell): # CODE: 'IG' // Constant: Always
        row = cell[0]
        column = cell[1]
        isGiven = False
        if (self.booleanStates[4][row][column] == True):
            isGiven = True
        return isGiven
    
    def isSafe(self, cell): # CODE: 'IS' // Constant: if True
        row = cell[0]
        column = cell[1]
        isSafe = False
        if (self.booleanStates[0][row][column] == True):
            isSafe = True
        return isSafe
    
    def isUnsafe(self, cell): # CODE: 'IU' // Constant: if True
        row = cell[0]
        column = cell[1]
        isUnsafe = False
        if (self.booleanStates[1][row][column] == True):
            isUnsafe = True
        return isUnsafe
    
    def couldWompus(self, cell): # CODE: 'CW' // Constant: if False
        row = cell[0]
        column = cell[1]
        couldWompus = False
        if (self.holesWompuses[1][row][column] == True):
            couldWompus = True
        return couldWompus
        
    def couldHole(self, cell): # CODE: 'CH' // Constant: if False
        row = cell[0]
        column = cell[1]
        couldHole = False
        if (self.holesWompuses[0][row][column] == True):
            couldHole = True
        return couldHole
    
    def isWompus(self, cell): # CODE: 'IW' // Constant: if True
        row = cell[0]
        column = cell[1]
        isWompus = False
        #print(cell)
        if (self.holesWompuses[3][row][column] == True):
            isWompus = True
        return isWompus
        
    def isHole(self, cell): # CODE: 'IH' // Constant: if True
        row = cell[0]
        column = cell[1]
        isHole = False
        if (self.holesWompuses[2][row][column] == True):
            isHole = True
        return isHole
    def atCapacity(self):
        atCapacity = (self.arrows == 0)
        #print("arrows = " + str(self.cellsWithWompus))
        return atCapacity
    
    def cellWithinCapacity(self, cell): # code: 'CWC' // updated by setting 
        # // Constant: if ((not self.couldWompus(cell)) or self.isWompus(cell))
        # eplanation: if isWompus, then cell is not affected by capacity (always returns True)
        # if cell could not be wompus, then capacity has been accounted for (always returns True)
        # if map is at capacity and self.couldWompus(cell) is true, then self.couldWompus(cell) could be set false and alter result
        # if map is not at capacity, result is always true but may change if map becomes at capacity
        atCapacity = self.atCapacity()
        
        if (atCapacity):
            #print("we are at capacity")
            result = ((not self.couldWompus(cell)) or self.isWompus(cell)) 
            return result # true if cell has wompus, otherwise false
        else:
            return True # can still be wompus
        
    def equalsArrowsWompus(self, cell): # CODE: 'EAW' // constant if True or if cell does not need (BECAUSE could not have) wompus
        needWompus = ((self.arrows == self.possibleWompuses) and self.couldWompus(cell))
        return needWompus
        
    
    def isConstant(self, element): # no code likely needed -- called during unification and resolution
        
        if (element == True or element == False): # if it is a constant True or False
            return True
        if type(element) != tuple or len(element) != 2:  # if shape not consistent with graph calls
            return False
        code = element[0]
        cell = element[1]
        
        if code == 'HS':  # Constant if True // ACTUALLY, WE NEVER SET IT (see rules), SO ALWAYS TRUE
            return True
            #return self.hasStench(cell)
        elif code == 'HB':  # Constant if True // ACTUALLY, WE NEVER SET IT (see rules), SO ALWAYS TRUE
            return True
            # return self.hasBreeze(cell)
        elif code == 'IS':  # Constant if True 
            return self.isSafe(cell)
        elif code == 'IU':  # Constant if True
            return self.isUnsafe(cell)
        elif code == 'CW':  # Constant if False (could not)
            return not self.couldWompus(cell)
        elif code == 'CH':  # Constant if False
            return not self.couldHole(cell)
        elif code == 'IW':  # Constant if True
            return self.isWompus(cell)
        elif code == 'IH':  # Constant if True
            return self.isHole(cell)
        elif code == 'IG':  # Always constant
            return True
        elif code == 'CWC':  # conditions explained above
            result = ((not self.couldWompus(cell)) or self.isWompus(cell)) # or (not self.atCapacity())
            return result
        elif code == 'EAW': # constant if True or if cell does not need (could not have)wompus
            return (self.equalsArrows(cell) or not self.couldWompus(cell)) 
        
        return False
    
    def evaluateCellCall(self, element):
        code = element[0]
        cell = element[1]
        if code == 'HS':  
            return self.hasStench(cell)
        elif code == 'HB':  
            return self.hasBreeze(cell)
        elif code == 'IS': 
            return self.isSafe(cell)
        elif code == 'IU': 
            return self.isUnsafe(cell)
        elif code == 'CW': 
            return self.couldWompus(cell)
        elif code == 'CH': 
            return self.couldHole(cell)
        elif code == 'IW': 
            return self.isWompus(cell)
        elif code == 'IH': 
            return self.isHole(cell)
        elif code == 'IG': 
            return self.isGiven(cell)
        elif code == 'CWC': 
            return self.cellWithinCapacity(cell)
        elif code == 'EAW':
            return self.equalsArrows(cell) 
        
        #print(element)
        #print("EVALUATE CELL CALL INVALID")
        return # if invalid, return failure
        
    
    
    
        # END GET-DATA METHODS -------------------------------------------------
    
        # BOOLEAN OPERATOR METHODS -------------------------------------------------
        
        # python defines and, or, and not operators.
        # If all variables (one for not and two for and/or) operated on by an operator
        # are constants, simplify to boolean state
        
        # TUPLES LOOK LIKE THIS: (OPERATOR/FUNCTION, VAR_A, VAR_B) (if var B exists), Result is result of predicate operating on Variable(s)
        
        
    def impliesMethod(self, X, Y): # NO CODE, APPLIED DIRECTLY UPON KNOWLEDGE INIT
        # store the expression: (not x) or y
        implies = ("OR", ("NOT", X), Y)
        return implies
    
    def iffMethod(self, X, Y):
        iffResult = ('AND', self.impliesMethod(X, Y), self.impliesMethod(Y, X))
        return iffResult
    
    def moveCancelNots(self, statementTuple, previousPredicate):
        newStatementTuple = statementTuple
        predicate = statementTuple[0]
        notWasMoved = False
        
        if (previousPredicate == 'NOT'):
            if (predicate == 'AND'):
                new1 = ('NOT', statementTuple[1])
                new2 = ('NOT', statementTuple[2])
                newStatementTuple = ('OR', new1, new2)
                notWasMoved = True
            elif (predicate == 'OR'):
                new1 = ('NOT', statementTuple[1])
                new2 = ('NOT', statementTuple[2])
                newStatementTuple = ('AND', new1, new2)
                notWasMoved = True
            elif (predicate == 'NOT'):
                new1 = statementTuple[1]
                newStatementTuple = new1
                notWasMoved = True
                
                
        newPredicate = newStatementTuple[0]
        finalStatementTuple = ()
        removeNot = False
        
        for element in newStatementTuple:
            nottedElement = ()
            if (type(element) == tuple):
                nottedResults = self.moveCancelNots(element, newPredicate)
                nottedElement = nottedResults[0]
                removeNot = nottedResults[1]
                
            else:
                nottedElement = element
            
            finalStatementTuple += (nottedElement,)
        if removeNot:
            finalStatementTuple = finalStatementTuple[1]
        
        resultsTuple = (finalStatementTuple, notWasMoved)
            
        return resultsTuple
         
        
    
    def andMethod(self, X, Y): # CODE: 'AND' // Constant: if FALSE OR IF X and Y are constants (do not call if both are variables)
        # (if one of X or Y is variable and result is True, treat result as variable)
        #print(str(X) + " AND " + str(Y))
        if (X == False): # expression must result in False (constant)
            #print("False")
            return False
        if (Y == False): # expression must result in False (constant)
            #print("False")
            return False
        #print("True")
        return True # Expression results in True: (if X and Y are constants, treat as constant). If X or Y is variable, treat as variable
    
    def orMethod(self, X, Y): # CODE: 'OR' // Constant: if TRUE OR IF X and Y are constants (do not call if both are variables)
        #print(str(X) + " OR " + str(Y))
        # (if one of X or Y is variable and result is false, treat result as variable)
        if (X == True): # expression must result in True (constant)
            #print("True")
            return True
        if (Y == True): # expression must result in True (constant)
            #print("True")
            return True
        #print("False")
        return False # Expression results in False: (if X and Y are constants, treat as constant). If X or Y is variable, treat as variable
    
    def notMethod(self, X): # CODE: 'NOT' // Constant: X is constant (do not call if X is variable)
        return (not X)
    
    
        # END BOOLEAN OPERATOR METHODS -------------------------------------------------
    
    
        # MAP COMMAND OPERATIONS -------------------------------------------------
    
        # MAYBE ALL UNNCESSARY
    
    def setCell(self, element):
        code = element[0]
        cell = element[1]
        row = cell[0]
        column = cell[1]
        if code == 'HS':  
            self.booleanStates[3][row][column] = True
        elif code == 'HB':  
            self.booleanStates[2][row][column] = True
        elif code == 'IS':
            self.booleanStates[0][row][column] = True
        elif code == 'IU': 
            self.booleanStates[1][row][column] = True
        elif code == 'CW': 
            self.holesWompuses[1][row][column] = False
            self.possibleWompuses = (self.possibleWompuses - 1)
        elif code == 'CH': 
            self.holesWompuses[0][row][column] = False
        elif code == 'IW': 
            self.holesWompuses[3][row][column] = True
            self.arrows = (self.arrows - 1)
            self.possibleWompuses = (self.possibleWompuses - 1) # must also decrease number of required wompuses remaining
            # otherwise, setting cell as wompus when rule is being reinforced (partially) stops the rule from being reinforced.
        elif code == 'IH': 
            self.holesWompuses[2][row][column] = True
        elif code == 'CWC':
            #print(str(element) + "forced set")
            self.holesWompuses[1][row][column] = False
        elif code == 'EAW':
            # THIS IS NEVER SET BECAUSE:
            # - ONLY APPEARS IN TOP OF QUEUE AS PART OF 'OR' STATEMENT, AND IS NOTTED
            # - ALWAYS CONSTANT IF TRUE, NOT TRUE == FALSE, SO RETURN FAILURE INSTEAD OF ATTEMPTING SET
            print("ERROR: SHOULD NEVER ATTEMPT SET ON EAW")
            
        return
        
    
    
    
    
    
        # END MAP COMMAND OPERATIONS -------------------------------------------------
    
    
        # KNOWLEDGE BASE OPERATIONS METHODS -------------------------------------------------
    def initializeKnowledge(self): # create initial tuple containing all of knowledge base
        for row in range(self.rows):
            for column in range(self.columns):
                cell = [row, column]
                #print(cell)
                self.allCellRules(cell)
                
        if (self.test == 0):
            self.clausesQueue += self.cellNotUnsafe(self.query)
        if (self.test == 1):
            self.clausesQueue += self.cellNotSafe(self.query)
            
        CNFIndex = 0
        clausesCount = len(self.clausesQueue)
        for i in self.clausesQueue:
            self.clausesArray.append(str(i)) # add every clause to clauses Queue records string
            #print(i)
            newResult = self.moveCancelNots(i, 'AND') 
            newClause = newResult[0]
            #print(newClause)
            if (CNFIndex != 0 and CNFIndex != clausesCount - 1):
                self.clausesQueue = (self.clausesQueue[:CNFIndex] + [newClause] + self.clausesQueue[CNFIndex + 1:])

            elif (CNFIndex == 0):
                self.clausesQueue = [newClause] + self.clausesQueue[1:]
                
            else:
                self.clausesQueue = self.clausesQueue[:-1] + [newClause]
            
            CNFIndex += 1
        for i in self.clausesQueue:
            self.clausesArray.append(str(i)) # add every clause to clauses Queue records 
        #for i in self.clausesArray:
            #print(i)
        
        return
    
    def allCellRules(self, cell):
        self.clausesQueue += self.noStenchNeighbor(cell)
        self.clausesQueue += self.noBreezeNeighbor(cell)
        self.clausesQueue += self.cellGivenSafe(cell)
        self.clausesQueue += self.safeDefinition(cell)
        self.clausesQueue += self.unsafeDefinition(cell)
        self.clausesQueue += self.wompusHoleExclusive(cell)
        self.clausesQueue += self.couldDefinition(cell)
        self.clausesQueue += self.arrowsCount(cell)
        self.clausesQueue += self.stenchRule(cell)
        self.clausesQueue += self.breezeRule(cell)
        # self.clausesQueue += ...
        # ...
        return
        
    # -3
    def cellNotUnsafe(self, cell): # if this causes a contradiction, then cell must be Unsafe -- do not append to the clausesQueue within 
        # the same knowledge base as cellNotUnsafe
        addKnowledge = [('NOT', ('IU', cell))]
        # addKnowledge = ('NOT', ('IU', cell, True), True)
        return addKnowledge
    
    # -2
    def cellNotSafe(self, cell): # if this causes a contradiction, then cell must be Safe -- do not append to the clausesQueue within 
        # the same knowledge base as cellNotUnsafe
        addKnowledge = [('NOT', ('IS', cell))]
        return addKnowledge
    
    # -1.
    def noStenchNeighbor(self, cell): # if cell is adjacent to a given cell without a stench, then cell could not have wompus
        row = cell[0]
        column = cell[1]
        
        addKnowledge = []
        if (row + 1 < self.rows):
            addKnowledge.append(self.impliesMethod(('AND', ('NOT', ('HS', [row + 1, column])), ('IG', [row + 1, column])), ('NOT', ('CW', cell))))
            
        if (row - 1 >= 0):
            addKnowledge.append(self.impliesMethod(('AND', ('NOT', ('HS', [row - 1, column])), ('IG', [row - 1, column])), ('NOT', ('CW', cell))))
                
        if (column + 1 < self.columns):
            addKnowledge.append(self.impliesMethod(('AND', ('NOT', ('HS', [row, column + 1])), ('IG', [row, column + 1])), ('NOT', ('CW', cell))))
                
        if (column - 1 >= 0):
            addKnowledge.append(self.impliesMethod(('AND', ('NOT', ('HS', [row, column - 1])), ('IG', [row, column - 1])), ('NOT', ('CW', cell))))
        
        return addKnowledge
    # 0.
    def noBreezeNeighbor(self, cell): # if cell is adjacent to a given cell without a breeze, then cell could not have hole
        row = cell[0]
        column = cell[1]
        
        addKnowledge = []
        if (row + 1 < self.rows):
            addKnowledge.append(self.impliesMethod(('AND', ('NOT', ('HB', [row + 1, column])), ('IG', [row + 1, column])), ('NOT', ('CH', cell))))
            
        if (row - 1 >= 0):
            addKnowledge.append(self.impliesMethod(('AND', ('NOT', ('HB', [row - 1, column])), ('IG', [row - 1, column])), ('NOT', ('CH', cell))))
                
        if (column + 1 < self.columns):
            addKnowledge.append(self.impliesMethod(('AND', ('NOT', ('HB', [row, column + 1])), ('IG', [row, column + 1])), ('NOT', ('CH', cell))))
                
        if (column - 1 >= 0):
            addKnowledge.append(self.impliesMethod(('AND', ('NOT', ('HB', [row, column - 1])), ('IG', [row, column - 1])), ('NOT', ('CH', cell))))     
        
        return addKnowledge
        
    # 1. If cell is given, then cell is safe
    # 2. If cell is given, then cell is not unsafe
    def cellGivenSafe(self, cell):
        addKnowledge = []
        cellGivenSafe = self.impliesMethod(('IG', cell), ('IS', cell))
        cellGivenNotUnsafe = self.impliesMethod(('IG', cell), ('NOT', ('IU', cell)))
        addKnowledge.append(cellGivenSafe)
        addKnowledge.append(cellGivenNotUnsafe)
        return addKnowledge
    
    # 3. cell is safe IFF (cell could not have hole AND cell could not have wompus)
    def safeDefinition(self, cell):
        addKnowledge = []
        safetyDef = self.iffMethod(('IS', cell), ('AND', ('NOT', ('CH', cell)), ('NOT', ('CW', cell))))
        addKnowledge.append(safetyDef)
        return addKnowledge
    # 4. cell is unsafe IFF (cell has hole OR cell has wompus)
    def unsafeDefinition(self, cell):
        addKnowledge = []
        unsafetyDef = self.iffMethod(('IU', cell), ('OR', ('IH', cell), ('IW', cell)))
        addKnowledge.append(unsafetyDef)
        return addKnowledge
    # 5. if cell has wompus, cell could not have hole
    # 6. if cell has hole, cell could not have wompus
    def wompusHoleExclusive(self, cell):
        addKnowledge = []
        wompusNoHole = self.impliesMethod(('IW', cell), ('NOT', ('CH', cell)))
        holeNoWompus = self.impliesMethod(('IH', cell), ('NOT', ('CW', cell)))
        addKnowledge.append(wompusNoHole)
        addKnowledge.append(holeNoWompus)
        return addKnowledge
    
    # 7. if cell could not have wompus, cell does not have wompus
    # 8. if cell could not have hole, cell does not have hole
    def couldDefinition(self, cell):
        addKnowledge = []
        wompusNoHole = self.impliesMethod(('NOT', ('CW', cell)), ('NOT', ('IW', cell)))
        holeNoWompus = self.impliesMethod(('NOT', ('CH', cell)), ('NOT', ('IH', cell)))
        addKnowledge.append(wompusNoHole)
        addKnowledge.append(holeNoWompus)
        return addKnowledge
    
    # 9. if number of cells with wompuses is equal to the number of arrows, all remaining cells could not have a wompus
    # USEFUL TO US: ALL CELLS MUST BE WITHIN CAPACITY
    def arrowsCount(self, cell):
        addKnowledge = []
        arrowCountRule = ('CWC', cell) # this must be true--or made true--for all cells
        addKnowledge.append(arrowCountRule)
        return addKnowledge
    
    # 10. if cell has stench, then at least one adjacent cell has wompus:
    # (neighbor1wompus OR neighbor2wompus OR neighbor3wompus OR neighbor4wompus)
    def stenchRule(self, cell):
        row = cell[0]
        column = cell[1]
        
        addKnowledge = []
        addTuple = None
        if (row + 1 < self.rows):
            alteredTuple = None
            if addTuple == None:
                alteredTuple = ('IW', [row + 1, column])
            else:
                alteredTuple = ('OR', addTuple, ('IW', [row + 1, column]))
            addTuple = alteredTuple
            
        if (row - 1 >= 0):
            alteredTuple = None
            if addTuple == None:
                alteredTuple = ('IW', [row - 1, column])
            else:
                alteredTuple = ('OR', addTuple, ('IW', [row - 1, column]))
            addTuple = alteredTuple
                
        if (column + 1 < self.columns):
            alteredTuple = None
            if addTuple == None:
                alteredTuple = ('IW', [row, column + 1])
            else:
                alteredTuple = ('OR', addTuple, ('IW', [row, column + 1]))
            addTuple = alteredTuple
                
        if (column - 1 >= 0):
            alteredTuple = None
            if addTuple == None:
                alteredTuple = ('IW', [row, column - 1])
            else:
                alteredTuple = ('OR', addTuple, ('IW', [row, column - 1]))
            addTuple = alteredTuple
            
        if addTuple != None:
            #addKnowledge.append(self.iffMethod(('HS', cell), addTuple))
            addKnowledge.append(self.impliesMethod(('HS', cell), addTuple))
            
        # print(addKnowledge[0])
        return addKnowledge
    
    # 11. if cell has breeze, then at least one adjacent cell has hole
    def breezeRule(self, cell):
        row = cell[0]
        column = cell[1]
        
        addKnowledge = []
        addTuple = None
        if (row + 1 < self.rows):
            alteredTuple = None
            if addTuple == None:
                alteredTuple = ('IH', [row + 1, column])
            else:
                alteredTuple = ('OR', addTuple, ('IH', [row + 1, column]))
            addTuple = alteredTuple
            
        if (row - 1 >= 0):
            alteredTuple = None
            if addTuple == None:
                alteredTuple = ('IH', [row - 1, column])
            else:
                alteredTuple = ('OR', addTuple, ('IH', [row - 1, column]))
            addTuple = alteredTuple
                
        if (column + 1 < self.columns):
            alteredTuple = None
            if addTuple == None:
                alteredTuple = ('IH', [row, column + 1])
            else:
                alteredTuple = ('OR', addTuple, ('IH', [row, column + 1]))
            addTuple = alteredTuple
                
        if (column - 1 >= 0):
            alteredTuple = None
            if addTuple == None:
                alteredTuple = ('IH', [row, column - 1])
            else:
                alteredTuple = ('OR', addTuple, ('IH', [row, column - 1]))
            addTuple = alteredTuple
            
        if addTuple != None:
            # addKnowledge.append(self.iffMethod(('HB', cell), addTuple))
            addKnowledge.append(self.impliesMethod(('HB', cell), addTuple))
            
        # print(addKnowledge[0])
        return addKnowledge
    # 12. for all cells, if (Equals Arrows) AND (cell could have wompus) THEN (cell is wompus)
    def ArrowsRule(self, cell):
        addKnowledge = []
        #arrowCountRule = self.impliesMethod(('AND', ('EA', cell), ('CW', cell)), ('IW', cell)) 
        arrowCountRule = self.impliesMethod(('EAW', cell), ('IW', cell)) 
        # this must be true--or made true--for all cells
        addKnowledge.append(arrowCountRule)
        return addKnowledge
    
    
    # (neighbor1hole OR neighbor2hole OR neighbor3hole OR neighbor4hole)
    
    # END KNOWLEDGE BASE OPERATIONS METHODS -------------------------------------------------
    
    
    # FUNCTION EVALUATION METHODS ------------------------------------------------- 
    
    
    
    
    
    # END FUNCTION EVALUATION METHODS -------------------------------------------------
    
    
    # UNIFICATION METHODS -------------------------------------------------

    def unifyForcedValues(self): # works because all 2-tuples are 
        # moved to the bottom of tree (not-and, not-or), or removed (not-not)
        # or were at bottom of tree to start (map-cells)

        # TARGET VALUE ALWAYS SET TRUE FOR INITIAL CALL!

        performedUnify = False
        replacements = {}

        for clause in self.clausesQueue:
            targetValue = True # from top of tree, always seek True values
            clauseCat = len(clause) # get type (should never be raw boolean)
            currentClause = clause
            if(clauseCat == 2):
                self.runCount += 1 # number of times this is run -- metric for program scaling
                #print(currentClause)
                resultingValue = False
                clausePredicate = clause[0]
                if (clausePredicate == 'NOT'): # will only ever be one 'NOT' at back-end of logic tree
                    #print(clause)
                    targetValue = False # target value becomes False
                    innerClause = clause[1] # grab inner variable/constant
                    currentClause = innerClause
                    if (type(innerClause) != tuple):
                        print("Error: Appended unreadable atom")
                        print("atomApendage: " + str(innerClause))
                        print("original: " + str(clause))

                # VALUES NEVER CONSTANT--THIS PERFORMED APART FROM RESOLUTION
                #print(currentClause)
                resultingValue = self.evaluateCellCall(currentClause)

                replacements.update({str(currentClause) : targetValue})
                performedUnify = True

            else:
                pass # if not correct type of expression, no replacement is found

        self.clausesQueue = list(self.Unify(replacements, self.clausesQueue))

        return performedUnify
    
    def Unify(self, theta, currentQueue):
        newClausesQueue = ()
        for clause in currentQueue:
            if str(clause) in theta: # base case: replacement available, do not recurse
                newClausesQueue = newClausesQueue + (theta[str(clause)],)
            elif (type(clause) == tuple): # recursive case: no replacement available, search lower tree
                newClausesQueue = newClausesQueue + (self.Unify(theta, clause),)
            else:
                newClausesQueue = newClausesQueue + (clause,) # Base case: tree not expandable, preserve datastructure
                
        return newClausesQueue
    # END UNIFICATION METHODS -------------------------------------------------
    
    
    
    # RESOLUTION METHODS -------------------------------------------------
    def setForcedValues(self): # works because all 2-tuples are 
        # moved to the bottom of tree (not-and, not-or), or removed (not-not)
        # or were at bottom of tree to start (map-cells)
        
        # TARGET VALUE ALWAYS SET TRUE FOR INITIAL CALL!
        
        performedResolve = False
        newClausesQueue = []
        #print("NEW ITERATION")
        
        for clause in self.clausesQueue:
            targetValue = True # from top of tree, always seek True values
            clauseCat = len(clause) # get type (should never be raw boolean)
            currentClause = clause
            if(clauseCat == 2):
                self.runCount += 1 # number of times this is run -- metric for program scaling
                #print(currentClause)
                resultingValue = False
                clausePredicate = clause[0]
                if (clausePredicate == 'NOT'): # will only ever be one 'NOT' at back-end of logic tree
                    #print(clause)
                    targetValue = False # target value becomes False
                    innerClause = clause[1] # grab inner variable/constant
                    currentClause = innerClause
                    if (type(innerClause) != tuple):
                        print("Error: Appended unreadable atom")
                        print("atomApendage: " + str(innerClause))
                        print("original: " + str(clause))
                
                isConstantValue = self.isConstant(currentClause)
                
                if(isConstantValue): # if constant
                    resultingValue = self.evaluateCellCall(currentClause) # check consistency
                    # do not re-append to queue, value is set
                    if (targetValue == resultingValue): # if already consistent
                        pass # do nothing, remove from queue
                    
                    else: # if constant causes contradiction, return failure
                        # print("failure in Resolution")
                        return -1
                    
                else: # if variable
                    #print(currentClause)
                    resultingValue = self.evaluateCellCall(currentClause)
                    
                    if (targetValue == resultingValue): # if already consistent
                        newClausesQueue.append(clause) # do nothing
                        # (could still cause contradiction later)
                    else: # if not consistent
                        #print(currentClause)
                        self.setCell(currentClause) # value becomes constant
                        # Value has been updates, maximum impact of clause achieved, remove
                        # (could still cause contradiction later)
                    
            else:
                newClausesQueue.append(clause) # if different kind of tuple, no forced value exists
                
        self.clausesQueue = newClausesQueue
        return performedResolve
    
        
        
    
    def resolveStatements(self):
        performedResolve = False
        newClausesQueue = []
        for clause in self.clausesQueue:
            #print(clause)
            newClause = self.resolvePredicate(clause)
            
            if (newClause == True):
                # pass # if top-level clause resolved to True, remove from array
                # print(newClause)
                performedResolve = True
            elif (newClause == False):
                # maybe print error message
                # print("failure in Unification")
                return -1 # return failure if top-level clause becomes false,
            else:
                if (type(newClause) != tuple):
                    print("Error: Appending unreadable atom")
                    print("atomApendage: " + str(newClause))
                    print("original: " + str(clause))
                
                newClausesQueue += [newClause]
                if (newClause != clause):
                    performedResolve = True
                
        self.clausesQueue = newClausesQueue
        
        # NOW CHECK FOR FORCED VALUE-SETS!!!
        forcedValuesSet = self.setForcedValues()
        
        if (forcedValuesSet == -1):
            return -1 # return failure if top-level clause is forced false
        
        
        if (forcedValuesSet): # If forced values were set, re-call resolveStatements to ensure completed resolution
            self.resolveStatements() # no need to check whether inner resolves were performed, if we're here, we know changes occurred
            performedResolve = True # we know this happened if setForcedValues occurred
        return performedResolve # flag for code to determine whether resolution changed anything
    
    def resolvePredicate(self, statementTuple): # start with this for all predicates, then unify. 
        
        newStatementTuple = ()
        
        if (type(statementTuple) == bool):
            return statementTuple
        
        for element in statementTuple:
            resolvedElement = ()
            if (type(element) == tuple):
                resolvedElement = self.resolvePredicate(element)
            else:
                resolvedElement = element
            
            newStatementTuple += (resolvedElement,)
        
        for element in newStatementTuple:
            if (type(element) == tuple and newStatementTuple[0] != 'AND' and newStatementTuple[0] != 'OR'):
                return newStatementTuple # if, following recursion, tuple still contains unresolved tuples, then return without 
                # attempting further resolution
        result = self.evaluateFunction(newStatementTuple)
        
        return result
            
        
        
        
    
    def evaluateFunction(self, statementTuple): # NOTE: FAILURE SIMPLY RESULTS IN A FALSE VALUE INSIDE resolveFunction METHOD
        predicate = statementTuple[0]
        self.runCount += 1 # number of times this is run -- metric for program scaling
        tupleLength = len(statementTuple)
        
        if (predicate == 'NOT'):
            toEvaluate = statementTuple[1]
            
            typeVar = type(toEvaluate)
            
            if (typeVar == bool): # if value is constant, return method Value
                result = self.notMethod(toEvaluate)
                if (result):
                    return True # if the result is correct, return 1
                return False # if the result is incorrect, return -1 (False)
            else: # if value is not constant, try both True and False values (basically, always remains as a variable here, but more code
                # is explanatory
                return statementTuple
                
            
            
        elif (tupleLength == 2):
            
            result = self.evaluateCellCall(statementTuple) # variable if current value of couldWompus in cell is True
            constant = self.isConstant(statementTuple)
            
            if (not constant): # if value is variable
                return statementTuple # if the result is a variable and true, return 0 to keep as variable
            elif (result == True): 
                return True # if the result is a constant and true return true
            elif (result == False):
                return False # if result is constant (false), return false
            return 
        
        elif (predicate == 'AND'): # note: we do not have to deal with evaluating cell-calls because 
            #that is handled at a lower-level of recursion
            value1 = statementTuple[1]
            value2 = statementTuple[2]
            #print(statementTuple)
            
            type1 = type(value1)
            type2 = type(value2)
            
            totalConstants = 0
            if (type1 == bool):
                totalConstants += 1
            if (type2 == bool):
                totalConstants += 1 
                
            if (totalConstants == 0):
                return statementTuple
            elif (totalConstants == 1):
                #print(statementTuple)
                attemptResult = self.andMethod(value1, value2)
                if (attemptResult == True):
                    if (type1 == bool):
                        #print(value2)
                        return value2 # result no longer dependent upon value1
                    if (type2 == bool):
                        #print(value1)
                        return value1 # result no longer dependent upon value2
                #print(False)
                return False
            elif (totalConstants == 2):
                result = self.andMethod(value1, value2)
                if (result == True):
                    return True
                return False
            return statementTuple
            
        elif (predicate == 'OR'): # note: we do not have to deal with evaluating cell-calls because 
            #that is handled at a lower-level of recursion
            value1 = statementTuple[1]
            value2 = statementTuple[2]
            #print(statementTuple)
            
            type1 = type(value1)
            type2 = type(value2)
            
            totalConstants = 0
            if (type1 == bool):
                totalConstants += 1
            if (type2 == bool):
                totalConstants += 1 
                
            if (totalConstants == 0):
                return statementTuple
            elif (totalConstants == 1):
                #print(statementTuple)
                attemptResult = self.orMethod(value1, value2)
                if (attemptResult == False):
                    if (type1 == bool):
                        #print(value2)
                        return value2 # result no longer dependent upon value1
                    if (type2 == bool):
                        #print(value1)
                        return value1 # result no longer dependent upon value2
                    return statementTuple
                #print(True)
                return True
            elif (totalConstants == 2):
                result = self.orMethod(value1, value2)
                if (result == True):
                    return True
                return False
            return statementTuple
            
        else:
            # print error message maybe
            print("ERROR: INVALID TUPLE")
            print(statementTuple)
            print("-----")
            return statementTuple
            
            
        # CODE CYCLE:
        
        # 0. If there is variable that cannot be turned into a constant, do not evaluate the function (return 0)
        # 1. Evaluate Function
            # a. Select function based upon first element of statement tuple
            # b. Run function with correct number of elements, and the target value
            # c. Expect it to return True (result is step 2), otherwise result is step 3
        # 2. If function holds, update map accordingly (only needed if variable was forced to become a constant)
        # 3. if function does not hold, return -1. This tuple's value is now resolved to False
        # 4. return 1 -- Our tuple will be resolved to True
        # NOTE: DUE TO THE 3 RETURN CASES (FAILURE, contains_var, SUCCESS), we will return an integer -1, 0, or 1 instead of a boolean
    
    
    
    # END RESOLUTION METHODS -------------------------------------------------
    
    
        
        
    
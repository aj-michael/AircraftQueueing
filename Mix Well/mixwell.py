from coopr.pyomo import *
from coopr.opt import *

M = AbstractModel()
M.name = 'Mix Well'

# Parameters
M.NumBoardMembers = Param(within=NonNegativeIntegers)
M.NumSessions = Param(within=NonNegativeIntegers)
M.BoardMembers = RangeSet(0,M.NumBoardMembers-1)
M.Sessions = RangeSet(0,M.NumSessions-1)
M.Groups = Param(M.Sessions,within=NonNegativeIntegers)

# Variables


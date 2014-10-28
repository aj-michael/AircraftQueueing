from coopr.pyomo import *
from coopr.opt import *

M = AbstractModel()
M.name = 'Mix Well'

# Parameters
M.NumBoardMembers = Param(within=NonNegativeIntegers)
M.NumSessions = Param(within=NonNegativeIntegers)
M.MaxGroupsPerSession = Param(within=NonNegativeIntegers)
M.BoardMember = RangeSet(0,M.NumBoardMembers-1)
M.Session = RangeSet(0,M.NumSessions-1)
M.Group = RangeSet(0,M.MaxGroupsPerSession-1)
M.MaxAttendance = Param(M.Session,M.Group,within=NonNegativeIntegers)


# Variables
M.tt = Var(M.BoardMember,M.BoardMember,within=NonNegativeIntegers)
M.at = Var(M.BoardMember,M.Session,M.Group,within=Binary)
M.meet = Var(M.BoardMember,M.BoardMember,M.Session,M.Group,within=Binary)

M.avgMeetings = Var(within=NonNegativeReals)

M.fpos = Var(M.BoardMember,M.BoardMember,M.Session,M.Group,within=NonNegativeIntegers)
M.fneg = Var(M.BoardMember,M.BoardMember,M.Session,M.Group,within=NonNegativeIntegers)
M.zpos = Var(M.BoardMember,M.BoardMember,M.Session,M.Group,within=Binary)
M.zneg = Var(M.BoardMember,M.BoardMember,M.Session,M.Group,within=Binary)

M.diff = Var(M.BoardMember,M.BoardMember,within=NonNegativeIntegers)
M.gpos = Var(M.BoardMember,M.BoardMember,within=NonNegativeIntegers)
M.gneg = Var(M.BoardMember,M.BoardMember,within=NonNegativeIntegers)
M.wpos = Var(M.BoardMember,M.BoardMember,within=Binary)
M.wneg = Var(M.BoardMember,M.BoardMember,within=Binary)

M.mymax = Var(within=NonNegativeReals)


# Objective

def CalcTotalDiff(M):
    return sum(M.diff[m,n] for m in M.BoardMember for n in M.BoardMember if m != n)
#M.TotalDiff = Objective(rule=CalcTotalDiff,sense=minimize)

def CalcTotalMeetings(M):
    return M.mymax
M.TotalMeetings = Objective(rule=CalcTotalMeetings,sense=minimize)

def EnsureMeetsFirstObjective(M):
    return sum(M.diff[m,n] for m in M.BoardMember for n in M.BoardMember if m != n) == 0
M.MeetsFirstObjective = Constraint(rule=EnsureMeetsFirstObjective)

def EnsureMyMaxIsGood(M,m,n):
    return M.mymax >= M.tt[m,n] if m != n else Constraint.Skip
M.MyMaxIsGood = Constraint(M.BoardMember,M.BoardMember,rule=EnsureMyMaxIsGood)

# Constraints
def EnsureNoClones(M,m,s):
    return sum(M.at[m,s,g] for g in M.Group) == 1
M.NoClones = Constraint(M.BoardMember,M.Session,rule=EnsureNoClones)

def EnsureTimesTogether(M,m,n):
    return M.tt[m,n] == sum(M.meet[m,n,s,g] for s in M.Session for g in M.Group) if m <> n else Constraint.Skip
M.TimesTogether = Constraint(M.BoardMember,M.BoardMember,rule=EnsureTimesTogether)

def EnsureNonExistant(M,s,g):
    return sum(M.at[m,s,g] for m in M.BoardMember) <= M.MaxAttendance[s,g]
M.NonExistant = Constraint(M.Session,M.Group,rule=EnsureNonExistant)

def EnsureAttendsSomething(M,m):
    return sum(M.at[m,s,g] for s in M.Session for g in M.Group) >= 1
M.AttendsSomething = Constraint(M.BoardMember,rule=EnsureAttendsSomething)

def EnsurePart1(M,m,n,s,g):
    return M.at[m,s,g] + M.at[n,s,g] - 1 == M.fpos[m,n,s,g] - M.fneg[m,n,s,g] if m <> n else Constraint.Skip
M.Part1 = Constraint(M.BoardMember,M.BoardMember,M.Session,M.Group,rule=EnsurePart1)

def EnsurePart2(M,m,n,s,g):
    return M.fpos[m,n,s,g] <= 2*M.zpos[m,n,s,g]
M.Part2 = Constraint(M.BoardMember,M.BoardMember,M.Session,M.Group,rule=EnsurePart2)

def EnsurePart3(M,m,n,s,g):
    return M.fneg[m,n,s,g] <= 2*M.zneg[m,n,s,g]
M.Part3 = Constraint(M.BoardMember,M.BoardMember,M.Session,M.Group,rule=EnsurePart3)

def EnsurePart4(M,m,n,s,g):
    return M.zpos[m,n,s,g] + M.zneg[m,n,s,g] == 1
M.Part4 = Constraint(M.BoardMember,M.BoardMember,M.Session,M.Group,rule=EnsurePart4)

def EnsurePart5(M,m,n,s,g):
    return M.meet[m,n,s,g] == M.zpos[m,n,s,g]
M.Part5 = Constraint(M.BoardMember,M.BoardMember,M.Session,M.Group,rule=EnsurePart5)

def EnsurePartA(M,m,n):
    return M.diff[m,n] == M.gpos[m,n] + M.gneg[m,n] if m != n else Constraint.Skip
M.PartA = Constraint(M.BoardMember,M.BoardMember,rule=EnsurePartA)

def EnsurePartB(M,m,n):
    return M.tt[m,n] - M.avgMeetings == M.gpos[m,n] - M.gneg[m,n]
M.PartB = Constraint(M.BoardMember,M.BoardMember,rule=EnsurePartB)

def EnsurePartC(M,m,n):
    return M.wpos[m,n] + M.wneg[m,n] == 1
M.PartC = Constraint(M.BoardMember,M.BoardMember,rule=EnsurePartC)

def EnsurePartD(M,m,n):
    return M.gpos[m,n] <= 7*M.wpos[m,n]
M.PartD = Constraint(M.BoardMember,M.BoardMember,rule=EnsurePartD)

def EnsurePartE(M,m,n):
    return M.gneg[m,n] <= 7*M.wneg[m,n]
M.PartE = Constraint(M.BoardMember,M.BoardMember,rule=EnsurePartE)

def EnsureAvgWorks(M):
    return M.NumBoardMembers * (M.NumBoardMembers - 1) * M.avgMeetings == sum(M.tt[m,n] for m in M.BoardMember for n in M.BoardMember if m != n)
M.AvgWorks = Constraint(rule=EnsureAvgWorks)



instance = M.create('data.dat')
opt = SolverFactory('gurobi')
soln = opt.solve(instance)
soln.write()
instance.load(soln)
display(instance)

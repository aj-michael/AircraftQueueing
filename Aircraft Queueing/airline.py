import sys
from coopr.pyomo import *
from coopr.opt import *

M = AbstractModel()
M.name = "Aircraft Queueing"


# Parameters
M.NumFlights = Param(within=NonNegativeIntegers)
M.NumIncFlights = Param(within=NonNegativeIntegers)
M.Flight = RangeSet(0,M.NumFlights-1)
M.IncFlight = RangeSet(0,M.NumIncFlights-1)

M.pob = Param(M.Flight, within=NonNegativeIntegers)
M.ppf = Param(within=NonNegativeIntegers)
M.Person = RangeSet(0,M.ppf-1)
M.cft = Param(M.Flight, M.Person, within=NonNegativeIntegers)

M.spt = Param(M.Flight, within=NonNegativeIntegers)
M.sat = Param(M.Flight, within=NonNegativeIntegers)
M.cap = Param(M.Flight, within=NonNegativeIntegers)
M.ati = Param(M.IncFlight, within=NonNegativeIntegers)

M.rws = Param(within=NonNegativeIntegers)
M.tbt = Param(within=NonNegativeIntegers)
M.mpt = Param(within=NonNegativeIntegers)
M.mpw = Param(within=NonNegativeIntegers)
M.mtt = Param(within=NonNegativeIntegers)

# Variables
M.apt = Var(M.Flight, within=NonNegativeIntegers)
M.tot = Var(M.Flight, within=NonNegativeIntegers)
M.aat = Var(M.Flight, within=NonNegativeIntegers)

M.depDiffPos = Var(M.Flight,M.Flight,within=NonNegativeIntegers)
M.depDiffNeg = Var(M.Flight,M.Flight,within=NonNegativeIntegers)
M.depDiffZ1  = Var(M.Flight,M.Flight,within=NonNegativeIntegers)
M.depDiffZ2  = Var(M.Flight,M.Flight,within=NonNegativeIntegers)

M.Miss = Var(M.Flight,M.Person,within=NonNegativeIntegers)
M.Make = Var(M.Flight,M.Person,within=NonNegativeIntegers)

M.MissPos = Var(M.Flight,M.Person,within=NonNegativeIntegers)
M.MissNeg = Var(M.Flight,M.Person,within=NonNegativeIntegers)


M.ariDiffPos = Var(M.Flight,M.IncFlight,within=NonNegativeIntegers)
M.ariDiffNeg = Var(M.Flight,M.IncFlight,within=NonNegativeIntegers)
M.ariDiffZ1  = Var(M.Flight,M.IncFlight,within=NonNegativeIntegers)
M.ariDiffZ2  = Var(M.Flight,M.IncFlight,within=NonNegativeIntegers)


# Objective
def CalcAirlineHappiness(M):
    return -1*sum(M.Miss[i,j] for i in M.Flight for j in M.Person)
M.AirlineHappiness = Objective(rule=CalcAirlineHappiness, sense=maximize)

# Constraints
def EnsureSetFlightDuration(M,i):
    #return M.tot[i] - (M.spt[i]+M.mpt) == M.aat[i] - M.sat[i]
    return M.aat[i] - M.tot[i] == M.sat[i] - (M.spt[i]+M.mpt)
M.SetFlightDuration = Constraint(M.Flight,rule=EnsureSetFlightDuration)

def EnsureNotOverbooked(M,i):
    return M.pob[i] <= M.cap[i]
#M.NotOverbooked = Constraint(M.Flight,rule=EnsureNotOverbooked);

def EnsureSequentialDeparture(M,i):
    return M.tot[i] >= M.apt[i] + M.mpt
M.SequentialDeparture = Constraint(M.Flight,rule=EnsureSequentialDeparture)

def EnsureSequentialPushback(M,i):
    return M.apt[i] >= M.spt[i]
M.SequentualPushback = Constraint(M.Flight,rule=EnsureSequentialPushback)

def EnsureDepartureSeparation(M,i,j):
    return M.depDiffPos[i,j] + M.depDiffNeg[i,j] >= M.tbt if i <> j else Constraint.Skip
M.DepartureSeparation = Constraint(M.Flight,M.Flight,rule=EnsureDepartureSeparation)


def EnsureDepDiffP1(M,i,j):
    return M.tot[i] - M.tot[j] == M.depDiffPos[i,j] - M.depDiffNeg[i,j] if i <> j else Constraint.Skip
M.DepDiffP1 = Constraint(M.Flight,M.Flight,rule=EnsureDepDiffP1)

def EnsureDepDiffP2(M,i,j):
    return M.depDiffPos[i,j] <= 1440*M.depDiffZ1[i,j]
M.DepDiffP2 = Constraint(M.Flight,M.Flight,rule=EnsureDepDiffP2)

def EnsureDepDiffP3(M,i,j):
    return M.depDiffNeg[i,j] <= 1440*M.depDiffZ2[i,j]
M.DepDiffP3 = Constraint(M.Flight,M.Flight,rule=EnsureDepDiffP3)

def EnsureDepDiffP4(M,i,j):
    return M.depDiffZ1[i,j] + M.depDiffZ2[i,j] == 1 if i <> j else Constraint.Skip
M.DepDiffP4 = Constraint(M.Flight,M.Flight,rule=EnsureDepDiffP4)


def EnsureArrivalSeparation(M,i,k):
    return M.ariDiffPos[i,k] + M.ariDiffNeg[i,k] >= M.tbt
M.ArrivalSeparation = Constraint(M.Flight,M.IncFlight,rule=EnsureArrivalSeparation)

def EnsureAriDiffP1(M,i,k):
    return M.tot[i] - M.ati[k] == M.ariDiffPos[i,k] - M.ariDiffNeg[i,k]
M.AriDiffP1 = Constraint(M.Flight,M.IncFlight,rule=EnsureAriDiffP1)

def EnsureAriDiffP2(M,i,k):
    return M.ariDiffPos[i,k] <= 1440*M.ariDiffZ1[i,k]
M.AriDiffP2 = Constraint(M.Flight,M.IncFlight,rule=EnsureAriDiffP2)

def EnsureAriDiffP3(M,i,k):
    return M.ariDiffNeg[i,k] <= 1440*M.ariDiffZ2[i,k]
M.AriDiffP3 = Constraint(M.Flight,M.IncFlight,rule=EnsureAriDiffP3)

def EnsureAriDiffP4(M,i,k):
    return M.ariDiffZ1[i,k] + M.ariDiffZ2[i,k] == 1
M.AriDiffP4 = Constraint(M.Flight,M.IncFlight,rule=EnsureAriDiffP4)



def EnsureMissPart1(M,i,j):
    return M.Miss[i,j] + M.Make[i,j] == 1
M.MissPart1 = Constraint(M.Flight,M.Person,rule=EnsureMissPart1)

def EnsureMissPart2(M,i,j):
    return M.aat[i] + M.mtt - M.cft[i,j] == M.MissPos[i,j] - M.MissNeg[i,j]
M.MissPart2 = Constraint(M.Flight,M.Person,rule=EnsureMissPart2)

def EnsureMissPart3(M,i,j):
    return M.MissPos[i,j] <= 9999*M.Miss[i,j]
M.MissPart3 = Constraint(M.Flight,M.Person,rule=EnsureMissPart3)

def EnsureMissPart4(M,i,j):
    return M.MissNeg[i,j] <= 9999*M.Make[i,j]
M.MissPart4 = Constraint(M.Flight,M.Person,rule=EnsureMissPart4)


instance = M.create("data.dat")
Opt = SolverFactory("glpk")
Soln = Opt.solve(instance)
Soln.write()
instance.load(Soln)
display(instance)

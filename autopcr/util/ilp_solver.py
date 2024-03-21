from typing import List, Tuple
from pulp import PULP_CBC_CMD, LpProblem, LpMinimize, LpStatus, LpVariable, lpSum, LpStatusOptimal, LpInteger, value

def ilp_solver(ub: List[int], target: int, limit: int, effect: List[int]) -> Tuple[bool, List[int]]:
    prob = LpProblem(name='solve', sense=LpMinimize)
    assert(len(ub) == len(effect))

    n = len(ub)

    x = [LpVariable(str(effect[i]), lowBound=0, upBound=ub[i], cat=LpInteger) for i in range(n)]

    prob += lpSum([effect[i]*x[i] for i in range(n)]), "cost"

    prob += lpSum([effect[i]*x[i] for i in range(n)]) >= target, "target_value"
    if limit != -1:
        prob += lpSum([effect[i]*x[i] for i in range(n)]) <= limit - 1, "limit_value"

    prob.solve(PULP_CBC_CMD(msg=False))
    result = {v.name: int(v.varValue) for v in prob.variables()}
    ret = [result[str(effect[i])] for i in range(n)]
    print(LpStatus[prob.status])
    print(ret)
    print(effect)
    print(target, limit, value(prob.objective))
    return prob.status == LpStatusOptimal, ret

if __name__ == '__main__':
    ilp_solver([3, 1, 1], 100, 1000, [10, 20, 30])

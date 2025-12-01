from typing import Dict, List, Tuple
from pulp import PULP_CBC_CMD, LpProblem, LpMinimize, LpStatus, LpVariable, lpSum, LpStatusOptimal, LpInteger
import networkx as nx

def ilp_solver(ub: List[int], target: int, limit: int, effect: List[int]) -> Tuple[bool, List[int]]:
    '''
    物品数量使用确定，使效果值尽可能小，处于给定上下界内
    :param ub: 物品数量上限
    :param target: 效果值下界
    :param limit: 效果值上界
    :param effect: 物品效果值
    :return: 是否有解，物品数量
    '''
    prob = LpProblem(name='solve', sense=LpMinimize)
    assert len(ub) == len(effect)

    n = len(ub)

    x = [LpVariable(str(effect[i]), lowBound=0, upBound=ub[i], cat=LpInteger) for i in range(n)]

    prob += lpSum([effect[i]*x[i] for i in range(n)]), "cost"

    prob += lpSum([effect[i]*x[i] for i in range(n)]) >= target, "target_value"
    if limit != -1:
        prob += lpSum([effect[i]*x[i] for i in range(n)]) <= limit - 1, "limit_value"

    prob.solve(PULP_CBC_CMD(msg=False))
    result = {v.name: int(v.varValue) for v in prob.variables()}
    ret = [result[str(effect[i])] for i in range(n)]
    return prob.status == LpStatusOptimal, ret

def dispatch_solver(start: List[int], candidate: List[int], lb: List[int], choose: int) -> Tuple[bool, List[int]]:
    '''
    数字分配，使得不同组的数字和尽可能平均
    :param start: 组的初始数字和
    :param candidate: 候选数字
    :param lb: 每组数字和的下界
    :param choose: 每组选择的数字个数
    :return: 是否有解，数字分配结果
    '''
    def vname(i, j):
        return f"x_{i}_{j}"
    n = len(start)
    m = len(candidate)
    assert n * choose == m, "候选数需等于安排数"
    assert len(start) == len(lb), "组数需等于组下界数"
    prob = LpProblem(name='dispatch', sense=LpMinimize)

    x = [[LpVariable(vname(j, i), lowBound=0, upBound=1, cat=LpInteger) for i in range(n)] for j in range(m)]
    min = LpVariable("min")
    max = LpVariable("max")

    psum = [lpSum([x[i][j] * candidate[i] for i in range(m)]) + start[j] for j in range(n)]
    prob += (max - min), "dispatch_power"

    for i in range(m):
        prob += lpSum([x[i][j] for j in range(n)]) == 1, f"dispatch_once_{i}"

    for i in range(n):
        prob += lpSum([x[j][i] for j in range(m)]) == choose, f"dispatch_{i}"
        prob += psum[i] >= lb[i], f"dispatch_lb_{i}"
        prob += max >= psum[i], f"max_{i}"
        prob += min <= psum[i], f"min_{i}"

    prob.solve(PULP_CBC_CMD(msg=False, gapAbs = 200))
    result = {v.name: int(v.varValue) for v in prob.variables()}
    ret = [next(i for i in range(n) if result[vname(j, i)] == 1) for j in range(m)]
    return prob.status == LpStatusOptimal, ret

def memory_use_average(items: List[int], target_cnt: int) -> Tuple[bool, List[int]]:
    '''
    均匀使用碎片，使得剩余碎片的最大值尽可能小，整数规划
    :param items: 碎片数量
    :param target_cnt: 目标数量
    :return: 是否有解，每种碎片使用数量
    '''
    n = len(items)
    prob = LpProblem(name='memory_use', sense=LpMinimize)

    x = [LpVariable(f"x_{i}", lowBound=0, upBound=items[i], cat=LpInteger) for i in range(n)]
    max = LpVariable("max")

    prob += max, "object"

    prob += lpSum([x[i] for i in range(n)]) == target_cnt, f"total_use"
    for i in range(n):
        prob += max >= items[i] - x[i], f"max_{i}"

    prob.solve(PULP_CBC_CMD(msg=False))
    result = {v.name: int(v.varValue) for v in prob.variables()}
    ret = [result[f"x_{i}"] for i in range(n)]
    return prob.status == LpStatusOptimal, ret

def memory_use_average_binary_search(items: List[int], target_cnt: int) -> Tuple[bool, List[int]]:
    '''
    均匀使用碎片，使得剩余碎片的最大值尽可能小，二分
    :param items: 碎片数量
    :param target_cnt: 目标数量
    :return: 是否有解，每种碎片使用数量
    '''
    if sum(items) < target_cnt:
        return False, []
    l, r = 0, max(items) + 1
    while l + 1 < r: # [l, r)
        mid = (l + r) // 2;
        if sum(max(0, item - mid) for item in items) >= target_cnt:
            l = mid
        else:
            r = mid
    ret = [max(0, item - l) for item in items]
    mod = sum(ret) - target_cnt
    pos = [i for i in range(len(items)) if ret[i] > 0][:mod]
    for i in pos:
        ret[i] -= 1
    return True, ret

def ex_equip_power_max_cost_flow(edges: List[Tuple[str, str, int, int]], s: str, t: str) -> Tuple[int, List[Tuple[str, str, int]]]:
    '''
    最大流最小费用流求解EX装备战力分配问题
    :param edges: 边列表，(u, v, capacity, cost)
    :param n: 节点数量
    :param source: 源点
    :param sink: 汇点
    :return: 最小费用，分配策略列表(u, v, flow)
    '''
    G = nx.DiGraph()
    for edge in edges:
        u, v, capacity, cost = edge
        G.add_edge(u, v, capacity=capacity, weight=cost)

    # 求最小费用最大流
    minCostFlow = nx.max_flow_min_cost(G, s, t)
    minCost = nx.cost_of_flow(G, minCostFlow)
    strategy = []
    strategy = []
    for u, v in G.edges():
        flow = minCostFlow[u][v]
        if flow > 0:
            strategy.append((u, v, flow))
    return minCost, strategy

if __name__ == '__main__':
    # ilp_solver([3, 1, 1], 100, 1000, [10, 20, 30])
    # candidate = [61504,58688,58534,58201,57029,56686,56452,56348,56287,56238,56179,55966,55508,55117,55099,55039,54990,54661,54454,54400,54295,54055,53413,53290,53169,52944,52925,52235,51849,51713,51033,51026,50443,50233,49224,48957,48936,48890,48787,48603,48601,48600,48214,47903,47851,47507,47253,47129,46984,46881,46804,46765,46753,46600,46569,46567,46566,46476,46440,46297,45831,45808,45796,45783,45653,45626,45623,45560,45491,45472,45317,45206,45051,45038,44954,44741,44673,44601,44244,44108,43921,43838,43643,43532,43434,43259,43187,42857,42849,42791,42671,42534,42481,42309,42272,41880,41851,41755,41714,41481,41130,41034,40982,40966,40873,40686,40510,40188,39742,39522,39444,39153,38338,38107,37976,37776,37063,36895,36862,36653,35553,35303,34773,34740,34290,34198,33768,33102,32617,32519,31543,30843,30610,29648,29526,27902,27798,26901,26753,26283,26250,24512,23968,23779,22667,22347,22179,21796,21322,21019,20938,19611,19415,18988,16064,13391,12020,11845,4395,1721,1588,1443,1394,1384,1322,1316,1276,1233,1229,1223,1213,1206,1200,1180,1171,1162,1161,1146,1084,1083,725,689,685,628,628,621,601,601,599,594,498,497,496,465]
    # candidate = candidate[:24]
    # dispatch_solver([0,0,0], candidate, [100000, 100000, 100000], 8)
    # memory_use_average([1, 1, 55, 46, 10, 90, 3, 124, 90, 4, 33, 31, 5, 51, 18, 114, 30, 9, 47, 22, 19, 53, 9, 9, 37, 22, 24, 32, 176, 32, 200, 234, 322, 103, 44, 21, 45, 69, 20, 58, 57, 147, 85, 27, 9, 89, 31, 46, 37, 22, 7, 9, 16, 46, 88, 38, 16, 33, 15], 3000)
    # memory_use_average_binary_search([1, 1, 55, 46, 10, 90, 3, 124, 90, 4, 33, 31, 5, 51, 18, 114, 30, 9, 47, 22, 19, 53, 9, 9, 37, 22, 24, 32, 176, 32, 200, 234, 322, 103, 44, 21, 45, 69, 20, 58, 57, 147, 85, 27, 9, 89, 31, 46, 37, 22, 7, 9, 16, 46, 88, 38, 16, 33, 15], 3000)
    edges = eval(open("input.txt").read())
    cost, s = ex_equip_power_max_cost_flow(edges, 'st', 'ed')
    print(cost)

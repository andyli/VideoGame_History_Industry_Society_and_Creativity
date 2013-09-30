from pulp import *

num_topics = 9
groups = [
    [4, 8, 7, 2, 1, 3, 6, 9, 5],
    [6, 8, 3, 2, 9, 5, 1, 7, 4],
    [3, 4, 8, 1, 9, 5, 7, 6, 2],
    [3, 2, 4, 9, 8, 1, 7, 5, 6],
    [2, 4, 9, 8, 3, 1, 7, 5, 6],
    [8, 3, 1, 9, 4, 6, 2, 5, 7]
]

prob = LpProblem("Assign Topics", LpMinimize)
group_vars = [[LpVariable("group_{}_is_{}".format(gi, ti), 0, 1, LpBinary) for ti in range(num_topics)] for gi in range(len(groups))]
prob += pulp.lpSum([group_vars[gi][p-1] * pi * pi for gi, g in enumerate(groups) for pi, p in enumerate(g)])

for gi in range(len(groups)):
    prob += pulp.lpSum(group_vars[gi]) == 1

for ti in range(num_topics):
    prob += pulp.lpSum([group_vars[gi][ti] for gi in range(len(groups))]) <= 1

prob.solve()

print pulp.LpStatus[prob.status], pulp.value(prob.objective)

for gi in range(len(groups)):
    print "group", gi, "is", sum([value(group_vars[gi][pi]) * (pi+1) for pi in range(num_topics)])
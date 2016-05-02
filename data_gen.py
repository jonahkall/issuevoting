import numpy as np
import matplotlib.pyplot as plt

num_voters = 10000
num_issues = 8
num_candidates = 10

rule_1_scores = [0] * num_candidates
plurality_scores = [0] * num_candidates

# this is dumb but just doing this for now to
# get winners under the two rules
alphas = np.abs(np.random.normal(0,5,(num_voters,num_issues)))
betas = np.abs(np.random.normal(0,5,(num_voters,num_issues,num_candidates)))

for i in xrange(num_voters):
	r1tmp = [0] * num_candidates
	for j in xrange(num_issues):
		for k in xrange(num_candidates):
			r1tmp[k] += alphas[i][j] * betas[i][j][k]
			rule_1_scores[k] += alphas[i][j] * betas[i][j][k]
	tmax = 0
	for a in xrange(len(r1tmp)):
		if r1tmp[a] > r1tmp[tmax]:
			tmax = a
	plurality_scores[tmax] += 1

print "Rule 1 candidate ranking:", np.argsort(rule_1_scores)
print "Plurality candidate ranking:", np.argsort(plurality_scores)
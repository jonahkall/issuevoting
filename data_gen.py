import numpy as np
import matplotlib.pyplot as plt

num_voters = 10
num_issues = 8
num_candidates = 10
num_alpha_bases = 7
num_beta_bases = 12

# first entry is unnormalized rule 1
rule_1_scores = [0] * num_candidates
plurality_scores = [0] * num_candidates
borda_scores = [0] * num_candidates
two_step_scores = [0] * num_candidates

def normalize_and_fix_zeros(v):
	return [a/float(sum(v)) if a >= 0 else 0 for a in v]

def max_ind(vec):
	maxi = 0
	m = vec[0]
	for i, a in enumerate(vec):
		if a > m:
			maxi = i
	return maxi

basis_alphas = np.random.random((num_alpha_bases, num_issues))
basis_betas = np.random.random((num_beta_bases, num_candidates))

alphas = []
betas = []

beta_offsets = np.abs(np.random.normal(0, 0.10, (num_issues, num_candidates)))

for i in xrange(num_voters):
	basis_alpha_ind = np.random.randint(num_alpha_bases)
	alpha = np.random.normal(basis_alphas[basis_alpha_ind], 0.08)

	# If any entries in alpha are negative, we will ignore them
	alpha = normalize_and_fix_zeros(alpha)
	alphas.append(alpha)

	# Now we need to generate our beta
	beta = []
	basis_beta_ind = np.random.randint(num_beta_bases)
	for j in xrange(num_issues):
		bjtmp = np.random.normal(basis_betas[basis_beta_ind], 0.08)
		bjtmp = normalize_and_fix_zeros(bjtmp)
		beta.append(bjtmp)
	beta = np.array(beta)
	beta += beta_offsets
	betas.append(beta)

# First take care of plurality, borda, rule 1
for i in xrange(num_voters):
	for j in xrange(num_issues):
		borda = np.argsort(betas[i][j])
		for k in xrange(num_candidates):
			rule_1_scores[k] += alphas[i][j] * betas[i][j][k]
			borda_scores[k] += alphas[i][j] * borda[k]
		plurality_scores[max_ind(betas[i][j])] += alphas[i][j]

# now two step
# first aggregate alphas
alpha_final = [0] * len(alphas[0])
for alph in alphas:
	for j in xrange(len(alphas[0])):
		alpha_final[j] += alph[j]

superbetas = np.zeros((num_candidates, num_issues))
# now aggregate betas
for i in xrange(num_voters):
	for j in xrange(num_issues):
		borda = np.argsort(betas[i][j])
		for k in xrange(num_candidates):
			superbetas[k][j] += borda[k]
	
for j in xrange(num_issues):
	for i in xrange(num_candidates):
		two_step_scores[i] += alpha_final[j] * superbetas[i][j]	

print "Rule 1 candidate ranking:", np.argsort(rule_1_scores)
print "Plurality candidate ranking:", np.argsort(plurality_scores)
print "Borda ranking:", np.argsort(borda_scores)
print "Two step ranking:", np.argsort(two_step_scores)


lambda = var('lambda')
AA1, BB1, CC1, DD1, EE1, FF1 = var('AA1, BB1, CC1, DD1, EE1, FF1')
AA2, BB2, CC2, DD2, EE2, FF2 = var('AA2, BB2, CC2, DD2, EE2, FF2')


A = matrix([[AA1, BB1, DD1], [BB1, CC1, EE1], [DD1, EE1, FF1]])
B = matrix([[AA2, BB2, DD2], [BB2, CC2, EE2], [DD2, EE2, FF2]])

expand(det(lamda*A + B))

#-----------------------------------------------------------------------
# After sage ....
#-----------------------------------------------------------------------


# lamda ^ 3
- CC1*DD1^2*lam^3 
+ 2*BB1*DD1*EE1*lam^3 
- AA1*EE1^2*lam^3 
- BB1^2*FF1*lam^3 
+ AA1*CC1*FF1*lam^3 

# lambda ^ 2
- CC2*DD1^2*lam^2 
- 2*CC1*DD1*DD2*lam^2 
+ 2*BB2*DD1*EE1*lam^2 
+ 2*BB1*DD2*EE1*lam^2 
- AA2*EE1^2*lam^2
+ 2*BB1*DD1*EE2*lam^2 
- 2*AA1*EE1*EE2*lam^2 
- 2*BB1*BB2*FF1*lam^2 
+ AA2*CC1*FF1*lam^2 
+ AA1*CC2*FF1*lam^2 
- BB1^2*FF2*lam^2 
+ AA1*CC1*FF2*lam^2 

# lamda
- 2*CC2*DD1*DD2*lam 
- CC1*DD2^2*lam 
+ 2*BB2*DD2*EE1*lam 
+ 2*BB2*DD1*EE2*lam 
+ 2*BB1*DD2*EE2*lam 
- 2*AA2*EE1*EE2*lam 
- AA1*EE2^2*lam 
- BB2^2*FF1*lam 
+ AA2*CC2*FF1*lam 
- 2*BB1*BB2*FF2*lam 
+ AA2*CC1*FF2*lam 
+ AA1*CC2*FF2*lam 

# constant
- CC2*DD2^2 
+ 2*BB2*DD2*EE2 
- AA2*EE2^2 
- BB2^2*FF2 
+ AA2*CC2*FF2

import math

n_stock = 10
xi = 0
yi = 0
n_stock = 5
n_col = math.ceil(math.sqrt(n_stock))
n_row = math.ceil(n_stock / n_col)
print([n_col, n_row])

for i in range(n_stock):
	print([xi, yi])

	if xi < n_col - 1:
		xi += 1
	else:
		yi += 1
		xi = 0

import math
import sys
from array import array
sys.setrecursionlimit(1500)
#9009131337
#2,100,000

class Counter():
	collatzCache = {}
	def start(self, input_val):
		if input_val < 11:
			return 0
			
		total = 0
		for i in range(input_val + 1):
			total += self.collatz(i)
		fib_value = self.fib(input_val, total)
		return fib_value
		
	
	def collatz(self, input_val):				
			counter = 0
			testing_var = input_val
			while testing_var >= 2:
				#if testing_var in self.collatzCache:
				#	counter += self.collatzCache[testing_var]
				#	break
					
				if testing_var % 2 == 1:
					testing_var = (3 * testing_var) + 1
				else:
					testing_var = math.floor(testing_var/2)
				counter += 1
				
			#self.collatzCache[input_val] = counter
			return counter
	
	"""
	def collatz(self, limit):
		maximum = 0
		known = array("L", (0 for i in range(limit)))
		for num in range(2, limit):
			steps = known[num]
			if steps:
				print(steps)
				return steps
			else:
				start_num = num
				steps = 0
				while num != 1:
					if num < start_num:
						steps += known[num]
						break
					while num & 1:
						num += (num >> 1) + 1
						steps += 2
					while num & 1 == 0:
						num >>= 1
						steps += 1
				
				temp_start_num = start_num
				while temp_start_num < limit:
					assert known[temp_start_num] == 0
					known[temp_start_num] = steps
					temp_start_num <<= 1
					steps += 1
				return known[start_num]
	"""
	
	
	def fib(self, n, modulo): 
	      
	    F = [[1, 1], 
	         [1, 0]] 
	    if (n == 0): 
	        return 0
	    self.power(F, n - 1, modulo) 
	          
	    return F[0][0] % modulo
	
	      
	def multiply(self, F, M, modulo): 
	      
	    x = (F[0][0] * M[0][0] + 
	         F[0][1] * M[1][0]) 
	    y = (F[0][0] * M[0][1] + 
	         F[0][1] * M[1][1]) 
	    z = (F[1][0] * M[0][0] + 
	         F[1][1] * M[1][0]) 
	    w = (F[1][0] * M[0][1] + 
	         F[1][1] * M[1][1]) 
	      
	    F[0][0] = (x % modulo)
	    F[0][1] = (y % modulo) 
	    F[1][0] = (z % modulo)
	    F[1][1] = (w % modulo)
	
	def power(self, F, n, modulo):
		if n == 0 or n == 1:
			return
		
		M = [[1, 1],
			[1, 0]]
		
		self.power(F, math.floor(n/2), modulo)
		self.multiply(F, F, modulo)
		
		if n % 2 != 0:
			self.multiply(F, M, modulo)




counter = Counter()
input_value = sys.argv[1]
print(hex(counter.start(int(input_value))))

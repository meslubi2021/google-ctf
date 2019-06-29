import math
import sys
import numpy as np
#from fastcache import lru_cache

#sum for 0 to 10,000 is 849666

#9009131337
#9,009,131,337
#recurvsive (900,000) = 53.0 * 10,000
#recurvsive (900,000) + functools.lru_cache = 9.2 * 10,000
#dictionary with bit wizardry = 1.74 * 10,000
#np.arry with bit wizardry = 1.93 * 10,000
#C (900,000) = 0.058 * 10,000
#C++ (900,000) = 0.61 * 10,000

#8.0 seconds for miss caching
#16.4 seconds for latest cached
#13.6 cache largest steps

sys.setrecursionlimit(1500)

class Counter():
	def start(self, input_val):
		if input_val < 11:
			return 0
			
		total = self.collatzSum(input_val)
		print("collatz(10,000) = " + str(self.collatz(10000)))
		print("total=" + str(total))
		fib_value = self.fib(input_val, total)
		return fib_value
		
	
	def collatzSum(self, upperLimit, x):
		totalSteps = 0
		cacheSize = 10000000
		#collatzCache = dict.fromkeys(range(cacheSize))
		collatzCache = np.zeros(cacheSize)

		for num in range(1, upperLimit + 1):
			start_num = num
			steps = 0
			while num != 1:
				#check cache
				if num < start_num:
					steps += collatzCache[num]
					break
				
				#not in cache calculate next collatz
				if num & 0x1: #odd
					num += (num >> 1) + 1
					steps += 2
				
				if num & 0x1 == 0: #even
					num >>= 1
					steps += 1
			
			#write to cache
			collatzCache[start_num] = steps
		
		#sum cache
		totalSteps = np.sum(collatzCache, dtype = 'int')
		#totalSteps = sum(collatzCache)

		return totalSteps

	def collatzSum(self, upperLimit):
		total = 0
		for i in range(upperLimit + 1):
			total +=self.collatz(i)
		return total
	
	def collatz(self, num):
		if num <= 1:
			return 0
		else:
			if num % 2 == 1:
				return self.collatz((3 * num) + 1) + 1
			else:
				return self.collatz(num/2) + 1
	
	
	
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

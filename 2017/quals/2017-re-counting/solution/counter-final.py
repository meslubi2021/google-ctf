import math
import sys

class Counter():
	def start(self, input_val):
		if input_val < 11:
			return 0
		
		
		total = 0
		i = input_val
		while(i >= 0):
			total += self.collatz(i)
			i -= 1
		fib_value = self.fib(input_val)
		return fib_value % total
		
	def collatz(self, input_val):
			counter = 0
			testing_var = input_val
			while testing_var >= 2:
				print(testing_var)
				if testing_var % 2 == 1:
					testing_var = (3 * testing_var) + 1
				else:
					testing_var = math.floor(testing_var/2)
				counter += 1
			return counter
	
	def fib(self, fib_value):
		if fib_value == 0:
			return 0
		elif fib_value == 1:
			return 1
		else:
			return self.fib(fib_value - 1) + self.fib(fib_value - 2)


counter = Counter()

#for i in range(0, 20):
#	result = counter.oddEven(i)
#	print("input = " + str(i) + ", result = " + str(result))


input_value = sys.argv[1]
print(hex(counter.start(int(input_value))))

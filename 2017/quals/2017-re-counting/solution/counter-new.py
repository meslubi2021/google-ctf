import sys
import struct
import binascii
import math

class Counter():
	TOTAL_LINES = 0x77
	CODE_FILEPOINTER = None
	
	
	def _0x00(self, key_buffer):
		self.copyAndClearQwords(key_buffer, 0x8, 0x0)
		return 0x02
		
	def _0x20(self, key_buffer):
		self.writeQWord(key_buffer, 0x10, 11)
		return 0x0d
		
	def _0xd0(self, key_buffer):
		print("nop")
		return 0x0e
		
	def _0x140(self, key_buffer):
		self.writeQWord(key_buffer, 0x10, 0)
		return 0x15
		
	def _0x150(self, key_buffer):
		counter = 0
		testing_var = self.toQWord(key_buffer[0x8:0x8+8])
		while testing_var >= 2:
			if testing_var % 2 == 1:
				testing_var = (3 * testing_var) + 1
			else:
				testing_var = math.floor(testing_var/2)
			counter += 1
		self.writeQWord(key_buffer, 0x00, counter)
		return 0x16
		
	def _0x1e0(self, key_buffer):
		self.copyQWords(key_buffer, 0x0, 0x8)
		return 0x1f
		
	def _0x1f0(self, key_buffer):
		self.writeQWord(key_buffer, 0x18, 0)
		return 0x20
		
	def _0x200(self, key_buffer):
		self.copyAndClearQwords(key_buffer, 0x18, 0x0)
		return 0x22
	def _0x240(self, key_buffer):
		print("WARNING - 0x240 is broken")
		print("key_buffer[0x0] = math.floor(key_buffer[0x8]/2)")
		key_buffer[0x0] = math.floor(key_buffer[0x8]/2)
		print("if key_buffer[0x8] mod 2 == 1: then (%s)" %(key_buffer[0x8] % 2 == 1))
		if key_buffer[0x8] % 2 == 0:
			return 0x25
		print("	key_buffer[0x0] = 3 * key_buffer[0x8] + 1")
		key_buffer[0x0] = 3 * key_buffer[0x8] + 1 
		return 0x25
		
	def _0x2d0(self, key_buffer):
		self.writeQWord(key_buffer, 0x10, 0)
		return 0x2e
		
	def _0x2e0(self, key_buffer):
		self.copyQWords(key_buffer, 0x0, 0x8)
		return 0x2f
		
	def _0x2f0(self, key_buffer):
		self.copyAndClearQwords(key_buffer, 0x10, 0x0)
		return 0x31
		
	def _0x310(self, key_buffer):
		if self.toQWord(key_buffer[0x0:0x0+8]) != 0 | self.toQWord(key_buffer[0xc8:0xc8+8]) != 0:
			print("WARNING")
		
		self.writeQWord(key_buffer, 0x8, 0)
		
		print("key_buffer[0x0] = key_buffer[0x10]/2")
		value1 = self.toQWord(key_buffer[0x10:0x10+8])
		key_buffer[0x0:0x0+8] = struct.pack("<q", math.floor(value1/2))
		print("if key_buffer[0x10] % 2 == 1 (%s)" % (value1 % 2 == 1))
		if value1 % 2 == 1:
			print("key_buffer[0x8] = 1")
			key_buffer[0x8:0x8+8] = struct.pack("<q", 1)
		return 0x32
	
	def _0x260(self, key_buffer):
		self.writeQWord(key_buffer, 0x8, 0)
		return 0x27
		
	def _0x270(self, key_buffer):
		self.copyAndClearQwords(key_buffer, 0x8, 0x0)
		return 0x29
		
	def _0x330(self, key_buffer):
		self.writeQWord(key_buffer, 0x0, 0)
		return 0x34
		
	def _0x350(self, key_buffer):
		self.copyAndClearQwords(key_buffer, 0x8, 0x10)
		return 0x37
		
	def _0x370(self, key_buffer):
		self.copyQWords(key_buffer, 0x0, 0x8)
		return 0x38
		
	def _0x380(self, key_buffer):
		self.copyAndClearQwords(key_buffer, 0x10, 0x0)
		return 0x3a
		
	def _0x3a0(self, key_buffer):
		self.copyQWords(key_buffer, 0x0, 0x8)
		return 0x3b
		
	def _0x3b0(self, key_buffer):
		self.copyAndClearQwords(key_buffer, 0x00, 0x8)
		return 0x3d
		
	def _0x3d0(self, key_buffer):
		self.copyAndClearQwords(key_buffer, 0x00, 0x10)
		return 0x3f
		
	def _0x1d0(self, key_buffer):
		self.writeQWord(key_buffer, 0x10, 0)
		return 0x1e
		
	
	optimizer = {
		0x00: _0x00,
		0x20: _0x20,
		0xd0: _0xd0,
		0x140: _0x140,
		0x150: _0x150,
		0x1e0: _0x1e0,
		0x1f0: _0x1f0,
		0x200: _0x200,
		0x240: _0x240,
		0x2d0: _0x2d0,
		0x2e0: _0x2e0,
		0x2f0: _0x2f0,
		0x310: _0x310,
		0x260: _0x260,
		0x270: _0x270,
		0x330: _0x330,
		0x350: _0x350,
		0x370: _0x370,
		0x380: _0x380,
		0x3a0: _0x3a0,
		0x3b0: _0x3b0,
		0x3d0: _0x3d0,
		0x1d0:	_0x1d0,
	 }
	
	def init(self):
		f = open("./code", "rb")
		self.CODE_FILEPOINTER = f.read()
		self.CODE_FILEPOINTER = self.CODE_FILEPOINTER[4:]
		
	def toDWord(self, code_buffer):
		return struct.unpack("<i", code_buffer)[0]
	def toQWord(self, code_buffer):
		return struct.unpack("<q", code_buffer)[0]
		
	def packQWord(self, value_buffer, offset, value):
		return struct.pack_into("<q", value_buffer, offset, value )
		
	def copyQWords(self, key_buffer, destination, source):
		destinationValue = self.toQWord(key_buffer[destination:destination+8])
		sourceValue = self.toQWord(key_buffer[source:source+8])
		print("key_buffer[0x%x] += key_buffer[0x%x]" % (destination, source))
		key_buffer[destination:destination + 8] = struct.pack("<q", sourceValue + destinationValue)
	
	def copyAndClearQwords(self, key_buffer, destination, source):
		self.copyQWords(key_buffer, destination, source)
		print("key_buffer[0x%x] = 0" % (source))
		key_buffer[source:source + 8] = struct.pack("<q", 0)
		
	def writeQWord(self, key_buffer, destination, value):
		print("key_buffer[0x%x] = %s" % (destination, value))
		key_buffer[destination:destination+8] = struct.pack("<q", value)
	
	def counter(self, key_buffer, line_num):
		print("starting counter, key = " + str(binascii.hexlify(key_buffer)))
		while line_num != self.TOTAL_LINES:
			current_line = line_num << 4
			headerByte = self.toDWord(self.CODE_FILEPOINTER[current_line:current_line+4])
			
			print("(0x%x) - " % (current_line), end ="")
			
			#special cases
			if current_line in self.optimizer:
				line_num = self.optimizer[current_line](self, key_buffer)
				continue
				
			
			
			if headerByte == 0:
				#add 1 at key_address
				key_address = self.CODE_FILEPOINTER[current_line+4] * 8
				_temp = self.toQWord(key_buffer[key_address:key_address+8]) + 1
				self.packQWord(key_buffer, key_address, _temp)
				line_num = self.toDWord(self.CODE_FILEPOINTER[current_line+8:current_line+8+4])
				print("add 1, at = 0x%x, new_val = %s" % (key_address, _temp))
			if headerByte == 1:
				#subtract 1 at key_address if already zero then jump to different spot
				key_address = self.CODE_FILEPOINTER[current_line+4] * 8
				Qword_value = self.toQWord(key_buffer[key_address:key_address+8])
				if Qword_value != 0:
					Qword_value = Qword_value -1
					
					line_num = self.toDWord(self.CODE_FILEPOINTER[current_line+8:current_line+8+4])
					self.packQWord(key_buffer, key_address, Qword_value)
					print("sub 1, at = 0x%x, new_val = %s" % (key_address, Qword_value))
				else:
					line_num = self.toDWord(self.CODE_FILEPOINTER[current_line+12:current_line+12+4])
					print("zero , at = 0x%x, jumping" % (key_address))
			if headerByte == 2:
				#call counter from new_next_line copy result if firstDWord greater than zero
				new_buffer = key_buffer[:]
				new_next_line = self.toDWord(self.CODE_FILEPOINTER[current_line+8:current_line+8+4])
				firstQWord = self.toDWord(self.CODE_FILEPOINTER[current_line+4:current_line+4+4])
				print("call , to = 0x%x and copy first = %s bytes" % (new_next_line, firstQWord))
				self.counter(new_buffer, new_next_line)
				if firstQWord != 0:
					key_buffer[0:firstQWord*8] = new_buffer[0:firstQWord*8]
				line_num = self.toDWord(self.CODE_FILEPOINTER[current_line+12:current_line+12+4])
				
		print("exiting counter, key = " + str(binascii.hexlify(key_buffer)))
					
					
	

count = Counter()
count.init()

input_value = int(sys.argv[1])
key = bytearray(struct.pack("<q", input_value)) + bytearray([0]*200)
count.counter(key, 0)
result = str(hex(struct.unpack("<q", key[0:8])[0]))[2:]
if len(result) < 16:
	result = "0"*(16-len(result)) + result

print(binascii.hexlify(key))

print("---")
print("CTF{" + result + "}")



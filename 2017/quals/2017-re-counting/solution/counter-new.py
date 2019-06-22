import sys
import struct
import binascii

class Counter():
	TOTAL_LINES = 0x77
	CODE_FILEPOINTER = None

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

	def counter(self, key_buffer, line_num):
		while line_num != self.TOTAL_LINES:
			current_line = line_num << 4
			headerByte = self.toDWord(self.CODE_FILEPOINTER[current_line:current_line+4])
			
			print("(0x%x) - " % (current_line), end ="")
			
			#special cases
			if current_line == 0x0:
				print("key_buffer[0x8] = key_buffer[0x0]")
				key_buffer[0x8:0x8 + 8] = key_buffer[0x0:0x0+8]
				print("key_buffer[0x0] = 0x0")
				key_buffer[0x0:0x0 + 8] = struct.pack("<q", 0)
				line_num = 0x02
				continue
			if current_line == 0xd0:
				print("nop - jump to 0x0e")
				line_num = 0x0e
				continue
			#if current_line == 0x1e0:
			#	value1 = self.toQWord(key_buffer[0x0:0x0+8])
			#	if value1 != 0:
			#		print("WARNING")
			#	print("key_buffer[0x0] = key_buffer[0x8]")
			#	continue
			
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
				print("call , to = 0x%x" % (new_next_line))
				self.counter(new_buffer, new_next_line)
				firstQWord = self.toDWord(self.CODE_FILEPOINTER[current_line+4:current_line+4+4])
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



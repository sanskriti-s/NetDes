a1_bit_flip = """\

a1 = 0b1101010001101111 # accepts the binary input but will store it as an int

a1_bin = bin(a1)[2:] # creates a string of the binary form of the integer minus the first 2 characters

flip_bin_a1 = a1_bin.translate(str.maketrans("10","01"))"""

a = 0b1001010000101001
print(a)
b = 0b1111000111110100

#a = a + b
#if(a > 65536):
#    a -= 65536
#    a += 1

# after all additions, then flip the compliment and make it an integer value
a_bin = bin(a)
a_flipped = int(a_bin.translate(str.maketrans("10", "01"))[2:], 2)

print(int(a_bin, 2))

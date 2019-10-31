a1_bit_flip = """\

a1 = 0b1101010001101111 # accepts the binary input but will store it as an int

a1_bin = bin(a1)[2:] # creates a string of the binary form of the integer minus the first 2 characters

flip_bin_a1 = a1_bin.translate(str.maketrans("10","01"))"""

a = 973
b = 7154

verify = bin(a^b)
checker = (2 ** (len(verify) - 2)) - 1
if int(verify, 2) == checker:
    print("True")
else:
    print("False")

import timeit

a1_bit_flip = """\

a1 = 0b1101010001101111 # accepts the binary input but will store it as an int

a1_bin = bin(a1)[2:] # creates a string of the binary form of the integer minus the first 2 characters

flip_bin_a1 = a1_bin.translate(str.maketrans("10","01"))"""


trans_time = timeit.timeit(a1_bit_flip, number=100000) # time 100k iterations

print('translate time')

print(trans_time / 100000) # determine average time of a single iteration ~ 0.6282 us

print('\n')

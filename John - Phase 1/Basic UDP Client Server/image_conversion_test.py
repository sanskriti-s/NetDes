from PIL import Image # for pillow image handling

imageName = '42.bmp'

ogBmp = Image.open(imageName) # create image object
#ogBmp.show() # show original image
# print(ogBmp) # PY displays original image info
print(ogBmp.size) # PILf outputs image size: is a tuple

#ogBmp.rotate(45).show() # rotate and show received & stored image

#ogImage = open(imageName,'rb') # PY opens file for reading in binary mode
#ogImageBin = ogImage.read() # stores the binary file into a temporary file

localBytes = ogBmp.tobytes(encoder_name = 'raw') # convert image to bytes for TX
# encoder is the default & not strictly necessary

# ERROR size = ('36, 36,') # will a string work ? NO SIZE must be a tuple

newBmp = Image.frombytes('RGB', size, localBytes, decoder_name = 'raw')
# (mode, size, data, decoder_name = 'raw', *args) size must be at least a 2 dimension tuple

#newBmp.save('test.bmp')
newBmp.rotate(45).show() 


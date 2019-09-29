import ast
from PIL import Image # for pillow image handling

imageName = '42.bmp'
open(imageName, mode = 'rb') # PY open file for binary reading

ogBmp = Image.open(imageName) # PILf create image object
imgSize = ogBmp.size
# print(imgSize) # i can get the size as a tuple object
# imgSizeBin = imgSize.encode() # cant encode tuple object
# i need to convert the tuple to a string so it is easy to encode and send

ogImgSizeString = (str(ogBmp.size)) # converts the 2 tuple size of the image into a string
#print(ogImgSizeString)
#imgSizeString =  ','.join(imgSize) 
#print(imgSizeString)
print('Did it work ??')

sizeString = (ogImgSizeString) # given a 2 tuple size string, was '36, 36'
sizeStringEncoded = sizeString.encode() # encode it for binary TX
# print(sizeStringEncoded)
localBytes = ogBmp.tobytes() # convert image to bytes for TX, encoder_name = 'raw'
# print (localBytes) # displays image binary data LARGE

# client TX the tuple & image info -> server RX the tuple & image info

sizeStringDecoded = sizeStringEncoded.decode() #decode it after RX for use
print(sizeStringDecoded)
newSizeTuple = ast.literal_eval(sizeStringDecoded) # turn sizeStringDecoded back into a sizeTuple ??

# can i use the tuple() to convert instead ?? wrong size output
# newSizeTuple = tuple(sizeStringDecoded)
#print(newSizeTuple)

newBmp = Image.frombytes('RGB', newSizeTuple, localBytes) # decoder_name = 'raw'
newBmp.rotate(45).show() # works : )
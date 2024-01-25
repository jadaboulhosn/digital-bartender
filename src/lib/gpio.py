BOARD = 1
OUT = 1
IN = 1

HIGH = 1
LOW = 0

def setmode(a):
   print("Mode:" + a)
def setup(a, b):
   print("Setup: " + str(a) + " -> " + str(b))
def output(a, b):
   print("Output: " + str(a) + " -> " + str(b))
def cleanup():
   print('Cleanup')
def setwarnings(flag):
   print("Flag: " + str(flag))
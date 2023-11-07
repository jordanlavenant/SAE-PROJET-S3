import time
import pyotp

key = pyotp.random_base32()

print("Your key is: " + key)
from machine import UART
from network import LoRa
import binascii
import os
import pycom

pycom.heartbeat(False)

# Setting up the UART to dump the output to the console
uart = UART(0, 115200)
os.dupterm(uart)

# Getting the LoRa MAC
lora = LoRa(mode=LoRa.LORAWAN, public=1, adr=0, tx_retries=0)
print("LORA MAC")
print(binascii.hexlify(lora.mac()))

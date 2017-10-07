from network import LoRa
import socket
import binascii
import cayenneLPP

# init Lorawan
lora = LoRa(mode=LoRa.LORAWAN, adr=False, tx_retries=0, device_class=LoRa.CLASS_A)

def join_lora(force_join = False):
    '''Joining The Things Network '''

    # restore previous state
    if not force_join:
        lora.nvram_restore()

    # remove default channels
    for i in range(0, 72):
        lora.remove_channel(i)

    # adding the Australian channels
    for i in range(8, 15):
        lora.add_channel(i, frequency=915200000 + i * 200000, dr_min=0, dr_max=3)
    lora.add_channel(65, frequency=917500000, dr_min=4, dr_max=4)

    for i in range(0, 7):
        lora.add_channel(i, frequency=923300000 + i * 600000, dr_min=0, dr_max=3)

    if not lora.has_joined() or force_join == True:

        # create an OTA authentication params
        app_eui = binascii.unhexlify('APP EUI'.replace(' ','')) # these settings can be found from TTN
        app_key = binascii.unhexlify('APP KEY'.replace(' ','')) # these settings can be found from TTN

        # join a network using OTAA if not previously done
        lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

        # wait until the module has joined the network
        while not lora.has_joined():
            time.sleep(2.5)

        # saving the state
        lora.nvram_save()

        # returning whether the join was successful
        if lora.has_joined():
            return True
        else:
            return False

    else:
        return True

# joining TTN
join_lora(True)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
s.setblocking(True)

# creating Cayenne LPP packet
lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)

# creating some payloads and sending them
lpp.add_digital_input(True)
lpp.add_digital_input(False, channel = 112)
lpp.send(reset_payload = True)

lpp.add_digital_output(True)
lpp.add_digital_output(False, channel = 113)
lpp.send(reset_payload = True)

lpp.add_analog_input(102.34)
lpp.add_analog_input(-89.34, channel = 114)
lpp.send(reset_payload = True)

lpp.add_analog_output(102.34)
lpp.add_analog_output(-89.34, channel = 115)
lpp.send(reset_payload = True)

lpp.add_luminosity(1024)
lpp.add_luminosity(6000.87, channel = 116)
lpp.send(reset_payload = True)

lpp.add_presence(True)
lpp.add_presence(False, channel = 117)
lpp.send(reset_payload = True)

lpp.add_temperature(-11.0)
lpp.add_temperature(54.3, channel = 118)
lpp.send(reset_payload = True)

lpp.add_relative_humidity(100.0)
lpp.add_relative_humidity(0.0, channel = 119)
lpp.add_relative_humidity(45.5, channel = 120)
lpp.send(reset_payload = True)

lpp.add_accelerometer(12.441,20.112,7.023)
lpp.send(reset_payload = True)
lpp.add_accelerometer(12.441,-30.112,8.023, channel = 121)
lpp.send(reset_payload = True)

lpp.add_barometric_pressure(123.3)
lpp.add_barometric_pressure(0.4, channel = 122)
lpp.send(reset_payload = True)

lpp.add_gyrometer(12.02,23.44,-23.01)
lpp.send(reset_payload = True)
lpp.add_gyrometer(-12.02,-23.44,23.01, channel = 123)
lpp.send(reset_payload = True)

lpp.add_gps(50.5434, 4.4069, 100.98)
lpp.send(reset_payload = True)
lpp.add_gps(-34.406183, 150.880962, 10.3, channel = 124)
lpp.send(reset_payload = True)

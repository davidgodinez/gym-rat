import bluetooth

target_name = "BLE Counter"
target_address = "ED:5E:20:E7:2B:A1"

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name(bdaddr):
        target_address = bdaddr
        break

if target_address is not None:
    print(f"Found target Bluetooth device with address {target_address}")
else:
    print("Could not find target Bluetooth device nearby")

# Create the client socket
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    client_socket.connect((target_address, 1))
    print("Connected to the device")
except bluetooth.btcommon.BluetoothError as err:
    print(f"Unable to connect: {err}")

# After this point you can start sending or receiving data from the device
# ...

# Close the connection when finished
client_socket.close()

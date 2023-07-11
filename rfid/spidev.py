import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
resp = spi.xfer2([0x01, 0xA0, 0x00])
print(resp)

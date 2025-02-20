import machine
sda = machine.Pin(6)
scl = machine.Pin(7)
i2c = machine.I2C(1,sda=sda,scl=scl, freq=400000)
print("I2C Address : " + hex(i2c.scan()[0]).upper())
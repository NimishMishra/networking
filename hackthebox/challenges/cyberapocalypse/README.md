# Cyberapocalyse

Post CTF solving and analysis...

## Hardware

### Serial logs

**Challenge info**: We have gained physical access to the debugging interface of the Access Control System which is based on a Raspberry Pi-based IoT device. We believe that the log messages of this device contain valuable information of when our asset was abducted.

- Single channel communication: UART (Asynchronous, serial communication)

- Very first signal's time period used for calculating baud rate (115200): 

![Initial baud](./hardware/hw_serial_logs/hardware_serial_logs_initial_baud.png)

- Baud changed midway somewhere to 74300:

![Final baud](./hardware/hw_serial_logs/hardware_serial_logs_backup_baud.png)

Flag: **CHTB{wh47?!_f23qu3ncy_h0pp1n9_1n_4_532141_p2070c01?!!!52}**

### Compromised

**Challenge info**: An embedded device in our serial network exploited a misconfiguration which resulted in the compromisation of several of our slave devices in it, leaving the base camp exposed to intruders. We must find what alterations the device did over the network in order to revert them before its too late.

So there are two channels and the talk about master-slave implies this be I2C communication. Adding a I2C analyser and we have the data. A bit of fiddling around and we get a specific address where the flag was being communicated. Extra ASCII data for that address and we got the flag. Channel 1 is the SCL, and channel 0 is the SDA.

Flag: **CHTB{nu11_732m1n47025_c4n_8234k_4_532141_5y573m!@52)@%}**

### Secure

**Challenge Info**: We need to find cover before the invasion begins but unfortunately, the bunker is secured by a smart door lock. The keys of the device are stored in an external microSD connected with wiring with the unsecured part of the device enabling us to capture some traces while trying random combinations. Can you recover the key?

Four channels and seems like SPI. The connections seem like the following:

Channel 3 = Clock. Channel 2 = enable. MOSI = Channel 1. MISO = Channel 2. Exporting data and we see a lot of interesting stuff. Therein, at the very bottom, lies the key or the flag.

Flag: **CHTB{5P1_15_c0mm0n_0n_m3m02y_d3v1c35_!@52}**
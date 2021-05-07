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
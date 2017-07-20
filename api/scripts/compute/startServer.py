from opentrons import server, robot
import boot_config as bc
import os, time

if __name__ == '__main__':
    try:
        print("[BOOT] Opening status indication pipe")
        fd = os.open(bc.STATUS_INDICATOR_FIFO, os.O_WRONLY) 
    except FileNotFoundError:
        print("[BOOT] No status indication pipe found. Sleeping - will attempt to open again")
        time.sleep(.1)
        fd = os.open(bc.STATUS_INDICATOR_FIFO, os.O_WRONLY) 
    os.write(fd, str(bc.BOOTING).encode())

    try:
        print("[BOOT] Server node setup")
        try:
            robot.connect(bc.DEFAULT_PORT)
        except RuntimeError:
            # Sometimes it fails on the first connection attempt - not sure why.
            # TODO: Change this hackey fix
            print("[BOOT] Second smoothie connect attempt")
            robot.connect(bc.DEFAULT_PORT)
        except FileNotFoundError:


        os.write(fd, str(bc.WIFI_AND_SMOOTHIE_CONNECTED).encode()) 
        server.start('0.0.0.0')
        print("[BOOT] Server node terminated")
    
    # The server above should run indefinitely 
    finally:
        os.write(fd, str(bc.ISSUE).encode()) 

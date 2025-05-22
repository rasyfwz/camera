import numpy as np
import cv2 as cv
import serial

#camera and image values
IMG_SIZE = 19278
HEIGHT = 119
WIDTH = 162
frame = bytearray()
buffer = bytearray()
frame_start = False
port = '/dev/tty.usbmodemC81A809C01BC1'

ser = serial.Serial(port, baudrate=115200, timeout=1)
try:
    while True:
        data = ser.read(ser.in_waiting)
        buffer.extend(data)

        try:
            head = buffer.index(b'\xAA\x55\xAA\x55')
            tail = buffer.index(b'\xAA\x55\xAA\x55', head + 4)
            packet = buffer[head + 4 : tail-1]
            buffer = buffer[tail:]

            #print(f'buffer size: {len(buffer)}')
            
            frame_indicator = packet[0] & 0b00000001
            if frame_indicator:
                #print(f'frame indicator: {frame_indicator}')
                frame_start = True
            
            if frame_start:
                frame += packet[1:]
            
                if len(frame) >= IMG_SIZE:
                    #print("full frame recieved")
                    img = np.frombuffer(frame[:IMG_SIZE], dtype=np.uint8).reshape((HEIGHT, WIDTH))
                    cv.imshow("camera stream", img)
                    cv.waitKey(1)
                
                    frame_start = False
                    frame = bytearray()
        except ValueError:
            continue
except KeyboardInterrupt:
    print('closing all windows...')
    cv.destroyAllWindows()

            





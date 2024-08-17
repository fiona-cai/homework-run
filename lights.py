import serial
import serial.tools.list_ports
import time

def get_port():
    ports = serial.tools.list_ports.comports()
    print(ports)
    usbports = [port for port in ports if 'USB VID:PID=0403:6001' in port.hwid]
    comm_port = usbports[0].device
    ser = serial.Serial(comm_port, 9600, timeout=1)
    return ser

def send(ser, command):
    ser.write(command if isinstance(command, (bytes, bytearray)) else command.encode())

def left_on(comm_port):
    send(comm_port, bytes([1]))

def left_off(comm_port):
    send(comm_port, bytes([2]))

def middle_on(comm_port):
    send(comm_port, bytes([3]))

def middle_off(comm_port):
    send(comm_port, bytes([4]))

def right_on(comm_port):
    send(comm_port, bytes([5]))

def right_off(comm_port):
    send(comm_port, bytes([6]))

def close(ser):
    ser.close()

if __name__ == '__main__':
    comm_port = get_port()
    time.sleep(2)
    print(comm_port)
    left_on(comm_port)
    time.sleep(1)
    left_off(comm_port)
    time.sleep(1)
    middle_on(comm_port)
    time.sleep(1)
    middle_off(comm_port)
    time.sleep(1)
    right_on(comm_port)
    time.sleep(1)
    right_off(comm_port)
    close(comm_port)

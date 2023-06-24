import sys
from time import sleep
import queue
import serial
import threading


class Uart(object):
    def __init__(self, port, baud):
        self.err = 0
        self.queue_recv=queue.Queue(10)
        try:
            self.serial = serial.Serial(port, baud)
            print("open serial success.")
        except:
            print("open serial error!")
            self.err = -1
        self.start_recv_tread()

    def uart_recv_thread(self):
        print("start uart_recv_thread.\n")
        while (True):
            try:
                sleep(0.02)
                recv_len = self.serial.inWaiting()
                if recv_len > 0:
                    recv_data_raw = self.serial.read(self.serial.inWaiting())
                    if (recv_data_raw != None):
                        data = "DEVICE---->PC: " + recv_data_raw.decode()
                        print(data)
                        if self.queue_recv.full():
                            self.queue_recv.get()
                        self.queue_recv.put(data)

            except Exception as e:
                print(e)
                print("recv data error!")
                break

    def start_recv_tread(self):
        thread = threading.Thread(target=self.uart_recv_thread, daemon=True)
        thread.start()
        #thread.join()

    def send_uart_data(self,data):
        self.serial.write(data.encode())

    def uart_close(self):
        self.serial.close()

    def flush_queue_recv(self):
        while not self.queue_recv.empty():
            self.queue_recv.get()

    def is_queue_recv_empty(self):
        return self.queue_recv.empty()

    def get_queue_recv(self):
        return self.queue_recv.get()


if __name__ == '__main__':
    myuart = Uart("COM2", 9600)
    if (myuart.err == 0):
        print("init uart success")
        myuart.start_recv_tread()

        while (True):
            input_data = input("please input data...")
            if (input_data == "quit"):
                # 退出
                myuart.uart_close()
                break
            else:
                # 发送数据给设备
                myuart.send_uart_data(input_data)
            sleep(0.01)
        print('exit!')

    else:
        print("init uart fail!")
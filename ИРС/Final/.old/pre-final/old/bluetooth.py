import bluetooth

class car_bluetooth:
    def __init__(self, MAC, port = 1):
        self.__mac = MAC
        self.__port = port
        self.__blue_soc = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def connect(self):
        print("Trying to connect: ", self.__mac)
        self.__blue_soc.connect((self.__mac, self.__port))
        print(self.__mac, "connected")

    def send (self, msgStr):
        self.__blue_soc.send(msgStr)
    
    def __del__(self):
        self.__blue_soc.close()


def main():
    serverMACAddress_car = "68:27:19:f3:94:8c"
    

    car = car_bluetooth(serverMACAddress_car)

    print("Connecting...\n")
    car.connect()
    print("Send cmd...\n")

    while 1:
        text = raw_input() # Note change to the old (Python 2) raw_input
        if text == "q":
            break
        car.send(text)

if __name__=="__main__":
    main()
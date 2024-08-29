class Destination:
    message = []

    @staticmethod
    def clear_message():
        Destination.message = []

    @staticmethod
    def add_frame(frame):
        Destination.message.append(frame)

    @staticmethod
    def read_message():

        print("Destination:")
        for i in range(0, len(Destination.message)):
            for j in range(0, len(Destination.message[i])):
                print(Destination.message[i][j], end=" ")
            print()

        print("Received message:")
        for i in range(0, len(Destination.message)):
            for j in range(0, len(Destination.message[i])):
                print(Destination.message[i][j], end=" ")
        print()

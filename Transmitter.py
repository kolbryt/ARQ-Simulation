from Noise import Noise
from Receiver import Receiver
import time


class Transmitter:

    number_of_all_shipments = []

    @staticmethod
    def clear_number_of_all_shipments():
        Transmitter.number_of_all_shipments = []

    @staticmethod
    def send_message(coded_message):

        print("Packets:")
        packet = []
        noise_frame = []
        for i in range(0, len(coded_message)):

            packet = coded_message[i]
            number_of_shipments = 0

            frame_accepted = False
            while frame_accepted != True: 
                print(str(number_of_shipments + 1) + ".\tSending frame:", end=" ")
                for j in range(0, len(packet)):
                    print(packet[j], end=" ")

                noise_frame = Noise.make_noise(packet)

                print("--> Noised frame:", end=" ")
                for j in range(0, len(noise_frame)):
                    print(noise_frame[j], end=" ")
                print("-->", end=" ")

                frame_accepted = Receiver.receive_packet(noise_frame)
                #time.sleep(0.1)
                number_of_shipments += 1

            Transmitter.number_of_all_shipments.append(number_of_shipments)



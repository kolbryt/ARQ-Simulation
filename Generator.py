from random import randint, choice
from Coder import Coder


class Generator:

    NUMBER_OF_BITS_IN_MESSAGE = 500
    NUMBER_OF_BITS_IN_PACKET = 10

    message = []

    @staticmethod
    def set_number_of_bits_in_message(number_of_bits_in_message):
        Generator.number_of_bits_in_message = number_of_bits_in_message

    @staticmethod
    def make_message():
        bits = []
        for x in range(Generator.NUMBER_OF_BITS_IN_MESSAGE):
            bits.append(randint(0, 1))

        Generator.read_message(bits)
        Coder.message_divide(bits)
        Generator.message = bits

    @staticmethod
    def read_message(message):
        print("Message:")
        for i in range(0, len(message)):
            print(message[i], end=" ")
        print()

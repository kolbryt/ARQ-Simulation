from Decoder import Decoder


class Receiver:

    @staticmethod
    def receive_packet(noise_frame):

        if Decoder.decode(noise_frame):
            return True     # frame acepted
        else:
            return False    # send frame again

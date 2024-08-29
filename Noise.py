from random import randint


class Noise:

    probability_of_noise = 10  # from 0 to 1000

    @staticmethod
    def set_probability_of_noise(probability_of_noise):
        Noise.probability_of_noise = probability_of_noise

    @staticmethod
    def make_noise(packet):

        noise_packet = []
        for i in range(0, len(packet)):
            chance = randint(1, 1000)
            if chance <= Noise.probability_of_noise:
                if packet[i] == 0:
                    noise_packet.append(1)
                else:
                    noise_packet.append(0)
            else:
                noise_packet.append(packet[i])
        return noise_packet

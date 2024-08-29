from Destination import Destination
import collections


class Decoder:

    @staticmethod
    def decode(noise_frame):
        if noise_frame[0] == 0 and noise_frame[1] == 0 and noise_frame[2] == 0:
            return Decoder.decode_parity_bit(Decoder.decapsulate_frame(noise_frame))
        elif noise_frame[0] == 0 and noise_frame[1] == 0 and noise_frame[2] == 1:
            print()
            return False
        elif noise_frame[0] == 0 and noise_frame[1] == 1 and noise_frame[2] == 0:
            return Decoder.code_repetition_code(Decoder.decapsulate_frame(noise_frame))
        elif noise_frame[0] == 0 and noise_frame[1] == 1 and noise_frame[2] == 1:
            return Decoder.code_2_from_k(Decoder.decapsulate_frame(noise_frame))
        else:
            print("Frame doesn't accepted (wrong code type)")
            return False  # code type has been corrupted

    @staticmethod
    def decapsulate_frame(noised_frame):
        noised_packet = []
        for i in range(3, len(noised_frame)):
            noised_packet.append(noised_frame[i])
        return noised_packet

    @staticmethod
    def decapsulate_parity_bit(noised_packet):
        noised_segment = []
        for i in range(0, len(noised_packet) - 1):
            noised_segment.append(noised_packet[i])
        return noised_segment

    @staticmethod
    def decapsulate_repetition_code_packet(noised_packet):
        noised_segment = []
        for i in range(0, len(noised_packet)):
            if i % 3 == 0:
                noised_segment.append(noised_packet[i])
        return noised_segment

    @staticmethod
    def decode_parity_bit(noised_packet):
        print("Parity bit -->")

        if len(noised_packet) < 2:
            print("Frame was not accepted (length < 2)")
            return False

        sum = 0
        for i in range(0, len(noised_packet) - 1):  # avoiding additional bit
            sum += noised_packet[i] % 2

        if (sum % 2) == noised_packet[len(noised_packet) - 1]:
            print("Frame accepted")
            Destination.add_frame(Decoder.decapsulate_parity_bit(noised_packet))
            return True
        else:
            print("Frame doesn't accepted (code doesn't match)")
            return False  # packet has been corrupted

    @staticmethod
    def code_crc_32(noised_packet, polynomial_bitstring):
        print("Decode code_crc_32 in progress")
        packet_len = len(noised_packet)
        check_value = []
        packet = []
        for i in range(packet_len-33):
            packet.append(noised_packet[i])
        for i in range(33):
            check_value.append(len(noised_packet-(33-i)))
        polynomial_bitstring = polynomial_bitstring.lstrip('0')
        len_input = len(packet)
        initial_padding = check_value
        input_padded_array = list(packet + initial_padding)
        while '1' in input_padded_array[:len_input]:
            cur_shift = input_padded_array.index('1')
            for i in range(len(polynomial_bitstring)):
                input_padded_array[cur_shift + i] \
                    = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
        status = ('1' not in ''.join(input_padded_array)[len_input:])
        if status == True:
            print("Frame accepted")
            Destination.add_frame(packet)
            return True
        else:
            print("Frame doesn't accepted (code doesn't match")
            return False

    @staticmethod
    def code_repetition_code(noised_packet):
        print("Repetition Code -->")
        if len(noised_packet) % 3 != 0:
            print("Frame was not accepted (length % 3 != 0)")
            return False

        status = True
        for index, element in enumerate(noised_packet):
            if index % 3 == 0:
                if noised_packet[index] == noised_packet[index + 1] and noised_packet[index] == noised_packet[index + 2]:
                    x = "Ala ma kota"
                else:
                    status = False

        if status == False:
            print("Frame was not accepted (code doesn't match)")
            return False
        else:
            print("Frame accepted")
            Destination.add_frame(Decoder.decapsulate_repetition_code_packet(noised_packet))
            return True

    @staticmethod
    def code_2_from_k(noised_packet):
        print("2 from k -->")

        if len(noised_packet) % 5 != 0:
            print("Frame was not accepted (length % 5 != 0)")
            return False

        zero = [1, 1, 0, 0, 0]
        one = [1, 0, 1, 0, 0]
        decoded_packet = []

        #    11000 10100 11000  -noised_packet
        #      |
        #  coded_bit
        #          0 1 0        -decoded_packet
        #          |
        #      decoded_bit

        number_of_coded_bits = int(len(noised_packet) / 5)
        noised_packet_index = 0
        for i in range(0, number_of_coded_bits):
            coded_bit = []
            for j in range(5):
                coded_bit.append(noised_packet[noised_packet_index])
                noised_packet_index += 1
            if coded_bit == [1, 1, 0, 0, 0] or coded_bit == [1, 0, 1, 0, 0]:
                if coded_bit == zero:
                    decoded_packet.append(0)
                elif coded_bit == one:
                    decoded_packet.append(1)
            else:
                print("Frame was not accepted (code doesn't match)")
                return False

        print("Frame accepted")
        Destination.add_frame(decoded_packet)
        return True

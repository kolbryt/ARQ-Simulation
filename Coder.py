from Transmitter import Transmitter


class Coder:

    code_choice = [0, 0, 0]
    number_of_bits_in_packet = 3
    segments_x = []
    segments = []
    packets = []

    @staticmethod
    def set_code_choice(code_choice):
        if code_choice == 1:
            Coder.code_choice = [0, 0, 0]
        if code_choice == 2:
            Coder.code_choice = [0, 0, 1]
        if code_choice == 3:
            Coder.code_choice = [0, 1, 0]
        if code_choice == 4:
            Coder.code_choice = [0, 1, 1]

    @staticmethod
    def set_number_of_bits_in_packet(number_of_bits_in_packet):
        Coder.number_of_bits_in_packet = number_of_bits_in_packet

    @staticmethod
    def code_parity_bit(divided_message):

        for i in range(0, len(divided_message)):
            sum_of_bits = 0
            segment = divided_message[i]
            for j in range(0, len(segment)):
                sum_of_bits += segment[j] % 2

            if sum_of_bits % 2 == 0:
                divided_message[i].append(0)
            else:
                divided_message[i].append(1)

        packets = []
        for i in range(0, len(divided_message)):
            segment = divided_message[i]
            packet = []
            packet.append(0)
            packet.append(0)
            packet.append(0)
            for j in range(0, len(segment)):
                packet.append(segment[j])
            packets.append(packet)

        Coder.read_coded_message(packets)
        Transmitter.send_message(packets)
        Coder.packets = packets

    @staticmethod
    def code_crc_32(divided_message, polynomial_bitstring, initial_filler):
        print("code_crc_32 in progress")
        polynomial_bitstring = polynomial_bitstring.lstrip('0')
        len_input = len(divided_message)
        initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
        input_padded_array = list(divided_message + initial_padding)
        while '1' in input_padded_array[:len_input]:
            cur_shift = input_padded_array.index('1')
            for i in range(len(polynomial_bitstring)):
                input_padded_array[cur_shift + i] \
                    = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
        packets = divided_message + ''.join(input_padded_array)[len_input:]

        Coder.read_coded_message(packets)
        Transmitter.send_message(packets)
        Coder.packets = packets


    @staticmethod
    def code_repetition_code(divided_message):
        packets = []
        for i in range(0, len(divided_message)):
            segment = divided_message[i]
            new_segment = [0, 1, 0]
            for j in range(0, len(segment)):
                new_segment.append(segment[j])
                new_segment.append(segment[j])
                new_segment.append(segment[j])
            packets.append(new_segment)

        Coder.read_coded_message(packets)
        Transmitter.send_message(packets)
        Coder.packets = packets

    @staticmethod
    def code_2_from_k(divided_message):

        """
                010111011

                010 - segment
                111
                011

                010 1 - packet
                111 1
                011 0

                000 010 1 - ram

                0 -> 11000
                1 -> 10100
        """

        packets = []
        for i in range(0, len(divided_message)):
            segment = divided_message[i]
            packet = []
            packet.append(0)
            packet.append(1)
            packet.append(1)
            for j in range(0, len(segment)):
                if segment[j] == 0:
                    packet.append(1)
                    packet.append(1)
                    packet.append(0)
                    packet.append(0)
                    packet.append(0)
                if segment[j] == 1:
                    packet.append(1)
                    packet.append(0)
                    packet.append(1)
                    packet.append(0)
                    packet.append(0)
            packets.append(packet)

        Coder.read_coded_message(packets)
        Transmitter.send_message(packets)
        Coder.packets = packets


    @staticmethod
    def choose_code_type(segments):
        if Coder.code_choice[0] == 0 and Coder.code_choice[1] == 0 and Coder.code_choice[2] == 0:
            Coder.code_parity_bit(segments)
        if Coder.code_choice[0] == 0 and Coder.code_choice[1] == 0 and Coder.code_choice[2] == 1:
            Coder.code_crc_32(segments, '101101010101010101010101010101010', '0')
        if Coder.code_choice[0] == 0 and Coder.code_choice[1] == 1 and Coder.code_choice[2] == 0:
            Coder.code_repetition_code(segments)
        if Coder.code_choice[0] == 0 and Coder.code_choice[1] == 1 and Coder.code_choice[2] == 1:
            Coder.code_2_from_k(segments)

    @staticmethod
    def message_divide(message):

        number_of_segments = len(message)//Coder.number_of_bits_in_packet 
        segments = []
        x = 0
        for i in range(0, number_of_segments):
            segment = []
            for j in range(0, Coder.number_of_bits_in_packet):
                segment.append(message[x])
                x += 1
            segments.append(segment)

        Coder.read_divided_message(segments)
        Coder.segments = segments[:]
        Coder.segments_x = segments[:]
        Coder.choose_code_type(segments)

    @staticmethod
    def read_coded_message(coded_message):
        print("Coded message:")
        for i in range(0, len(coded_message)):
            for j in range(0, len(coded_message[i])):
                print(coded_message[i][j], end=" ")
            print()

    @staticmethod
    def read_divided_message(segments):
        print("Divided message:")
        for i in range(0, len(segments)):
            for j in range(0, len(segments[i])):
                print(segments[i][j], end=" ")
            print()

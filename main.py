from Generator import Generator
from Coder import Coder
from Transmitter import Transmitter
from Noise import Noise
from Destination import Destination
import csv

NUMBER_OF_BITS_IN_MESSAGE = 500
NUMBER_OF_BITS_IN_PACKET = 10
PROBABILITY_OF_NOISE = 10 # from 0 to 1000
NUMBER_OF_REPETITIONS = 250

Generator.set_number_of_bits_in_message(NUMBER_OF_BITS_IN_MESSAGE)
Coder.set_number_of_bits_in_packet(NUMBER_OF_BITS_IN_PACKET)
Noise.set_probability_of_noise(PROBABILITY_OF_NOISE)

git = 0
niegit = 0
wsumie = 0
powtorzen = 0

print("Select encoding method:") 
print("1. Parity bit:")
print("2. CRC 32:")
print("3. Repeat code:")
print("4. Code 3 from k:")

user_code_choice = input("Give me a number: ")
Coder.set_code_choice(int(user_code_choice))

for i in range(1):
    for x in range(NUMBER_OF_REPETITIONS):
        git = 0
        niegit = 0
        wsumie = 0
        powtorzen = 0

        Destination.clear_message()
        Generator.make_message()
        Destination.read_message()

        print("Summary:")

        print("Source message: ", end=" ")
        generator_message = Generator.message
        for i in range(0, len(generator_message)):
            print(generator_message[i], end=" ")
        print()

        print("Output message: ", end=" ")
        destination_message = Destination.message
        for i in range(0, len(destination_message)):
            for j in range(0, len(destination_message[i])):
                print(destination_message[i][j], end=" ")
        print()

        # Count how many segments sent without any distortions
        source_message = Generator.message
        counter = 0
        source_message_segments = []
        segment = []
        for i in range(0, len(source_message)):
            segment.append(source_message[i])
            counter += 1
            if counter == NUMBER_OF_BITS_IN_PACKET:
                source_message_segments.append(segment)
                segment = []
                counter1 = counter
                counter = 0

        number_of_similar_packets = 0;
        for i in range(0, len(source_message_segments)):
            if destination_message[i] == source_message_segments[i]:
                number_of_similar_packets += 1
        print("Segments sent without any mistakes: " + str(number_of_similar_packets))
        iter_number = []
        iter_number.append(number_of_similar_packets)
        number_of_all_shipments = Transmitter.number_of_all_shipments
        print("Number of each packet shipments: ")
        for i in range(0, len(number_of_all_shipments)):
            print(str(i + 1) + ".\t" + str(number_of_all_shipments[i]))
            if number_of_all_shipments[i] == 1:
                git += 1
                wsumie += 1
            else:
                niegit += 1
                powtorzen += number_of_all_shipments[i] - 1
                wsumie += 1

        with open('numbers.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([int(NUMBER_OF_BITS_IN_MESSAGE / NUMBER_OF_BITS_IN_PACKET), number_of_similar_packets, int((NUMBER_OF_BITS_IN_MESSAGE / NUMBER_OF_BITS_IN_PACKET) - number_of_similar_packets), powtorzen])
        Transmitter.clear_number_of_all_shipments()

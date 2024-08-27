# ARQ-Simulation

ARQ (Automatic Repeat ReQuest) - We conducted a system analysis in terms of the relationship between the number of erroneous packets and the probability of corruption and the length of packets.

Algorithms used:
- Parity bit - we add to the packet a bit calculated by summing the "ones" in this packet and calculating modulo 2 from this sum.
- Repetition code - we add its duplicate to each bit in the packet. The decoder checks whether the received bits are equal in pairs.
- Code 3 of k - each bit is encoded using n bits. The decoder checks whether the "zeros" and "ones" in each sequence of k output bits are in the ratio 3/k.

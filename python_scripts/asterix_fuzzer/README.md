# Asterix protocol fuzzer program


*ASTERIX is a standard for the exchange of air traffic services (ATS) information. It is developed and maintained by the European ATS organization Eurocontrol (https://en.wikipedia.org/wiki/ASTERIX_(ATC_standard)).*

----------------------------------------------------

## Installation

*pip install scapy*

----------------------------------------------------

## Execution

- Capture an Asterix packet with type *48* using Wireshark, TCPdump, scapy...

- Get the raw value of the packet.

- Find the position of the bytes with the *theta* (angle) and *rho* (distance) values.

- Execute the send_udp.py script:

*python send_udp.py $RAW_PACKET $FIRST_INDEX $LAST_INDEX*

----------------------------------------------------

## Examples 

Fuzzing *theta* and *phi* values (bytes from 22 to 29):

*python send_udp.py 300017fede204820004980*ρρρρ*40000*θθθθ*3e8e00006be 22 29*


"Replay" attack (re-send the same packet in a loop):

*python loop.py 300017fede20409b7e49805a0046000fff03e8e00007bf*

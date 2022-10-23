from scapy.all import *
from random import randint

# Hoofdletters hebben een ASCII code van onder de 100, (65-90) en "normale" letters van 97 tot en met
# 122. Door alleen hoofdletters te gebruiken is elke 2 cijfers 1 letter. Deze consistentie maakt het
# makkelijker voor de andere groep.
# Deze tekst geeft 81 pakketjes


def get_uppercase_list():
    secretlists = list("Bitcoin is a decentralized digital currency that can be transferred on the peer-to-peer "
                       "bitcoin network. Bitcoin transactions are verified by network nodes through cryptography "
                       "and recorded in a public distributed ledger called a blockchain. Kavel Nummer 7A65726E696B657"
                       "06C65696E203131. Biedprijs is 775.000 euro. ")
    secretlist = [elem.upper() for elem in secretlists]
    return secretlist


# Deze functie veranderd de letters in de correcte ASCII code
def get_decimal_list(secretlist):
    decimallist = []
    for x in range(len(secretlist)):
        decimallist.append(ord(secretlist[x]))
    return decimallist


# De maximum value van een TCP sequence number is 4,294,967,295. Omdat de ASCII waarde boven de 42 komt
# gebruiken we alleen de laatste 8 cijfers, waardoor er 4 letters per sequence nummer verstopt zijn.
def get_sequencenumber_list(decimallist):
    var = ''
    x = 0
    c = ['420', '69', '360']  # Begin met 420, 69 & 360 als Sequence number als hint
    for element in decimallist:
        var += str(element)
        x += 1
        if x == 4:  # Bij 4 letters, voeg toe aan de list en begin aan een nieuwe TCP nummer.
            c.append(var)
            var = ''
            x = 0
    """Zie het aantal pakketjes dat verzonden worden en de inhoud:"""
    print(len(c), c)
    return c


# Verstuur de TCP frames met de nieuwe Sequence numbers
def packet_with_seq_n(c):
    sportnum = 50000
    # Loop door de port numbers als hint dat er is gekloot met de TCP frame, beginnend bij 50000

    # MTU van Ethernet is 1500 Bytes, -20 voor IPV4 & -20 voor TCP Header geeft 1460 Bytes aan data
    # 1 Letter is 8 Bytes, dus in de packet kunnen we 1480 / 8 = 182.5 = 182 letters doen die verschijnen in wireshark
    # als het pakketje door iemand wordt bekeken. Voor nu staat er alleen de tekst: Wat zou er in deze pakketjes zitten?
    # Time.sleep staat er zodat de pakketjes iets minder opvallen, forceert de andere groep om te filteren
    for x in c:
        a = int(x)
        time.sleep(randint(1, 4))
        packet = IP(dst="192.168.100.123", src="192.168.100.144")/TCP(sport=sportnum, dport=222, seq=a)/"Wat zou er in deze pakketjes zitten?"
        sportnum += 1
        send(packet)


def main():
    secretlist = get_uppercase_list()
    decimallist = get_decimal_list(secretlist)
    c = get_sequencenumber_list(decimallist)
    packet_with_seq_n(c)


if __name__ == "__main__":
    main()

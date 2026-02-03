from scapy.all import sniff

def capture_packets(callback, count=10):
    sniff(prn=callback, count=count)

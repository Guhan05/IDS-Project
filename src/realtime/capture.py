from scapy.all import sniff
import numpy as np

def extract_features(pkt):
    """
    Simple demo features (you can expand later)
    """
    length = len(pkt)
    proto = 1 if pkt.haslayer("TCP") else 0
    return np.array([length, proto])


def capture_packets(callback):
    """
    Captures live packets and sends features to callback
    """

    def process(pkt):
        features = extract_features(pkt)
        callback(features)

    sniff(prn=process, store=False)

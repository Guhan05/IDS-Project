import numpy as np

EXPECTED_FEATURES = 77   # must match training


def extract_features(packet):

    basic = [
        len(packet),
        packet.time % 1000,
        packet.proto if hasattr(packet, "proto") else 0
    ]

    # pad remaining with zeros
    padded = basic + [0] * (EXPECTED_FEATURES - len(basic))

    return np.array(padded, dtype=float)

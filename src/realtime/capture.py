from scapy.all import sniff, IP


def capture_packets(callback):

    def handle(pkt):
        if IP not in pkt:
            return

        src = pkt[IP].src
        dst = pkt[IP].dst
        proto = pkt[IP].proto

        # simple dummy features (replace with your extractor)
        features = [len(pkt)]

        callback(features, src, dst, proto)

    sniff(prn=handle, store=False)

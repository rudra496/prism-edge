"""
PRISM-Edge: Resilient Mesh Networking Subsystem
Offline-first gossip sync, opportunistic store-and-forward bundle routing,
and ultra-compact Base91-encoded binary payload compression for SMS/USSD fallback.
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Set

# Base91 character set definition without escaping issues
BASE91_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~" + '"'

def base91_encode(bindata: bytes) -> str:
    b = 0
    n = 0
    out = []
    for byte in bindata:
        b |= byte << n
        n += 8
        if n > 13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            out.append(BASE91_CHARS[v % 91] + BASE91_CHARS[v // 91])
    if n:
        out.append(BASE91_CHARS[b % 91])
        if n > 7 or b > 90:
            out.append(BASE91_CHARS[b // 91])
    return "".join(out)

def base91_decode(encoded_str: str) -> bytes:
    v = -1
    b = 0
    n = 0
    out = bytearray()
    for char in encoded_str:
        if char not in BASE91_CHARS:
            continue
        c = BASE91_CHARS.index(char)
        if v < 0:
            v = c
        else:
            v += c * 91
            b |= v << n
            n += 13 if (v & 8191) > 88 else 14
            while True:
                out.append(b & 255)
                b >>= 8
                n -= 8
                if not (n > 7):
                    break
            v = -1
    if v + 1:
        out.append((b | v << n) & 255)
    return bytes(out)

class MeshPacket:
    """Represents a store-and-forward multi-hop opportunistic bundle."""
    def __init__(self, sender_id: str, recipient_id: str, payload_type: str, payload_data: Dict[str, Any], ttl_hops: int = 7):
        self.packet_id: str = hashlib.sha256(f"{sender_id}:{recipient_id}:{time.time()}".encode()).hexdigest()[:16]
        self.sender_id: str = sender_id
        self.recipient_id: str = recipient_id
        self.payload_type: str = payload_type # HEALTH, CLIMATE, SOS, UPSKILL, SYNC
        self.payload_data: Dict[str, Any] = payload_data
        self.ttl_hops: int = ttl_hops
        self.timestamp: float = time.time()
        self.hop_trail: List[str] = [sender_id]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "payload_type": self.payload_type,
            "payload_data": self.payload_data,
            "ttl_hops": self.ttl_hops,
            "timestamp": self.timestamp,
            "hop_trail": self.hop_trail
        }

    def compress_for_sms(self) -> str:
        """Serializes and compresses the packet into an SMS-safe Base91 payload."""
        raw_json = json.dumps(self.to_dict()).encode("utf-8")
        return "PRISM:" + base91_encode(raw_json)

    @classmethod
    def decompress_from_sms(cls, sms_text: str) -> Optional['MeshPacket']:
        if not sms_text.startswith("PRISM:"):
            return None
        encoded_part = sms_text[6:]
        try:
            raw_bytes = base91_decode(encoded_part)
            data = json.loads(raw_bytes.decode("utf-8"))
            pkt = cls(
                sender_id=data["sender_id"],
                recipient_id=data["recipient_id"],
                payload_type=data["payload_type"],
                payload_data=data["payload_data"],
                ttl_hops=data["ttl_hops"]
            )
            pkt.packet_id = data["packet_id"]
            pkt.timestamp = data["timestamp"]
            pkt.hop_trail = data["hop_trail"]
            return pkt
        except Exception:
            return None

class ResilientMeshRouter:
    """
    Manages local packet queues, anti-entropy gossip synchronization,
    and opportunistic multi-hop forwarding across neighbor edge nodes.
    """
    def __init__(self, node_id: str):
        self.node_id: str = node_id
        self.packet_buffer: Dict[str, MeshPacket] = {}
        self.seen_packet_ids: Set[str] = set()
        self.neighbors: Set[str] = set()

    def discover_neighbor(self, neighbor_node_id: str) -> None:
        if neighbor_node_id != self.node_id:
            self.neighbors.add(neighbor_node_id)

    def ingest_packet(self, packet: MeshPacket) -> bool:
        if packet.packet_id in self.seen_packet_ids:
            return False # Duplicate suppression

        self.seen_packet_ids.add(packet.packet_id)

        if packet.recipient_id == self.node_id or packet.recipient_id == "BROADCAST":
            self.packet_buffer[packet.packet_id] = packet
            return True

        if packet.ttl_hops > 0:
            packet.ttl_hops -= 1
            packet.hop_trail.append(self.node_id)
            self.packet_buffer[packet.packet_id] = packet
            return True

        return False

    def gossip_sync_exchange(self, peer_router: 'ResilientMeshRouter') -> int:
        """Simulates P2P WiFi Direct / Bluetooth LE opportunistic bundle synchronization."""
        forwarded_count = 0
        self.discover_neighbor(peer_router.node_id)
        peer_router.discover_neighbor(self.node_id)

        for pkt_id, packet in list(self.packet_buffer.items()):
            if pkt_id not in peer_router.seen_packet_ids:
                success = peer_router.ingest_packet(packet)
                if success:
                    forwarded_count += 1

        return forwarded_count

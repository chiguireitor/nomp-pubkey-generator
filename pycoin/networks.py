from collections import namedtuple

from .serialize import h2b
from hashlib import sha256
#from .otros.groestl import groestl
from .otros.blake8 import BLAKE

def groestl512(data):
    return groestl(512, data)
    
def blake256(data):
    bl = BLAKE(256)
    bl.update(data)
    return bl
    
fnbl = blake256
fnbl.no_double = True
fnbl.ripe_hash = sha256
    
def hefty1(data):
    raise Exception("Hefty1 not implemented")

NetworkValues = namedtuple('NetworkValues',
                           ('network_name', 'subnet_name', 'code', 'wif_prefix', 'address_prefix',
                            'pay_to_script_prefix', 'bip32_priv_prefix', 'bip32_pub_prefix', 'alternate_hash'))

NETWORKS = (
    NetworkValues("Bitcoin", "mainnet", "BTC", b'\x80', b'\0', b'\5', h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Bitcoin", "testnet3", "XTN", b'\xef', b'\x6f', b'\xc4',
                  h2b("04358394"), h2b("043587CF"), sha256),
    NetworkValues("Litecoin", "mainnet", "LTC", b'\xb0', b'\x30', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Dogecoin", "mainnet", "DOGE", b'\x9e', b'\x1e', b'\x16',
                  h2b("02fda4e8"), h2b("02fda923"), sha256),
    # BlackCoin: unsure about bip32 prefixes; assuming will use Bitcoin's
    NetworkValues("Blackcoin", "mainnet", "BLK", b'\x99', b'\x19', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    
    NetworkValues("Skeincoin", "mainnet", "SKC", b'\xE2', b'\x3F', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Skeincoin", "testnet", "TSKC", b'\xED', b'\x38', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    
    NetworkValues("Slimcoin", "mainnet", "SLM", b'\xBF', b'\x3F', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Carpediemcoin", "mainnet", "DIEM", b'\x9E', b'\x1E', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Kashmircoin", "mainnet", "KSC", b'\xAE', b'\x2E', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Myriadcoin", "mainnet", "MYR", b'\xB2', b'\x32', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("GOODcoin", "mainnet", "GOOD", b'\xA6', b'\x26', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("LimecoinX", "mainnet", "LIMX", b'\xE6', b'\x66', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Bellscoin", "mainnet", "BEL", b'\x99', b'\x19', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Denarius", "mainnet", "DRS", b'\x8B', b'\x0B', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("DigiByte", "mainnet", "DGB", b'\x80', b'\x1E', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("ECCoin", "mainnet", "ECC", b'\xA1', b'\x21', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Hawaiicoin", "mainnet", "HIC", b'\x80', b'\0', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("HeisenbergHex", "mainnet", "HEX", b'\xC2', b'\x42', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Legendarycoin", "mainnet", "LGD", b'\xB0', b'\x30', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    #NetworkValues("Groestlcoin", "mainnet", "GRS", b'\x80', b'\x24', None, h2b("0488ADE4"), h2b("0488B21E"), groestl512),
    NetworkValues("Lovecoin", "mainnet", "LOVE", b'\xB0', b'\x30', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Mincoin", "mainnet", "MIN", b'\xB2', b'\x32', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Vertcoin", "mainnet", "VTC", b'\xC7', b'\x47', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Worldcoin", "mainnet", "WDC", b'\xC9', b'\x49', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Feathercoin", "mainnet", "FTC", b'\x8E', b'\x0E', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Neutrino", "mainnet", "NTR", b'\xB5', b'\x35', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Darkcoin", "mainnet", "DRK", b'\xCC', b'\x4C', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Quark", "mainnet", "QRK", b'\xBA', b'\x3A', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("BitShares-PTS", "mainnet", "PTS", b'\xB8', b'\x38', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Peercoin", "mainnet", "PPC", b'\xB7', b'\x37', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Primecoin", "mainnet", "XPM", b'\x97', b'\x17', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Megacoin", "mainnet", "MEC", b'\xB2', b'\x32', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("X11Coin", "mainnet", "XC", b'\xCB', b'\x4B', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Cinnicoin", "mainnet", "CINNI", b'\xAB', b'\x2B', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Zetacoin", "mainnet", "ZET", b'\xE0', b'\x50', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Infinitecoin", "mainnet", "IFC", b'\xE6', b'\x66', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Gridcoin", "mainnet", "GRC", b'\xA5', b'\x25', None, h2b("0488ADE4"), h2b("0488B21E"), sha256),
    NetworkValues("Dirac", "mainnet", "XDQ", b'\x80', b'\x5A', None, h2b("0488ADE4"), h2b("0488B21E"), fnbl),
    NetworkValues("Blakebitcoin", "mainnet", "BBTC", b'\x80', b'\xF3', None, h2b("0488ADE4"), h2b("0488B21E"), fnbl),
    NetworkValues("Blakecoin", "mainnet", "BLC", b'\x80', b'\x1A', None, h2b("0488ADE4"), h2b("0488B21E"), fnbl),
    NetworkValues("Photon", "mainnet", "PHO", b'\x80', b'\x1A', None, h2b("0488ADE4"), h2b("0488B21E"), fnbl),
    NetworkValues("Electron", "mainnet", "ELT", b'\x80', b'\x5C', None, h2b("0488ADE4"), h2b("0488B21E"), fnbl),
    NetworkValues("UniversalMolecule", "mainnet", "UMO", b'\x80', b'\x82', None, h2b("0488ADE4"), h2b("0488B21E"), fnbl),
    
    NetworkValues("Blakecoin", "testnet", "TBLC", b'\xEF', b'\x8E', None, h2b("0488ADE4"), h2b("0488B21E"), fnbl),
    NetworkValues("Photon", "testnet", "TPHO", b'\xEF', b'\x8E', None, h2b("0488ADE4"), h2b("0488B21E"), fnbl),

    
    # These need a patch on bip32.py on the function public_pair_to_bitcoin_address to support different hashing algos and hash160 on encoding.py
    NetworkValues("Heavycoin", "mainnet", "HVC", b'\x80', b'\x28', None, h2b("0488ADE4"), h2b("0488B21E"), hefty1), # Not working
    
)

# Map from short code to details about that network.
NETWORK_NAME_LOOKUP = dict((i.code, i) for i in NETWORKS)

# All network names, return in same order as list above: for UI purposes.
NETWORK_NAMES = [i.code for i in NETWORKS]


def _lookup(netcode, property):
    # Lookup a specific value needed for a specific network
    network = NETWORK_NAME_LOOKUP.get(netcode)
    if network:
        return getattr(network, property)
    return None


def network_name_for_netcode(netcode):
    return _lookup(netcode, "network_name")


def subnet_name_for_netcode(netcode):
    return _lookup(netcode, "subnet_name")


def full_network_name_for_netcode(netcode):
    network = NETWORK_NAME_LOOKUP[netcode]
    if network:
        return "%s %s" % (network.network_name, network.subnet_name)


def wif_prefix_for_netcode(netcode):
    return _lookup(netcode, "wif_prefix")


def address_prefix_for_netcode(netcode):
    return _lookup(netcode, "address_prefix")


def pay_to_script_prefix_for_netcode(netcode):
    return _lookup(netcode, "pay_to_script_prefix")


def prv32_prefix_for_netcode(netcode):
    return _lookup(netcode, "bip32_priv_prefix")
    
def alternate_hash_for_netcode(netcode):
    return _lookup(netcode, "alternate_hash")

def pub32_prefix_for_netcode(netcode):
    return _lookup(netcode, "bip32_pub_prefix")

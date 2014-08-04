#!/usr/bin/python
import os
from pycoin.key.bip32 import Wallet
from pycoin.encoding import public_pair_to_hash160_sec, hash160_sec_to_bitcoin_address
from pycoin.networks import address_prefix_for_netcode, alternate_hash_for_netcode

secret = os.urandom(64)
wallet = Wallet.from_master_secret(bytes(secret), 'BTC')

sec = public_pair_to_hash160_sec(wallet.public_pair)
pubkey = ''.join('{:02x}'.format(ord(x)) for x in sec)

addr_blc = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('BLC'), internal_hash=alternate_hash_for_netcode('BLC'))
#addr_blc_test = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('TBLC'), internal_hash=alternate_hash_for_netcode('TBLC'))
addr_pho = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('PHO'), internal_hash=alternate_hash_for_netcode('PHO'))
#addr_pho_test = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('TPHO'), internal_hash=alternate_hash_for_netcode('TPHO'))
addr_bbtc = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('BBTC'), internal_hash=alternate_hash_for_netcode('BBTC'))
addr_xdq = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('XDQ'), internal_hash=alternate_hash_for_netcode('XDQ'))
addr_elt = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('ELT'), internal_hash=alternate_hash_for_netcode('ELT'))
addr_umo = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('UMO'), internal_hash=alternate_hash_for_netcode('UMO'))

wallet.netcode = 'BLC'

wif = wallet.wif()

import_command = "importprivkey %s MERGED_NOMP_REWARD false" % wif

print("Your public key is\n\n%s\n" % pubkey)
print("Use it as your username on the NOMP pool.\n\n")
print("To import the address to your wallet, use the following command on")
print("Help > Debug window > Console in each wallet of the Blake family:\n")
print(import_command)
print("\nYour addresses should be:\n")
print("Blakecoin:\t\t%s" % addr_blc)
#print("Blakecoin Testnet:\t%s" % addr_blc_test)
print("Photon:\t\t\t%s" % addr_pho)
#print("Photon Testnet:\t\t%s" % addr_pho_test)
print("Blakebitcoin:\t\t%s" % addr_bbtc)
print("Dirac:\t\t\t%s" % addr_xdq)
print("Electron:\t\t%s" % addr_elt)
print("UniversalMolecule:\t%s\n" % addr_umo)
print("If you don't import your pubkey on a given wallet, you can retrieve")
print("it later from a working wallet using dumpprivkey on the debug console.\n\n")
raw_input("Press Enter to close...")

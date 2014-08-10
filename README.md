Easy NOMP Pubkey generator
=====================

Pubkey generator for NOMP pools, to anonymously mine in merged pools.

Just run gen_pubkey_nomp.py with Python 2.7 and follow the instructions on the console.

Generates addresses for:

 * Blakecoin
 * Photon
 * Electron
 * Dirac
 * BlakeBitcoin
 * UniversalMolecule
 
You can download the binary package to run this utility with a (rather horrible) GUI that has an option to autoconfigure your wallets and includes all the requirements so you don't have to install Python.
 
Troubleshooting
-------------

Q. The wallet address doesn't appear after importing the wallet key. What happened?
A. After importing the private key into your wallet, it happens sometimes that the address doesn't appear on the receive list. Although it doesn't appear, the wallet is already registered, importnig again the key will throw an error but will make the address appear on the list.
 
Includes a modified version of Pycoin that allows (rather partial) usage with a lot of altcoins.
 
Enjoy!

#!/usr/bin/python
import os

from pycoin.key.bip32 import Wallet
from pycoin.encoding import public_pair_to_hash160_sec, hash160_sec_to_bitcoin_address
from pycoin.networks import address_prefix_for_netcode, alternate_hash_for_netcode
from binascii import hexlify
import bitcoinrpc
import socket

secret = os.urandom(64)
wallet = Wallet.from_master_secret(bytes(secret), 'BLC')

sec = public_pair_to_hash160_sec(wallet.public_pair)
pubkey = ''.join('{:02x}'.format(ord(x)) for x in sec)

addr_blc = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('BLC'), internal_hash=alternate_hash_for_netcode('BLC'))
addr_pho = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('PHO'), internal_hash=alternate_hash_for_netcode('PHO'))
addr_bbtc = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('BBTC'), internal_hash=alternate_hash_for_netcode('BBTC'))
addr_xdq = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('XDQ'), internal_hash=alternate_hash_for_netcode('XDQ'))
addr_elt = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('ELT'), internal_hash=alternate_hash_for_netcode('ELT'))
addr_umo = hash160_sec_to_bitcoin_address(sec, address_prefix=address_prefix_for_netcode('UMO'), internal_hash=alternate_hash_for_netcode('UMO'))

addresses = {
    'blakecoin': addr_blc,
    'photon': addr_pho,
    'blakebitcoin': addr_bbtc,
    'dirac': addr_xdq,
    'electron': addr_elt,
    'universalmolecule': addr_umo
}

wallet.netcode = 'BLC'

wif = wallet.wif()

import_command = "importprivkey %s MERGED_NOMP_REWARD_USR_%s false" % (wif, pubkey)

############ Done calculating all the data, now show it

import platform

systm = platform.system()

if systm == "Windows":
    home = os.getenv('APPDATA')
elif (systm == "Linux") or (systm == "Darwin"):
    from os.path import expanduser
    home = expanduser("~")
else:
    raise Exception("System not supported: %s" % systm)

supported_wallets = ["blakecoin", 
    "blakebitcoin", "photon", 
    "dirac", "electron", 
    "universalmolecule"]
    
default_rpcport = {
    "blakecoin": 8332,
    "blakebitcoin": 1812,
    "photon": 18998,
    "dirac": 42024,
    "electron": 16852,
    "universalmolecule": 18779 
}

wallets_data = {}    
for wallet_name in supported_wallets:
    try:
        with open(os.sep.join([home, wallet_name, "%s.conf" % wallet_name]), "r") as f:
            data = f.read()
        usr = ""
        pwd = ""
        port = ""
        has_allow_ip = False
        has_listen = False
        has_server = False
        for line in data.split("\n"):
            try:
                key, value = line.split("=")
                if key == "rpcuser":
                    usr = value
                elif key == "rpcpassword":
                    pwd = value
                elif key == "rpcport":
                    port = value
                elif key == "rpcallowip":
                    has_allow_ip = True
                elif key == "listen":
                    has_listen = True
                elif key == "server":
                    has_server = True
            except ValueError:
                print("Error unpacking line: %s\nOn wallet %s" % (line, wallet_name))

        if usr and pwd and port and has_allow_ip and has_listen and has_server:
            wallets_data[wallet_name] = {
                    "rpcuser": usr,
                    "rpcpassword": pwd,
                    "rpcport": int(port)
                }
        else:
            wallets_data[wallet_name] = {
                "no-rpc-data": True,
                "missing-rpcuser": len(usr) == 0,
                "missing-rpcpassword": len(pwd) == 0,
                "missing-rpcport": len(port) == 0,
                "missing-rpcallowip": not(has_allow_ip),
                "missing-listen": not(has_listen),
                "missing-server": not(has_server),
            }
    except IOError:
        wallets_data[wallet_name] = {"no-conf": True}
        
import wx

privkey_edit = None
can_autoconfigure = False

def verify_cbox(c):
    if c.IsChecked():
        privkey_edit.SetValue(import_command)
        can_autoconfigure = True

def auto_configure(b):
    must_restart_wallets = []
    for wn in wallets_data:
        if 'no-conf' in wallets_data[wn]:
            must_restart_wallets.append(wn)
        elif 'no-rpc-data' in wallets_data[wn]:
            must_restart_wallets.append(wn)
            
    if len(must_restart_wallets) > 0:
        message_dlg = """The following wallets must be configured for RPC communication:

  * %s

Random RPC passwords will be generated using os.urandom (relatively secure), afterwards, you will need to restart them.

Are you sure you want to proceed?""" % "\n  * ".join(must_restart_wallets)
        
        wallets_configured = len(must_restart_wallets) == 0
        dlg = wx.MessageDialog(None, message=message_dlg, caption="Wallet configuration", style=wx.YES | wx.NO)
        num_config = 0
        if dlg.ShowModal() == wx.ID_YES:
            for wn in must_restart_wallets:
                pwd = hexlify(os.urandom(32))
                conf_base_dir = os.sep.join([home, wn])
                conf_path = os.sep.join([home, wn, "%s.conf" % wn])
                if not os.path.exists(conf_base_dir):
                    os.makedirs(conf_base_dir)
                    
                if 'no-conf' in wallets_data[wn]:
                    with open(conf_path, "w") as f:
                        f.write("""rpcallowip=127.0.0.1
rpcuser=%suser
rpcpassword=%s
rpcport=%i
listen=1
server=1
""" % (wn, pwd, default_rpcport[wn]))
                    del wallets_data[wn]['no-conf']
                    wallets_data[wn]['rpcuser'] = "%suser" % wn
                    wallets_data[wn]['rpcpassword'] = pwd
                    wallets_data[wn]['rpcport'] = default_rpcport[wn]
                    num_config += 1
                elif 'no-rpc-data' in wallets_data[wn]:
                    with open(conf_path, "a") as f:
                        if wallets_data[wn]["missing-rpcuser"]:
                            f.write("\nrpcuser=%user" % wn)
                            wallets_data[wn]['rpcuser'] = "%suser" % wn
                            
                        if wallets_data[wn]["missing-rpcpassword"]:
                            f.write("\nrpcpassword=%s" % pwd)
                            wallets_data[wn]['rpcpassword'] = pwd
                        
                        if wallets_data[wn]["missing-rpcport"]:
                            f.write("\nrpcport=%i" % default_rpcport[wn])
                            wallets_data[wn]['rpcport'] = default_rpcport[wn]
                        
                        if wallets_data[wn]["missing-rpcallowip"]:
                            f.write("\nrpcallowip=127.0.0.1")
                        
                        if wallets_data[wn]["missing-listen"]:
                            f.write("\nlisten=1")
                        
                        if wallets_data[wn]["missing-server"]:
                            f.write("\nserver=1")
                        

                    del wallets_data[wn]['no-rpc-data']
                    num_config += 1
            
            message_dlg = """Now restart the wallets that were just configured:

  * %s
  
Only dismiss this dialog after restarting them.""" % "\n  * ".join(must_restart_wallets)
            wx.MessageDialog(None, message=message_dlg, caption="Restart wallets", style=wx.OK).ShowModal()
        wallets_configured = len(must_restart_wallets) == num_config
            
        proceed_with_config = wallets_configured | (len(must_restart_wallets) == 0)
        if not(wallets_configured):
            message_dlg = """Not all the Blake ecosystem wallets were configured.

Do you want to proceed to configure the available anyways?"""
            proceed_with_config = wx.MessageDialog(None, message=message_dlg, caption="Configure wallets", style=wx.YES | wx.NO).ShowModal() == wx.ID_YES
    else:
        proceed_with_config = True
            
    if proceed_with_config:
        try:
            for wn in wallets_data:
                host = "127.0.0.1"
                
                try:
                    rpcuser = wallets_data[wn]['rpcuser']
                    rpcpassword = wallets_data[wn]['rpcpassword']
                    rpcport = wallets_data[wn]['rpcport']
                    process_wallet = True
                except KeyError:
                    print("Skipping %s" % wn)
                    process_wallet = False
                        
                if process_wallet:
                    try:
                        conn = bitcoinrpc.connect_to_remote(
                            rpcuser, 
                            rpcpassword, 
                            host=host, 
                            port=rpcport)
                            
                        try:
                            #conn.importprivkey(wif, "MERGED_NOMP_REWARD_USR_%s" % pubkey, False)
                            pass
                        finally:
                            del conn
                    except socket.error:
                        print("> Socket error configuring %s" % wn)
                    except bitcoinrpc.exceptions.WalletError:
                        print("> Wallet already has key %s" % wn)
        except Exception, e:
            wx.MessageDialog(None, message="An error ocurred while importing private keys.\n\nHere's the exception message:\n\n%s" % str(e), caption="Exception when configuring wallets", style=wx.OK).ShowModal()
            raise e
            
        wx.MessageDialog(None, message="Now you can begin mining with your pubkey as username!", caption="Pubkey configured succesfully", style=wx.OK).ShowModal()
    else:
        print("Nothing configured")
                    
        
class PubkeyWindow(wx.Frame):
  
    def __init__(self, parent, title):
        super(PubkeyWindow, self).__init__(parent, title=title, 
            size=(850, 600))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        #font.SetPointSize(12)
        
        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        cb = wx.CheckBox(panel, label="By checking this i understand that if i lose the private key, i'm the only person liable to that event.")
        cb.Bind(wx.EVT_CHECKBOX, verify_cbox)
        hbox1.Add(cb, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Pubkey')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel, value=pubkey)
        hbox1.Add(tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        st1 = wx.StaticText(panel, label="The pubkey is your NOMP username, use it on cgminer to receive the profits on your wallets.")
        st1.SetFont(font)
        vbox.Add(st1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Privkey')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel, value="Click on the first checkbox to reveal the privkey")#import_command)
        global privkey_edit
        privkey_edit = tc
        hbox1.Add(tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        st1 = wx.StaticText(panel, label="The privkey needs to be imported on each wallet on Help > Debug Window > Console. Copy and Paste it and press Return.")
        st1.SetFont(font)
        vbox.Add(st1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        line = wx.StaticLine(panel)
        vbox.Add(line, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        st1 = wx.StaticText(panel, label="These addresses are only for reference, if they don't are the same after importing the privkey, there's something wrong.")
        st1.SetFont(font)
        vbox.Add(st1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        hbox_ord = wx.BoxSizer(wx.HORIZONTAL)
        col1 = wx.BoxSizer(wx.VERTICAL)
        hbox_ord.Add(col1, flag=wx.RIGHT, border=8)
        col2 = wx.BoxSizer(wx.VERTICAL)
        hbox_ord.Add(col2, proportion=1, border=8)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.SetMinSize((100, 8))
        st1 = wx.StaticText(panel, label="")
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=10)
        col1.Add(hbox1)
        
        for wn in supported_wallets:
            hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            hbox1.SetMinSize((100, 32))
            st1 = wx.StaticText(panel, label=wn)
            st1.SetFont(font)
            hbox1.Add(st1, flag=wx.RIGHT, border=10)
            col1.Add(hbox1)
            
            hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            tc = wx.TextCtrl(panel, value=addresses[wn])
            tc.SetEditable(False)
            hbox1.Add(tc, proportion=1)
            col2.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
            
            """hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            st1 = wx.StaticText(panel, label=wn)
            st1.SetFont(font)
            hbox1.Add(st1, flag=wx.RIGHT, border=8)
            tc = wx.TextCtrl(panel, value=addresses[wn])
            tc.SetEditable(False)
            hbox1.Add(tc, proportion=1)
            vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)"""
        vbox.Add(hbox_ord, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        line = wx.StaticLine(panel)
        vbox.Add(line, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
            
        st1 = wx.StaticText(panel, label="This GUI is horrendous, i know, luckily you will use it just once, if you use it more than once, sorry ^_^")
        st1.SetFont(font)
        vbox.Add(st1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        button4 = wx.Button(panel, label="Auto-Configure")
        button4.Bind(wx.EVT_BUTTON, auto_configure)
        hbox1.Add(button4, flag=wx.Left, border=8)
        st1 = wx.StaticText(panel, label="Press this to configure all the wallets via JSON-RPC (reads your confs, you gotta trust me it doesn't do anything evil)")
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.Left, border=8)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        vbox.Add((-1, 10))
        
        panel.SetSizer(vbox)
        #wx.TextCtrl(panel, pos=(3, 3), size=(390, 300))

app = wx.App()

PubkeyWindow(None, title='NOMP Pubkey/Privkey Generator')

app.MainLoop()
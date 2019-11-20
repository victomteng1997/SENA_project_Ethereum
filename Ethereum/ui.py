import json
import web3
import subprocess
import shlex
import json
import logging

from web3 import Web3
from web3.auto import w3
from solc import compile_source
from web3.contract import ConciseContract
import tkinter as tk


# A tested version with tkinter as UI when the web UI is not ready. Currently not in use.
def build_contract():
    contract_source_code = '''
    pragma solidity ^0.4.21;
    
    contract StoreVar {
    
        string public _myVar;
        event MyEvent(string _var);
    
        function setVar(string _var) public {
            _myVar = _var;
            MyEvent(_var);
        }
    
        function getVar() public view returns (string) {
            return _myVar;
        }
    
    }
    '''
    compiled_sol = compile_source(contract_source_code) # Compiled source code
    w3.eth.defaultAccount = w3.eth.accounts[0]

    contract_interface = compiled_sol['<stdin>:StoreVar']
    StoreVar = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    tx_hash = StoreVar.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash.hex(),timeout=120000)

    storevar = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_interface['abi'],
    )
    try:
        f = open('contract_address','w')
        f.write(tx_receipt.contractAddress)
        f.close()
        print('Store contract address successful.')
    except Exception as e:
        logging.error('Error at %s', 'division', exc_info=e)
        print('Store contract address failed. For details, please check log file')
        return False

    try:
        with open('contract_abi.json', 'w') as f:
            json.dump(contract_interface['abi'], f)
    except Exception as e:
        logging.error('Error at %s', 'division', exc_info=e)
        print('Store contract abi failed. For details, please check log file')
        return False


def read_contract():
    '''
        Read smart contract in contract_address and contract_abi.
        :return: (address, abi) if exists, (False, False) if error
    '''
    try:
        f_addr = open('contract_address','r')
        addr = f_addr.readlines()[0].strip()
        with open('contract_abi.json') as f:
            abi = json.load(f)
        return(addr,abi)
    except Exception as e:
        logging.error('Error at %s', 'division', exc_info=e)
        print('Read contract addr/abi failed. For details, please check log file')
        return(False,False)
def do_curl(curl_cmd):
    '''
    :param curl_cmd: input cURL command
    :return: (curl_output, curl_status) when curl command receives output or (False, False) when error
    '''
    # Safety check:
    args = shlex.split(curl_cmd)
    if args[0] != 'curl':
        print("None curl detected. Your command and address are recorded in Ethereum System.")
        return (False,False)
    elif '&&' in args:
        print("One command at a time. Aborted. Your command and address are recorded in Ethereum System")
        return (False,False)
    else:
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return (stdout,stderr)

def implement_ethereum(key,var):
    #Firstly check if the key is correct
    #List all accounts:
    implementation_output = ""
    accounts = w3.eth.accounts
    #print(accounts)
    if key not in accounts:
        implementation_output = "Provided key not in existing accounts. Access Denied."
        return implementation_output
    # If Pass
    w3.eth.defaultAccount = w3.eth.accounts[0]
    gas_estimate = storevar.functions.setVar(var).estimateGas()
    #implementation_output += "Gas estimate to transact with setVar: {0}\n".format(gas_estimate)
    #implementation_output += '\n'
    # Wait for the transaction to be mined, and get the transaction receipt
    #tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash.hex(),timeout=120000)
    tx_hash = storevar.functions.setVar(var).transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash.hex())
    #implementation_output += "Transaction receipt mined: \n"
    #implementation_output += str(dict(receipt))
    #implementation_output += '\n'
    implementation_output += "Was transaction successful?"
    implementation_output += str(receipt['status'])
    implementation_output += '\n'
    rich_logs = storevar.events.MyEvent().processReceipt(receipt)
    implementation_output += str(rich_logs)

    #### Then do curl
    output,error = do_curl(var)
    print ("Curl command output:")
    print("########################################\n\n")
    print('output: \n',output)
    print(' ')
    print('error: \n', error)
    print(' ')
    print("########################################\n")
    return implementation_output

def show_entry_fields():
    '''
    for tkinter to show entry fileds, i.e. the UI entries.
    :return:
    '''
    print("Public key: %s\nCommand: %s\nImplementation Result: %s" % (e1.get(), e2.get(), implement_ethereum(str(e1.get()),str(e2.get()))))


if __name__ == "__main__":
    # Try to read contract:
    (addr, abi) = read_contract()
    error_count = 0
    while (addr == False or abi == False) and error_count <=5:
        # Re-initialization
        print("Reading contract error, start re-initialization")
        build_contract()
        error_count += 1
        (addr, abi) = read_contract()
    print("Contract detected.")

    # Load contract
    storevar = w3.eth.contract(
        address=addr,
        abi=abi,
    )

    # Start tk and do proper labels
    master = tk.Tk()
    tk.Label(master,
             text="Public Key").grid(row=0)
    tk.Label(master,
             text="Stored Var").grid(row=1)
    # do tk labels
    e1 = tk.Entry(master)
    e2 = tk.Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    # add tk buttons
    tk.Button(master,
              text='Implement', command=show_entry_fields).grid(row=3,
                                                                column=1,
                                                                sticky=tk.W,
                                                                pady=4)
    # start tk main loop
    tk.mainloop()

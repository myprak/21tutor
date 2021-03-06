## Objective: hash A|B, C|D and then the interior nodes to get the
## merkle root 

## Bitcoin relies on the SHA256 hash function
from hashlib import sha256
from codecs import decode
from binascii import hexlify

## Bitcoin uses the SHA256d hash function, which is the SHA256 function
## run twice (double).
def sha256d(data):
  return sha256(sha256(data).digest()).digest()

## We'll get our data from Bitcoin Core, which displays hashes in RPC
## Byte Order. This converts hex to binary in Internal Byte Order.
def rpc2internal(hash):
  return decode(hash, 'hex')[::-1]

## We'll also want to display our results as hex in RPC Byte Order, so
## we need to convert back.
def internal2rpc(hash):
  return hexlify(hash[::-1])



## build_tree takes a list of nodes in IBO and returns a merkle root in IBO
## Take an array with an factor-of-2 number of merkle nodes and hash
## each pair together. This is a recursive function where each level
## higher on the call stack is a level closer to the merkle root
def build_tree(list_of_nodes):
  ## if the list of nodes has only one has, it's the merkle root
  print("\n"+"Printing list of nodes")
  print (list_of_nodes)
  if len(list_of_nodes)==1:
    return list_of_nodes[0]

  ## Hash each pair together into a new list nodes one level closer
  ## the the merkle root
  new_nodes = []
  for i in range (0, len(list_of_nodes)-1,2):
    new_nodes.append(sha256d(list_of_nodes[i] + list_of_nodes[i+1]))

  ## Recursively build the next level closer to the merkle root
  return (build_tree(new_nodes))


 



## Take an array with two txids and hash them together to produce a
## merkle root.
def find_merkle_root(txids):
  ## Start by converting all hashes to Internal Byte Order, using them
  ## as the merkle leaf nodes
  leaf_nodes = []
  for i in range(0, len(txids)):
    leaf_nodes.append(rpc2internal(txids[i]))
    
  ## Use build_tree() to find the merkle root and convert the result
  ## to RPC byte order.
  return internal2rpc(build_tree(leaf_nodes))

## These are the txids from block 546.  The correct merkle root is
## e10a7f8442ea6cc6803a2b83713765c0b1199924110205f601f90fef125e7dfe
block_txids = [
  "e980fe9f792d014e73b95203dc1335c5f9ce19ac537a419e6df5b47aecb93b70",
  "28204cad1d7fc1d199e8ef4fa22f182de6258a3eaafe1bbe56ebdcacd3069a5f",
  "6b0f8a73a56c04b519f1883e8aafda643ba61a30bd1439969df21bea5f4e27e2",
  "3c1d7e82342158e4109df2e0b6348b6e84e403d8b4046d7007663ace63cddb23",
]

print(find_merkle_root(block_txids))

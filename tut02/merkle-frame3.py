## Objective: get the merkle root of a tree with an unbalanced number of
## nodes in one row

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

  ## If this merkle row has an odd number of elements, hash the
  ## last node with itself
  if len(list_of_nodes)%2==1:
    new_nodes.append(sha256d(list_of_nodes[-1] + list_of_nodes[-1]))
  
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

## These are the txids from block 586. The correct merkle root is
## 197b3d968ce463aa5da7d8eeba8af35eba80ded4e4fe6808e6cc0dd1c069594d
block_txids = [
  "d45724bacd1480b0c94d363ebf59f844fb54e60cdfda0cd38ef67154e9d0bc43",
  "4d6edbeb62735d45ff1565385a8b0045f066055c9425e21540ea7a8060f08bf2",
  "6bf363548b08aa8761e278be802a2d84b8e40daefe8150f9af7dd7b65a0de49f",
]

print(find_merkle_root(block_txids))

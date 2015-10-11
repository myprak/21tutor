## Objective: hash A|B to get merkle root C

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

## Take an array with two txids and hash them together to produce a
## merkle root.
def find_merkle_root(txids):
  ## Start by converting all hashes to Internal Byte Order, using them
  ## as the merkle leaf nodes
  leaf_nodes = []
  for i in range(0, len(txids)):
    leaf_nodes.append(rpc2internal(txids[i]))

  ## In this case, we know we're going to have two leaves, so simply
  ## hash them together and return the result in RPC byte order.
  return internal2rpc(sha256d(leaf_nodes[0] + leaf_nodes[1]))

## These are the txids from block 170. The correct merkle root for that
## block is 7dac2c5666815c17a3b36427de37bb9d2e2c5ccec3f8633eb91a4205cb4c10ff
block_txids = [
  "b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082",
  "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16",
]

print(find_merkle_root(block_txids))

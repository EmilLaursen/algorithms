
## HuffmanCode:
  - Currently compresses mobydick.txt (see https://gist.github.com/StevenClontz/4445774) from 654kB til 6.5kB!
  - Massive failure: Does not save serialization of huffman tree along with
  compressed data.

# TODO:
  - [] Encode huffmantree with code. Look at DEFLATE compression specification:
    https://www.ietf.org/rfc/rfc1951.txt
  - [] Enable compression of arbitrary byte data (alphabet size 256), not just strings.

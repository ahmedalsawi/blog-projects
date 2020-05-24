"""
makeshift MD5 implementation
https://tools.ietf.org/html/rfc1321

"""

from bitarray import bitarray


## bitarray utils
def hexstr_to_bitarray(h):
    ba = bitarray(endian='big')
    ba.frombytes(bytes.fromhex(h))
    return ba

def bitarray_to_hexstr(ba):
    return hex(int.from_bytes(ba.tobytes(),byteorder='big'))

def bitarray_to_int(ba):
    return int.from_bytes(ba.tobytes(),byteorder='big')

def int_to_bitarray(i,size=4):
     ba = bitarray()
     ba.frombytes(i.to_bytes(size,byteorder='big'))
     return ba

def rotate(x,s):
    return x[s:] + x[0:s]

def add_bitarray(a,b):
    i1 = bitarray_to_int(a)
    i2 = bitarray_to_int(b)
    i3 = (i1 + i2) % pow(2,32)
    return int_to_bitarray(i3)

def reverse_bytes(word):
    return word[24:32] + word[16:24] + word[8:16] + word[0:8]
## Constants
T =[
  bitarray('0'*32),  
  hexstr_to_bitarray("d76aa478"),
  hexstr_to_bitarray("e8c7b756"),
  hexstr_to_bitarray("242070db"),
  hexstr_to_bitarray("c1bdceee"),
  hexstr_to_bitarray("f57c0faf"),
  hexstr_to_bitarray("4787c62a"),
  hexstr_to_bitarray("a8304613"),
  hexstr_to_bitarray("fd469501"),
  hexstr_to_bitarray("698098d8"),
  hexstr_to_bitarray("8b44f7af"),
  hexstr_to_bitarray("ffff5bb1"),
  hexstr_to_bitarray("895cd7be"),
  hexstr_to_bitarray("6b901122"),
  hexstr_to_bitarray("fd987193"),
  hexstr_to_bitarray("a679438e"),
  hexstr_to_bitarray("49b40821"),
  hexstr_to_bitarray("f61e2562"),
  hexstr_to_bitarray("c040b340"),
  hexstr_to_bitarray("265e5a51"),
  hexstr_to_bitarray("e9b6c7aa"),
  hexstr_to_bitarray("d62f105d"),
  hexstr_to_bitarray("02441453"),
  hexstr_to_bitarray("d8a1e681"),
  hexstr_to_bitarray("e7d3fbc8"),
  hexstr_to_bitarray("21e1cde6"),
  hexstr_to_bitarray("c33707d6"),
  hexstr_to_bitarray("f4d50d87"),
  hexstr_to_bitarray("455a14ed"),
  hexstr_to_bitarray("a9e3e905"),
  hexstr_to_bitarray("fcefa3f8"),
  hexstr_to_bitarray("676f02d9"),
  hexstr_to_bitarray("8d2a4c8a"),
  hexstr_to_bitarray("fffa3942"),
  hexstr_to_bitarray("8771f681"),
  hexstr_to_bitarray("6d9d6122"),
  hexstr_to_bitarray("fde5380c"),
  hexstr_to_bitarray("a4beea44"),
  hexstr_to_bitarray("4bdecfa9"),
  hexstr_to_bitarray("f6bb4b60"),
  hexstr_to_bitarray("bebfbc70"),
  hexstr_to_bitarray("289b7ec6"),
  hexstr_to_bitarray("eaa127fa"),
  hexstr_to_bitarray("d4ef3085"),
  hexstr_to_bitarray("04881d05"),
  hexstr_to_bitarray("d9d4d039"),
  hexstr_to_bitarray("e6db99e5"),
  hexstr_to_bitarray("1fa27cf8"),
  hexstr_to_bitarray("c4ac5665"),
  hexstr_to_bitarray("f4292244"),
  hexstr_to_bitarray("432aff97"),
  hexstr_to_bitarray("ab9423a7"),
  hexstr_to_bitarray("fc93a039"),
  hexstr_to_bitarray("655b59c3"),
  hexstr_to_bitarray("8f0ccc92"),
  hexstr_to_bitarray("ffeff47d"),
  hexstr_to_bitarray("85845dd1"),
  hexstr_to_bitarray("6fa87e4f"),
  hexstr_to_bitarray("fe2ce6e0"),
  hexstr_to_bitarray("a3014314"),
  hexstr_to_bitarray("4e0811a1"),
  hexstr_to_bitarray("f7537e82"),
  hexstr_to_bitarray("bd3af235"),
  hexstr_to_bitarray("2ad7d2bb"),
  hexstr_to_bitarray("eb86d391"),
]

## MD5 operations
def F(x,y,z):
    return (x & y) | (~x & z)
def G(x,y,z):
    return (x & z) | (y & ~z)
def H(x,y,z):
    return (x ^ y ^ z)
def I(x,y,z):
    return y ^ (x | ~z)

"""
#a = b + ((a + func(b,c,d) + x + t) <<< s)
"""
def op(a, b, c , d, x, s, t, func):
    bit_tmp = func(b,c,d)
    bit_tmp  = add_bitarray(bit_tmp, x)
    bit_tmp  = add_bitarray(bit_tmp, a)

    bit_tmp  = add_bitarray(bit_tmp, t)
    bit_tmp  = rotate(bit_tmp,s)
    bit_tmp  = add_bitarray(bit_tmp,b)
    return bit_tmp
    

def md5sum(data):
    # convert string to bit array
    message = bitarray(endian='big')
    message.frombytes(data.encode())
    message_len = len(message)

    # Append padding up to 448
    rem = message_len % 512
    if rem >= 448:
        num_padding = 512 -rem + 448
    else:
        num_padding = 448 - rem
    padding = bitarray('1'+ ('0' * (num_padding - 1)))
    message.extend(padding)
    
    # Append message length
    message_len_bt = bitarray()
    message_len_64 = message_len % pow(2,64)
    message_len_bt = int_to_bitarray(message_len_64,size=8)
    message_len_bt = reverse_bytes(message_len_bt[32:64]) + reverse_bytes( message_len_bt[0:32])
    message.extend(message_len_bt)

    # Digest init
    A = hexstr_to_bitarray('67452301')
    B = hexstr_to_bitarray('efcdab89')
    C = hexstr_to_bitarray('98badcfe')
    D = hexstr_to_bitarray('10325476')


    # create N and M arrays. just to follow RFC notation
    N = int(len(message) / 32)
    M = []
    for i in range(N):
        word = message[i*32:(i*32)+32]
        word = reverse_bytes(word)
        M.append(bitarray(word))

    # The digest 
    for i in range(int(N/16)):
        X = []
        for j in range(16):
            X.append(bitarray(M[i*16+j]))

        AA = A
        BB = B
        CC = C
        DD = D

        # Round 1
        A = op(A,B,C,D,X[0],7,T[1],F)
        D = op(D,A,B,C,X[1],12,T[2],F)
        C = op(C,D,A,B,X[2],17,T[3],F)
        B = op(B,C,D,A,X[3],22,T[4],F)

        A = op(A,B,C,D,X[4],7,T[5],F)
        D = op(D,A,B,C,X[5],12,T[6],F)
        C = op(C,D,A,B,X[6],17,T[7],F)
        B = op(B,C,D,A,X[7],22,T[8],F)

        A = op(A,B,C,D,X[8],7,T[9],F)
        D = op(D,A,B,C,X[9],12,T[10],F)
        C = op(C,D,A,B,X[10],17,T[11],F)
        B = op(B,C,D,A,X[11],22,T[12],F)
        
        A = op(A,B,C,D,X[12],7,T[13],F)
        D = op(D,A,B,C,X[13],12,T[14],F)
        C = op(C,D,A,B,X[14],17,T[15],F)
        B = op(B,C,D,A,X[15],22,T[16],F)

        # Round 2
        A = op(A,B,C,D,X[1],    5,  T[17],G)
        D = op(D,A,B,C,X[6],    9,  T[18],G)
        C = op(C,D,A,B,X[11],   14, T[19],G)
        B = op(B,C,D,A,X[0],    20, T[20],G)

        A = op(A,B,C,D,X[5],    5,  T[21],G)
        D = op(D,A,B,C,X[10],    9,  T[22],G)
        C = op(C,D,A,B,X[15],   14, T[23],G)
        B = op(B,C,D,A,X[4],    20, T[24],G)

        A = op(A,B,C,D,X[9],    5,  T[25],G)
        D = op(D,A,B,C,X[14],    9,  T[26],G)
        C = op(C,D,A,B,X[3],   14, T[27],G)
        B = op(B,C,D,A,X[8],    20, T[28],G)

        A = op(A,B,C,D,X[13],    5,  T[29],G)
        D = op(D,A,B,C,X[2],    9,  T[30],G)
        C = op(C,D,A,B,X[7],   14, T[31],G)
        B = op(B,C,D,A,X[12],    20, T[32],G)

        # Round 3
        A = op(A,B,C,D,X[5],    4,  T[33],H)
        D = op(D,A,B,C,X[8],    11, T[34],H)
        C = op(C,D,A,B,X[11],   16, T[35],H)
        B = op(B,C,D,A,X[14],    23, T[36],H)

        A = op(A,B,C,D,X[1],    4,  T[37],H)
        D = op(D,A,B,C,X[4],    11, T[38],H)
        C = op(C,D,A,B,X[7],   16, T[39],H)
        B = op(B,C,D,A,X[10],    23, T[40],H)

        A = op(A,B,C,D,X[13],    4,  T[41],H)
        D = op(D,A,B,C,X[0],    11, T[42],H)
        C = op(C,D,A,B,X[3],   16, T[43],H)
        B = op(B,C,D,A,X[6],    23, T[44],H)

        A = op(A,B,C,D,X[9],    4,  T[45],H)
        D = op(D,A,B,C,X[12],    11, T[46],H)
        C = op(C,D,A,B,X[15],   16, T[47],H)
        B = op(B,C,D,A,X[2],    23, T[48],H)

        # Round 4
        A = op(A,B,C,D,X[0],     6,  T[49],I)
        D = op(D,A,B,C,X[7],     10, T[50],I)
        C = op(C,D,A,B,X[14],    15, T[51],I)
        B = op(B,C,D,A,X[5],    21, T[52],I)

        A = op(A,B,C,D,X[12],     6,  T[53],I)
        D = op(D,A,B,C,X[3],     10, T[54],I)
        C = op(C,D,A,B,X[10],    15, T[55],I)
        B = op(B,C,D,A,X[1],    21, T[56],I)

        A = op(A,B,C,D,X[8],     6,  T[57],I)
        D = op(D,A,B,C,X[15],     10, T[58],I)
        C = op(C,D,A,B,X[6],    15, T[59],I)
        B = op(B,C,D,A,X[13],    21, T[60],I)

        A = op(A,B,C,D,X[4],     6,  T[61],I)
        D = op(D,A,B,C,X[11],     10, T[62],I)
        C = op(C,D,A,B,X[2],    15, T[63],I)
        B = op(B,C,D,A,X[9],    21, T[64],I)

        # Add buffers
        A = add_bitarray(AA,A)
        B = add_bitarray(BB,B)
        C = add_bitarray(CC,C)
        D = add_bitarray(DD,D)

    md5 = reverse_bytes(A) + reverse_bytes(B) + reverse_bytes(C) +  reverse_bytes(D)
    return bitarray_to_hexstr(md5)[2:]

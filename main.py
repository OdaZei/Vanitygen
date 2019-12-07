import binascii, hashlib
#extended_gcd function
filepath = "prv_text.txt"


def extended_gcd(aa, bb):
	lastremainder, remainder = abs(aa), abs(bb)
	x, lastx, y, lasty = 0, 1, 1, 0
	while remainder:
		lastremainder, (quotient, remainder) = remainder, divmod(
		    lastremainder, remainder)
		x, lastx = lastx - quotient * x, x
		y, lasty = lasty - quotient * y, y
	return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0
	                                                              else 1)


#modinv function
def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m


#Wallet		: 1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF
#TX ID		: 48287df18d6e81538bd909b186a3eb88e0ec9e2757fcfa7132bcb9f5188192f4
#Final Balance	: 79,957.17564655 BTC
R = 0x000084a292d9d4dcc3b1579e1f3e50400d219ed36b3ba58de242970d1c9daaa21014
S = 0x00705d5c53e7d0d2c8fb42c23340fe469cd8384a9d1bba8fe7019e7c3937916212
Z = 0x00d2eef12d53057e5ed033236c39e1292a3a18d296d496d6f11052ce5715f5a23e
X = 0x004dc50123dd13a938607e55509c442c9fcf3c2ab51b9a754db034506b67f070c4
K = 0x000000000000000000000000000000000000000000000000000000000000000001
N = 0x00fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

#Private Key Equation
X = ((((S * K) - Z) * modinv(R, N)) % N)
Xc = hex(X)[2:][:-1]
if len(Xc) < 2:
	print "Usage: %s <format string>\n\nRead a hex private key from stdin and output formatted data.\n"
	print "These variables are supported:\n%h = HEX privkey\n%w = WIF privkey\n%p = public key\n%a = address\n"
	print "eg. 'Address: %a\\nPrivkey: %w' outputs a format like the vanitygen program\n"

alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
advanced = any(v in Xc for v in ['%p', '%a'])


def b58encode(num, pad=''):
	out = ''
	while num >= 58:
		num, m = divmod(num, 58)
		out = alphabet[m] + out
	return pad + alphabet[num] + out


def b58hex(s58):
	num = 0L
	for (i, c) in enumerate(s58[::-1]):
		num += alphabet.find(c) * (58**i)
	return hex(num)[4:-9].upper()


import ecdsa

# secp256k1, http://www.oid-info.com/get/1.3.132.0.10
_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
_b = 0x0000000000000000000000000000000000000000000000000000000000000007L
_a = 0x0000000000000000000000000000000000000000000000000000000000000000L
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L
curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
oid_secp256k1 = (1, 3, 132, 0, 10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1,
                               generator_secp256k1, oid_secp256k1)

Xc = Xc.replace(' ', '')
Xc = b58hex(Xc[:51]) if Xc[0] == '5' and len(Xc) < 64 else Xc[:64]
try:
	chksum = binascii.hexlify(
	    hashlib.sha256(hashlib.sha256(
	        binascii.unhexlify('80' + Xc)).digest()).digest()[:4])
except:
	pass
privkey = long('80' + Xc + chksum, 16)
pubkey = chr(4) + ecdsa.SigningKey.from_secret_exponent(
    long(Xc, 16), curve=SECP256k1).get_verifying_key().to_string()
pad = ""
rmd = hashlib.new('ripemd160')
rmd.update(hashlib.sha256(pubkey).digest())
an = chr(0) + rmd.digest()
for c in an:
	if c == '\0': pad += '1'
	else: break
addr = long(
    binascii.hexlify(
        an + hashlib.sha256(hashlib.sha256(an).digest()).digest()[0:4]), 16)
print 'HEX Private Key:', Xc
print 'WIF Private Key:', b58encode(privkey)
print 'Public Key:', binascii.hexlify(pubkey).upper()
print 'Bitcoin Address:', b58encode(addr, pad)
print ''
address = b58encode(addr, pad)
target = '1HYfivTqoSzjqy6eawyitWoK8HvigtU3yb'

while (address != target):
	import binascii, hashlib
	K = (K + 1)
	X = ((((S * K) - Z) * modinv(R, N)) % N)
	Xc = hex(X)[2:][:-1]
	if len(Xc) < 2:
		print "Usage: %s <format string>\n\nRead a hex private key from stdin and output formatted data.\n"
		print "These variables are supported:\n%h = HEX privkey\n%w = WIF privkey\n%p = public key\n%a = address\n"
		print "eg. 'Address: %a\\nPrivkey: %w' outputs a format like the vanitygen program\n"

	alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	advanced = any(v in Xc for v in ['%p', '%a'])

	def b58encode(num, pad=''):
		out = ''
		while num >= 58:
			num, m = divmod(num, 58)
			out = alphabet[m] + out
		return pad + alphabet[num] + out

	def b58hex(s58):
		num = 0L
		for (i, c) in enumerate(s58[::-1]):
			num += alphabet.find(c) * (58**i)
		return hex(num)[4:-9].upper()

	import ecdsa

	# secp256k1, http://www.oid-info.com/get/1.3.132.0.10
	_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL
	_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
	_b = 0x0000000000000000000000000000000000000000000000000000000000000007L
	_a = 0x0000000000000000000000000000000000000000000000000000000000000000L
	_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L
	_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L
	curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
	generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy,
	                                                _r)
	oid_secp256k1 = (1, 3, 132, 0, 10)
	SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1,
	                               generator_secp256k1, oid_secp256k1)

	Xc = Xc.replace(' ', '')
	Xc = b58hex(Xc[:51]) if Xc[0] == '5' and len(Xc) < 64 else Xc[:64]
	try:
		chksum = binascii.hexlify(
		    hashlib.sha256(
		        hashlib.sha256(
		            binascii.unhexlify('80' + Xc)).digest()).digest()[:4])
	except:
		pass
	privkey = long('80' + Xc + chksum, 16)
	pubkey = chr(4) + ecdsa.SigningKey.from_secret_exponent(
	    long(Xc, 16), curve=SECP256k1).get_verifying_key().to_string()
	pad = ""
	rmd = hashlib.new('ripemd160')
	rmd.update(hashlib.sha256(pubkey).digest())
	an = chr(0) + rmd.digest()
	for c in an:
		if c == '\0': pad += '1'
		else: break
	addr = long(
	    binascii.hexlify(
	        an + hashlib.sha256(hashlib.sha256(an).digest()).digest()[0:4]),
	    16)
	print 'HEX Private Key:', Xc
	print 'WIF Private Key:', b58encode(privkey)
	print 'Public Key:', binascii.hexlify(pubkey).upper()
	print 'Bitcoin Address:', b58encode(addr, pad)
	print ''
if target == address:
	print 'Bingo!'
	print 'HEX Private Key:', Xc
	print 'WIF Private Key:', b58encode(privkey)
	print 'Public Key:', binascii.hexlify(pubkey).upper()
	print 'Bitcoin Address:', b58encode(addr, pad)
	print ''

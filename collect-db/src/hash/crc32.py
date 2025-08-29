import binascii

# ~~~~~~~~~~~~~~~~~~~~~~~
# 関数
# ~~~~~~~~~~~~~~~~~~~~~~~
# ハッシュ化
def hash(word: str, pepper: str = '', salt: str = '') -> int:
	combined = (pepper + word + salt).encode('utf-8')
	return binascii.crc32(combined) & 0xffffffff

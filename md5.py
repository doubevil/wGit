import hashlib

src = '阿斯顿发送到发送到发送到发'

mdObj = hashlib.md5()
mdObj.update(src.encode(encoding='utf-8'))

print('MD5:' + src)
print('MD5:' + mdObj.hexdigest())
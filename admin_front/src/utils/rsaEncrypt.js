import JSEncrypt from 'jsencrypt/bin/jsencrypt'

// 密钥对生成 http://web.chacuo.net/netrsakeypair

const publicKey = `
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCofIO2t0UvpovPaccYdSbVtavn
vpsGCTEImvqz6jFS2+LwihpeW8VwlK6Bt6VFAnEgyqAa7r7I/WzFWCf+k4N8SjSR
mXrwcF0UVC27brRPihkYFnb4D59wlWuGDHdrDS58apWJNGlxKV8Ib0l3VG5aFCHb
LaeiO68FQB296P+/owIDAQAB
-----END PUBLIC KEY-----
`

// 加密
export function encrypt(txt) {
  const encryptor = new JSEncrypt()
  encryptor.setPublicKey(publicKey) // 设置公钥
  return encryptor.encrypt(txt.toString()) // 对需要加密的数据进行加密
}


importScripts('argon2-bundled.min.js');

self.onmessage = async (event) => {
    const salt = event.data.salt;
    const salt_64 = salt.toBase64()
    const senha_hash = event.data.senha_register;
    
    const hash = await self.argon2.hash({
    pass: senha_hash,
    salt: salt_64,
    time: 3,
    mem: 65536,
    hashLen: 32,
    parallelism: 4,
    type: 2
  });
  
  self.postMessage(hash.hashHex);
};
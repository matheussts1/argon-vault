importScripts('argon2-bundled.min.js');

self.onmessage = async (event) => {
    const salt = event.data.salt;
    const password = event.data.senha;
    
    const hash = await self.argon2.hash({
    pass: password,
    salt: salt,
    time: 3,
    mem: 65536,
    hashLen: 32,
    parallelism: 4,
    type: 2
});

    self.postMessage(hash.hashHex);
}
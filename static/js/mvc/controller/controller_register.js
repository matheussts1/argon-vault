document.querySelector("form.register").addEventListener('register', (r) => {
    const dados_worker = r.detail.message;
    const user = r.detail.message.user;
    const salt_antigo = r.detail.message.salt;
    const token = r.detail.message.token;

    const worker_register = new Worker('static/js/intern/worker_register.js');
    worker_register.postMessage(dados_worker);
    worker_register.onmessage = function (event) {
        const hash_recebido = event.data;
        const salt_64 = salt_antigo.toBase64()

        const dict_json = {
            csrf_token: token,
            user: user,
            password: hash_recebido,
            confirm_password: hash_recebido,
            salt: salt_64
        }

        const serializacao = JSON.stringify(dict_json);
        
        const url = "";
        const endpoint = "/register"

        const envio_dados = fetch(url + endpoint, { method: "POST", headers: { "Content-Type": "application/json"}, body: serializacao, credentials: 'include'})
        .then(response => response.json())
        .then(data => {
            if (data === "Sucesso") {
                window.location.href = "https://argon-vault.onrender.com/argonvault"
            } else {
                alert ("Erro no cadastro")
            }
        })
        .catch(error => {
            console.log("erro: ", error);
        });
    }
    worker_register.onerror = function (error) {
        console.error("Erro no Worker:", error.message);
        console.error("Arquivo:", error.filename);
        console.error("Linha:", error.lineno);
    }
})
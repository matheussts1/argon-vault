const form_login = document.querySelector("form.login");

form_login.addEventListener('login', (l) => {
    const username = l.detail.message.usuario;
    const password = l.detail.message.senha;
    const token = l.detail.message.token;

    const url = `/get-salt-login?username=${username}`

    fetch(url).then(function(response) {
        return response.json()
    }).then(function(data) {
        const salt = data.salt;
        const dados  = {
            senha: password,
            salt: salt
        }
        
        const worker_login = new Worker('static/js/intern/worker_login.js')
        worker_login.postMessage(dados);
        worker_login.onmessage = function (event) {
            const hash_front = event.data;

            const hash_json = {
                csrf_token: token,
                usuario: username,
                password: password,
                hash: hash_front
            }

            const serialization = JSON.stringify(hash_json);

            const url = "";
            const endpoint = "/login";

           const envio = fetch(url + endpoint, { method: "POST", headers: { "Content-Type": "application/json"}, body: serialization, credentials: 'include'})
            .then(response => response.json())
            .then(data => { if (data === 'Usuario logado!') {

                document.getElementById("section-login").style.display = 'none';
                document.getElementById("section-passwords").style.display = 'block';
                window.scrollTo(0, 0); 
                } else {
                    alert("Usuario ou senha incorretos!");
                }
            })
            .catch(error => {
                console.log("erro: ", error);
            });
        }
    }); 
});
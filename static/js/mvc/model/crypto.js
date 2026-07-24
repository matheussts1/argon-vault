async function key(m, salt) {
    let master_password = m;
    let sal = salt;

    const operations = window.crypto.subtle || window.crypto.webkitSubtle;

           if (!operations) {
            alert('Web Crypto nao é suportado');
           }

           const ALGO_NAME = 'PBKDF2';
           const molde_chave = operations.importKey(
            "raw",
            master_password,
            ALGO_NAME,
            false,
            ["deriveKey", "deriveBits"]
           );

           master_password.fill(0);
           master_password = null

            const chave = await operations.deriveKey({
            name:ALGO_NAME,
            salt:sal,
            iterations:300000,
            hash:"SHA-256"
            },
            await molde_chave,
            {name: "AES-GCM", length: 256},
            false,
             ["encrypt", "decrypt"]
        );

    return service;
    
    function service(s) {
        let service_password = s;
        return {encrypt, decrypt}

        async function encrypt() {

           if (!operations) {
            alert('Web Crypto nao é suportado');
           }

            const iv = window.crypto.getRandomValues(new Uint8Array(12));
            const iv_base64 = btoa(String.fromCharCode(...iv))
            const encryption = await operations.encrypt(
                {
                    name: "AES-GCM",
                    iv: iv
                },
                chave,
                service_password
            );
            const binary = String.fromCharCode(...new Uint8Array(encryption));
            const senha_criptografada = btoa(binary);

            service_password.fill(0);
            service_password = null

            return {
                senha: senha_criptografada,
                iv: iv_base64
            }
        }
        async function decrypt(iv, pass) { 
        const descriptografia = await operations.decrypt(
            {
                name: "AES-GCM",
                iv: iv
            },
            chave,
            pass
        );
        const decoder = new TextDecoder('utf-8');
        const senha_descriptografada = decoder.decode(descriptografia);

        return (senha_descriptografada)
        }
    }
}

let cripto;
let service;
let result;

const crypto_form = document.querySelector("form.passwords");
const master_form = document.querySelector("form.login");
const container = document.querySelector(".passwords-container");
const lixeira = document.querySelector("form.lixo");
const token = document.querySelector("#csrf_token").value

master_form.addEventListener("submit", () => {
    const senha_main = document.getElementById("password").value;
    const encoder = new TextEncoder();
    const senha_bytes = encoder.encode(senha_main);

    const usuario = document.getElementById("usuario").value;

    const url = `/get-salt-crypto?usuario=${usuario}`

    fetch(url).then(function(response) {
        return response.json()
    }).then(async function(data) {
        const salt = data.salt;
        const salt_bytes = encoder.encode(salt)

        service = await key(senha_bytes, salt_bytes);
        document.getElementById("password").value = '';
    });
    
});

crypto_form.addEventListener('senha', async (s) => {
    const senha_servico = s.detail.message.senha_service;
    const encoder = new TextEncoder();
    const senha_servico_bytes = encoder.encode(senha_servico)

    cripto = service(senha_servico_bytes);
    data = await cripto.encrypt();

    const token = s.detail.message.token;
    const service_bd = s.detail.message.service;
    const user_bd = s.detail.message.usuario_service;
    const senha_criptografada = data.senha;
    const iv_bd = data.iv;
    
    const dict_bd = {
        csrf_token: token,
        service: service_bd,
        usuario_service: user_bd,
        password_service: senha_criptografada,
        iv: iv_bd
    }

    const dict_json = JSON.stringify(dict_bd);

    const url = "";
    const endpoint = "/passwords";

    const senha_add = fetch(url + endpoint, {method: "POST", headers: { "Content-Type": "application/json"}, body: dict_json, credentials: 'include'})
    .then(response => response.json())
    .then(data => { if (data.message === "Senha salva com sucesso") {
        const id_senha = data.ID;
        const lista = document.querySelector("div.passwords-container");

        const novo_card = `
    <div class="password-card">
        <center>
            <div class="card-header">
                <h2>
                    <span class="label">Serviço: </span>
                    <h3 class="service-name">${service_bd}</h3>
                </h2>
            </div>

            <div class="card-body">
                <div class="info-group">
                    <br><span class="label">Usuário:</span>
                    <p class="user-display">${user_bd}</p>
                </div>
                <div class="info-group">
                    <br><span class="label">Senha:</span>
                    <div class="password-wrapper">
                        <p class="asteriscos">*************************</p>
                    </div>
                </div>
            </div>

            <div class="card-footer">
                <div class="actions">
                    <button data-password="${senha_criptografada}" data-iv="${iv_bd}" class="btns btn-eye" type="button">
                            <i class="bi bi-eye"></i>
                    </button>

                    <button hidden class="btns-slash btn-eye-slash" type="button">
                        <i class="bi bi-eye-slash"></i>
                    </button>

                    <form method="POST" action="/delete">
                    <input type="hidden" name="id_senha" value="${id_senha}"> 
                    <input id="csrf_token" name="csrf_token" type="hidden" value=${token}>
                    <button hidden class="lixeira btn" type="submit">
                        <i class="bi bi-trash"></i>
                    </button>
                        </form>
                    </div>
                </div>
            </div>
        </center>
    </div>
`;
    
    lista.insertAdjacentHTML('beforeend', novo_card);
    } else {
        alert("Erro no salvamento da senha!");
    }

    })
    .catch(error => { 
        console.log("error: ", error);
    })
})

container.addEventListener("click", async (event) => {
    const btn = event.target.closest(".btn-eye");

    if (btn) {
        const pass = btn.getAttribute('data-password');
        const p = atob(pass)
        const pass_bytes = Uint8Array.from(p, z => z.charCodeAt(0))
        
        const iv = btn.getAttribute('data-iv');
        const b = atob(iv);
        const iv_bytes = Uint8Array.from(b, c => c.charCodeAt(0))

        let process = service()
        let dec = await process.decrypt(iv_bytes, pass_bytes);

        const ast = btn.closest("div.password-card").querySelector("p.asteriscos");
        const olho_revelar = btn.closest("div.password-card").querySelector("i");
        const lixeira = btn.closest("div.password-card").querySelector("button.lixeira");
        
        if (ast.textContent.trim() === "*************************") {
            ast.textContent = dec;
            olho_revelar.classList.replace("bi-eye", "bi-eye-slash");
            lixeira.hidden = false;
        } else {
            ast.textContent = "*************************";
            olho_revelar.classList.replace("bi-eye-slash", "bi-eye");
            lixeira.hidden = true;
        }
    }
});

container.addEventListener("click", (l) => {
    l.preventDefault()
    const lixo = l.target.closest("button.lixeira");

    if (lixo) {
        const id = lixo.closest("div.password-card").querySelector("input").value;

        const id_dict = {
            csrf_token: token,
            id_senha: id
        }

        const id_json = JSON.stringify(id_dict);

        const url = "";
        const endpoint = "/delete";

        const envio_delete = fetch(url + endpoint, {method: "POST", headers: { "Content-Type": "application/json"}, body: id_json, credentials: 'include'})
        .then(response => response.json())
        .then(data =>  {
            if (data === "ID successfully deleted!") {
                document.querySelector("div.password-card").remove()
            } else {
                console.log("Algo deu errado no delete")
            }
        })
        .catch(error => { 
        console.log("error: ", error);
        })
    }
})
let idleTime = (5 * 1000) * 60;
let timeOut;
let isIdle = false;

function setActive() {
    isIdle = false;
    clearTimeout(timeOut);
    timeOut = setTimeout(setIdle, idleTime);
}

function setIdle() {
    isIdle = true;
    window.location.reload();
    alert("Sua sessão expirou, logue denovo para ver suas senhas");
}

["mousemove", "keydown", "scroll", "touchstart"].forEach(action => {
    document.addEventListener(action, setActive);
});

setActive();

const passwords_form = document.querySelector("form.passwords");

passwords_form.addEventListener('passwords', (p) => {
    const service = p.detail.message.service;
    const usuario_service = p.detail.message.usuario;
    const senha_service = p.detail.message.senha_servico;
    const token = p.detail.message.token;

    const pacote_senha = {
        service: service,
        usuario_service: usuario_service,
        senha_service: senha_service,
        token: token
    }

    const envio_senha = new CustomEvent('senha', {
        detail:{message: pacote_senha}
    });
    passwords_form.dispatchEvent(envio_senha);
});
class PasswordValues {
    constructor(service, usuario, senha_servico, token) {
        this.service = service;
        this.usuario = usuario;
        this.senha_servico = senha_servico;
        this.token = token
    }

    verificar() {
        if (this.service && this.usuario && this.senha_servico && this.token) {
            return true;
        } else {
            console.log("Um dos dados esta vazio!")
            return false;
        }
    }
}

const button_add = document.querySelector("button.btn-add");
const add_passwords = document.getElementById("section-add");
const form_passwords = document.querySelector("form.passwords")

button_add.addEventListener("click", function () {
    add_passwords.style.display = 'flex'; 
});

add_passwords.addEventListener("click", function (e) {
    if (e.target === add_passwords) {
        add_passwords.style.display = 'none';
    }
});

form_passwords.addEventListener("submit", function (f) {
    f.preventDefault()

    const service = document.getElementById("service").value;
    const usuario = document.getElementById("usuario_service").value;
    const senha_servico = document.getElementById("password_service").value;
    const token = form_passwords.closest("section.add_passwords").querySelector("input").value;

    const dados_passwords = new PasswordValues(service, usuario, senha_servico, token);

    if (dados_passwords.verificar() == true) {
        const envio_passwords = new CustomEvent('passwords', {
            detail:{message: dados_passwords}
        });
        form_passwords.dispatchEvent(envio_passwords);
    } else {
        alert("Um dos dados esta vazio!")
    }

    document.getElementById("password_service").value = '';
})
class RegisterValues {
    constructor(usuario, senha, senha_confirmation, token) {
    this.usuario = usuario;
    this.senha = senha;
    this.senha_confirmation = senha_confirmation;
    this.token = token;
}

verificar() {
    if (this.usuario && this.senha && this.senha_confirmation && this.token)  {
        return true;
    } 
    else {
        console.log("Um dos dados esta vazio!");
        return false;
        }
    }
}

class Data {
    constructor(user, senha_register, salt, token) {
        this.user = user;
        this.senha_register = senha_register;
        this.salt = salt;
        this.token = token;
    }
}

const form_register = document.querySelector("form.register");

form_register.addEventListener("submit", function (r) {
    r.preventDefault();

    const usuario = document.getElementById("user").value;
    const senha_register = document.getElementById("password").value;
    const senha_confirmation = document.getElementById("confirm_password").value;
    const token = document.getElementById("csrf_token").value;

    const dados_register = new RegisterValues(usuario, senha_register, senha_confirmation, token);

    if (dados_register.verificar() == true) {
        if (senha_register === senha_confirmation) {
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const pacote_controller = new Data(usuario, senha_register, salt, token);
            
            const envio_register = new CustomEvent('register', {
                detail:{message: pacote_controller}
            });
            form_register.dispatchEvent(envio_register);
        }
        else {
            alert("A senha e a confirmação da senha nao batem!")
        }
    } else {
        alert("Um dos dados esta vazio!")
    }
})
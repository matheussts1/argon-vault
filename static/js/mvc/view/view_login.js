class LoginValues {
    constructor(usuario, senha, token) {
    this.usuario = usuario;
    this.senha = senha;
    this.token = token;
}

verificar() {
    if (this.usuario && this.senha && this.token) {
        return true;
    } 
    else {
        console.log("Um dos dados esta vazio!");
        return false;
        }
    }
}

const form = document.querySelector("form.login")

form.addEventListener("submit", function (l) {
    l.preventDefault();
    const usuario = document.getElementById("usuario").value;
    const senha = document.getElementById("password").value;
    const token = form.closest("section.main-section").querySelector("input").value

    const dados_login = new LoginValues(usuario, senha, token)

    if (dados_login.verificar() == true) {
        const envio_login = new CustomEvent('login', {
            detail:{message: dados_login}
        });
        form.dispatchEvent(envio_login);
    } else {
        alert("Um dos dados esta vazio!")
    }
})
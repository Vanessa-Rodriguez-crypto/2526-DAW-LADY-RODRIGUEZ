const nombre = document.getElementById("nombre");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirmar = document.getElementById("confirmar");
const edad = document.getElementById("edad");
const btnEnviar = document.getElementById("btnEnviar");
const formulario = document.getElementById("formulario");

const validarCampo = (input, condicion, mensaje) => {
    const error = input.nextElementSibling;
    if (condicion) {
        input.classList.add("valido");
        input.classList.remove("invalido");
        error.textContent = "";
        return true;
    } else {
        input.classList.add("invalido");
        input.classList.remove("valido");
        error.textContent = mensaje;
        return false;
    }
};

function validarFormulario() {
    const nombreValido = validarCampo(
        nombre,
        nombre.value.length >= 3,
        "El nombre debe tener al menos 3 caracteres"
    );

    const emailValido = validarCampo(
        email,
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value),
        "Correo electrónico inválido"
    );

    const passwordValido = validarCampo(
        password,
        /^(?=.*\d)(?=.*[\W_]).{8,}$/.test(password.value),
        "Mínimo 8 caracteres, un número y un símbolo"
    );

    const confirmarValido = validarCampo(
        confirmar,
        confirmar.value === password.value && confirmar.value !== "",
        "Las contraseñas no coinciden"
    );

    const edadValida = validarCampo(
        edad,
        edad.value >= 18,
        "Debes ser mayor de edad"
    );

    btnEnviar.disabled = !(nombreValido && emailValido && passwordValido && confirmarValido && edadValida);
}

[nombre, email, password, confirmar, edad].forEach(campo => {
    campo.addEventListener("input", validarFormulario);
});

formulario.addEventListener("submit", e => {
    e.preventDefault();
    alert("Formulario enviado correctamente ✔️");
    formulario.reset();
    btnEnviar.disabled = true;
});

const imageUrlInput = document.getElementById("imageUrl");
const addImageBtn = document.getElementById("addImage");
const deleteImageBtn = document.getElementById("deleteImage");
const gallery = document.getElementById("gallery");

let selectedImage = null;

// Agregar imagen
addImageBtn.addEventListener("click", () => {
    const imageUrl = imageUrlInput.value;

    if (imageUrl === "") {
        alert("Por favor ingresa una URL válida");
        return;
    }

    const img = document.createElement("img");
    img.src = imageUrl;

    img.addEventListener("click", () => {
        selectImage(img);
    });

    gallery.appendChild(img);
    imageUrlInput.value = "";
});

// Seleccionar imagen
function selectImage(img) {
    const images = document.querySelectorAll(".gallery img");
    images.forEach(image => image.classList.remove("selected"));

    img.classList.add("selected");
    selectedImage = img;
}

// Eliminar imagen seleccionada
deleteImageBtn.addEventListener("click", () => {
    if (selectedImage) {
        gallery.removeChild(selectedImage);
        selectedImage = null;
    } else {
        alert("No hay ninguna imagen seleccionada");
    }
});

// Atajos de teclado
document.addEventListener("keydown", (event) => {
    if (event.key === "Delete") {
        if (selectedImage) {
            gallery.removeChild(selectedImage);
            selectedImage = null;
        }
    }
});

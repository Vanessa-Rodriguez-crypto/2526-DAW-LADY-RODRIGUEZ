// Arreglo de productos iniciales
// Cada producto es un objeto con nombre, precio y descripción
const productos = [
    {
        nombre: "Laptop",
        precio: 850,
        descripcion: "Equipo portátil para estudio y trabajo"
    },
    {
        nombre: "Mouse",
        precio: 15,
        descripcion: "Mouse inalámbrico ergonómico"
    },
    {
        nombre: "Teclado",
        precio: 30,
        descripcion: "Teclado mecánico compacto"
    }
];

// Obtención de los elementos del DOM
// Lista donde se mostrarán los productos
const lista = document.getElementById("listaProductos");

// Botón para agregar nuevos productos
const botonAgregar = document.getElementById("btnAgregar");

// Función que renderiza la lista de productos dinámicamente
function renderizarProductos() {

    // Limpia la lista para evitar duplicados
    lista.innerHTML = "";

    // Recorre el arreglo de productos
    productos.forEach(producto => {

        // Crea un elemento <li> por cada producto
        const li = document.createElement("li");

        // Inserta la información del producto usando plantillas
        li.innerHTML = `
            <strong>${producto.nombre}</strong><br>
            Precio: $${producto.precio}<br>
            ${producto.descripcion}
        `;

        // Agrega el <li> a la lista <ul>
        lista.appendChild(li);
    });
}

// Evento que se ejecuta al presionar el botón "Agregar Producto"
botonAgregar.addEventListener("click", () => {

    // Nuevo producto creado dinámicamente
    const nuevoProducto = {
        nombre: "Nuevo Producto",
        precio: 20,
        descripcion: "Producto agregado dinámicamente"
    };

    // Se agrega el nuevo producto al arreglo
    productos.push(nuevoProducto);

    // Se vuelve a renderizar la lista actualizada
    renderizarProductos();
});

// Llama a la función cuando la página se carga
// para mostrar los productos iniciales
renderizarProductos();

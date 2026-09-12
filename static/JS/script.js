// =============================
// CARRITO SIMPLE
// =============================

let contador = 0;

const contadorHTML = document.getElementById("contador");

const botones = document.querySelectorAll(".btn-warning");

botones.forEach((boton) => {

    if (boton.textContent.includes("Agregar")) {

        boton.addEventListener("click", function () {

            contador++;

            if (contadorHTML) {

                contadorHTML.textContent = contador;

            }

            alert("Producto agregado al carrito.");

        });

    }

});

// =============================
// NAVBAR SCROLL
// =============================

window.addEventListener("scroll", function(){

    const menu = document.querySelector(".navbar");

    if(menu){

        if(window.scrollY > 50){

            menu.classList.add("menu-scroll");

        }else{

            menu.classList.remove("menu-scroll");

        }

    }

});

//======================
// ANIMACIÓN SUAVE
//======================

const elementos=document.querySelectorAll("section");

const mostrar=()=>{

elementos.forEach(el=>{

const posicion=el.getBoundingClientRect().top;

const pantalla=window.innerHeight;

if(posicion<pantalla-120){

el.style.opacity="1";

el.style.transform="translateY(0)";

}

});

};

window.addEventListener("scroll",mostrar);

mostrar();

//======================
// BOTÓN SUBIR
//======================

const btnTop = document.getElementById("btnTop");

if(btnTop){

    btnTop.style.display = "none";

    window.addEventListener("scroll", () => {

        if(window.scrollY > 300){

            btnTop.style.display = "flex";

        }else{

            btnTop.style.display = "none";

        }

    });

    btnTop.addEventListener("click", function(e){

        e.preventDefault();

        window.scrollTo({

            top:0,

            behavior:"smooth"

        });

    });

}

/*==================================================
        CAPITAL BIKER
        JAVASCRIPT - DETALLE DE PRODUCTO
==================================================*/

document.addEventListener("DOMContentLoaded", () => {
    const varianteSelect = document.getElementById("variante");
    const cantidadInput = document.getElementById("cantidad");

    if (varianteSelect && cantidadInput) {
        // Evento para leer el stock dinámico de la variante seleccionada
        varianteSelect.addEventListener("change", function () {
            const optionSelected = this.options[this.selectedIndex];
            
            // Reiniciar siempre la cantidad a 1 al cambiar de variante
            cantidadInput.value = 1; 

            if (optionSelected && optionSelected.value !== "") {
                const texto = optionSelected.text;
                // Expresión regular que busca el número después de 'Stock: '
                const stockMatch = texto.match(/Stock:\s*(\d+)/);
                
                if (stockMatch) {
                    cantidadInput.max = parseInt(stockMatch[1], 10);
                }
            } else {
                cantidadInput.max = 1;
            }
        });
    }
});

/**
 * Incrementa la cantidad respetando el máximo del stock de la variante
 */
function aumentarCantidad() {
    const varianteSelect = document.getElementById("variante");
    const cantidadInput = document.getElementById("cantidad");
    
    if (!varianteSelect || !cantidadInput) return;

    // Bloquear incremento si no hay variante elegida
    if (varianteSelect.value === "") {
        alert("Por favor, selecciona primero una talla y color.");
        return;
    }

    let valor = parseInt(cantidadInput.value, 10);
    let maximo = parseInt(cantidadInput.max, 10) || 1;

    if (valor < maximo) {
        cantidadInput.value = valor + 1;
    } else {
        alert("Has alcanzado el límite máximo de unidades disponibles para esta variante.");
    }
}

/**
 * Disminuye la cantidad sin bajar de 1
 */
function disminuirCantidad() {
    const cantidadInput = document.getElementById("cantidad");
    if (!cantidadInput) return;

    let valor = parseInt(cantidadInput.value, 10);

    if (valor > 1) {
        cantidadInput.value = valor - 1;
    }
}

/**
 * Cambia la imagen principal de la galería macro al hacer clic en una miniatura
 * @param {string} url - URL de la imagen seleccionada
 * @param {HTMLElement} elemento - El contenedor .miniatura clickeado
 */
function cambiarImagen(url, elemento) {
    const imgPrincipal = document.getElementById("imagenPrincipal");
    if (imgPrincipal && url) {
        imgPrincipal.src = url;
        
        // Quitar la clase activa de todas las miniaturas y ponérsela a la actual
        document.querySelectorAll('.miniatura').forEach(min => min.classList.remove('activa'));
        elemento.classList.add('activa');
    }
}

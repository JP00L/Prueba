document.addEventListener("DOMContentLoaded", function() {
    var sidebar = document.getElementById("sidebar");
    var toggleButton = document.getElementById("toggle-button");

    // Verifica el estado guardado en localStorage
    var sidebarState = localStorage.getItem('sidebarState');
    if (sidebarState === 'open') {
        sidebar.style.left = '0';
        toggleButton.innerHTML = 'X';
        toggleButton.style.marginLeft = '234px';
        toggleButton.classList.add('open');
    } else {
        sidebar.style.left = '-250px';
        toggleButton.innerHTML = '☰';
        toggleButton.style.marginLeft = '4px';
        toggleButton.classList.remove('open');
    }

    // Añade el evento click para alternar la barra lateral
    toggleButton.addEventListener("click", function() {
        if (sidebar.style.left === "-230px" || sidebar.style.left === "") {
            sidebar.style.left = "0";
            toggleButton.innerHTML = "X";
            toggleButton.style.marginLeft = "234px";
            toggleButton.classList.add('open');
            localStorage.setItem('sidebarState', 'open'); // Guarda el estado en localStorage
        } else {
            sidebar.style.left = "-230px";
            toggleButton.innerHTML = "☰";
            toggleButton.style.marginLeft = "4px";
            toggleButton.classList.remove('open');
            localStorage.setItem('sidebarState', 'closed'); // Guarda el estado en localStorage
        }
    });
});




document.querySelectorAll('.sidebar ul > li > a').forEach(function(item) {
    item.addEventListener("click", function(e) {
        var sublist = this.nextElementSibling;

        // Solo prevenir el comportamiento predeterminado si hay una sublista
        if (sublist && sublist.classList.contains('sublist')) {
            e.preventDefault();

            if (sublist.style.display === "block") {
                sublist.style.display = "none";
            } else {
                sublist.style.display = "block";
            }
        }
    });
});

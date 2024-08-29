document.addEventListener("DOMContentLoaded", function() {
    var sidebar = document.getElementById("sidebar");
    var toggleButton = document.getElementById("toggle-button");
    var loaderOverlay = document.getElementById("loader-overlay");
    var contentSection = document.querySelector(".content");

    // var sidebarState = localStorage.getItem('sidebarState');
    // if (sidebarState === 'open') {
    //     sidebar.style.left = '0';
    //     toggleButton.innerHTML = 'X';
    //     toggleButton.style.marginLeft = '234px';
    //     toggleButton.classList.add('open');
    // } else {
    //     sidebar.style.left = '-250px';
    //     toggleButton.innerHTML = '☰';
    //     toggleButton.style.marginLeft = '4px';
    //     toggleButton.classList.remove('open');
    // }

    toggleButton.addEventListener("click", function() {
        if (sidebar.style.left === "-230px" || sidebar.style.left === "") {
            sidebar.style.left = "0";
            toggleButton.innerHTML = "X";
            toggleButton.style.marginLeft = "234px";
            toggleButton.classList.add('open');
            kcontentSection.classList.add('sidebar-open'); // Añadir la clase cuando se abre el sidebar
            localStorage.setItem('sidebarState', 'open'); 
        } else {
            sidebar.style.left = "-230px";
            toggleButton.innerHTML = "☰";
            toggleButton.style.marginLeft = "4px";
            toggleButton.classList.remove('open');
            // contentSection.classList.remove('sidebar-open'); // Remover la clase cuando se cierra el sidebar
            localStorage.setItem('sidebarState', 'closed');
        }
    });

    document.getElementById('toggle-button').addEventListener('click', function() {
        document.getElementById('sidebar').classList.toggle('collapsed');
        document.querySelector('.content').classList.toggle('expanded');
    });
    document.querySelectorAll('.loader-trigger').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            loaderOverlay.style.display = 'flex';
            
            setTimeout(function() {
                window.location.href = link.href; 
            }, 500);
        });
    });
    document.getElementById('logoutButton').addEventListener('click', function() {
        window.location.href = '/logout';
    });
});

document.querySelectorAll('.sidebar ul > li > a').forEach(function(item) {
    item.addEventListener("click", function(e) {
        var sublist = this.nextElementSibling;
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

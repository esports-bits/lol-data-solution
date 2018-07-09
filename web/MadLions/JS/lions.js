
// ========================= SEARCH COMPETENCIAS =================================

$(document).ready(function(){
        $("#inputCompetencias").on("keyup", function() {
            var value = $(this).val().toLowerCase();

            $("#tablaCompetencias tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });


        });
    });

// ========================= SEARCH EQUIPOS ======================================

$(document).ready(function(){
        $("#inputEquipos").on("keyup", function() {
            var value = $(this).val().toLowerCase();

            $("#tablaEquipos tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });

             
        });
    });

// ========================= SEARCH JUGADORES ====================================

$(document).ready(function(){
        $("#inputJugadores").on("keyup", function() {
            var value = $(this).val().toLowerCase();

            $("#tablaJugadores tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });

             
        });
    });

// ========================  SCROLLBAR ==========================================

$(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();

// ========================  MODALS =============================================

// Get the modal
var competencias = document.getElementById('#modalCompetencias');
var modal_equipos = document.getElementById('#modalEquipos');
var modal_jugadores = document.getElementById('#modalJugadores');
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close-btn-modal")[0];
// Get the submit element that closes the modal and add the new values to the DB
var close = document.getElementsByClassName("btn-primary")[0];

// When the user clicks on the button, open the modal 

//Competencias
$("#btnCompetencias").click(function(){
        
    $("#modalCompetencias").delay(250).fadeIn();    
})

//Equipos
$("#btnEquipos").click(function(){
        
    $("#modalEquipos").delay(250).fadeIn();    
})

//Jugadores
$("#btnJugadores").click(function(){
        
    $("#modalJugadores").delay(250).fadeIn();    
})

// When the user clicks on <span> (x), close the modal

//Competencias
$("#cerrarCompetencia").click(function(){
        
    $("#modalCompetencias").delay(0).fadeOut();    
})

//Equipos
$("#cerrarEquipo").click(function(){
        
    $("#modalEquipos").delay(0).fadeOut();    
})

//Jugadores
$("#cerrarJugador").click(function(){
        
    $("#modalJugadores").delay(0).fadeOut();    
})

// When the user clicks on the button, close the modal

//Competencias
$("#competenciaNueva").click(function(){
        
    $("#modalCompetencias").delay(0).fadeOut();    
})

//Equipos
$("#equipoNuevo").click(function(){
        
    $("#modalEquipos").delay(0).fadeOut();    
})

//Jugadores
$("#jugadorNuevo").click(function(){
        
    $("#modalJugadores").delay(0).fadeOut();    
})

// When the user clicks anywhere outside of the modal, keep it open
window.onclick = function(event) {
    if (event.target == competencias) {
        competencias.style.display = "block"
    }

    else if (event.target == modal_equipos){
        modal_equipos.style.display = "block"
    }

    else if (event.target == modal_jugadores){
        modal_jugadores.style.display = "block"
    }
}


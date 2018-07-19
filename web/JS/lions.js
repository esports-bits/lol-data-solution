
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


// ========================= SEARCH TEMPORADAS ===================================

$(document).ready(function(){
        $("#inputTemporada").on("keyup", function() {
            var value = $(this).val().toLowerCase();

            $("#tablaTemporada tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });


        });
    });

// ========================= SEARCH SPLITS =======================================

$(document).ready(function(){
        $("#inputSplit").on("keyup", function() {
            var value = $(this).val().toLowerCase();

            $("#tablaSplit tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });


        });
    });

// ========================= SEARCH EVENTOS =======================================

$(document).ready(function(){
        $("#inputEvento").on("keyup", function() {
            var value = $(this).val().toLowerCase();

            $("#tablaEvento tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });


        });
    });

// ========================= SEARCH SERIES =======================================

$(document).ready(function(){
        $("#inputSerie").on("keyup", function() {
            var value = $(this).val().toLowerCase();

            $("#tablaSerie tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });


        });
    });

// ========================  SCROLLBAR ===========================================

$(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();

// ========================  MODALS =============================================
$(document).ready(function(){
////////////////////////////////////////////////////////
// When the user clicks on the button, open the modal //
////////////////////////////////////////////////////////

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

//Temporadas
$("#btnTemporada").click(function(){
        
    $("#modalTemporada").delay(250).fadeIn();    
})

//Splits
$("#btnSplit").click(function(){
        
    $("#modalSplit").delay(250).fadeIn();    
})

//Eventos
$("#btnEvento").click(function(){
        
    $("#modalEvento").delay(250).fadeIn();    
})

//Series
$("#btnSerie").click(function(){
        
    $("#modalSerie").delay(250).fadeIn();    
})

//SPartidas
$("#btnPartida").click(function(){
        
    $("#modalPartida").delay(250).fadeIn();    
})
////////////////////////////////////////////////////////
// When the user clicks on <span> (x), close the modal//
////////////////////////////////////////////////////////

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

//Temporadas
$("#cerrarTemporada").click(function(){
        
    $("#modalTemporada").delay(0).fadeOut();    
})

//Splits
$("#cerrarSplit").click(function(){
        
    $("#modalSplit").delay(0).fadeOut();    
})

//Eventos
$("#cerrarEvento").click(function(){
        
    $("#modalEvento").delay(0).fadeOut();    
})

//Series
$("#cerrarSerie").click(function(){
        
    $("#modalSerie").delay(0).fadeOut();    
})

//Partidass
$("#cerrarPartida").click(function(){
        
    $("#modalPartida").delay(0).fadeOut();    
})
////////////////////////////////////////////////////////
// When the user clicks on the button, close the modal//
////////////////////////////////////////////////////////

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

//Temporadas
$("#TemporadaNueva").click(function(){
        
    $("#modalTemporada").delay(0).fadeOut();    
})

//Splits
$("#SplitNuevo").click(function(){
        
    $("#modalSplit").delay(0).fadeOut();    
})

//Eventos
$("#eventoNuevo").click(function(){
        
    $("#modalEvento").delay(0).fadeOut();    
})

//Series
$("#serieNuevo").click(function(){
        
    $("#modalSerie").delay(0).fadeOut();    
})

//Partidas
$("#partidaNuevo").click(function(){
        
    $("#modalPartida").delay(0).fadeOut();    
})

});
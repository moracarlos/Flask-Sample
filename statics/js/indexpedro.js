(function($){
	$.fn.index = function (opciones){
		//$(".cola-cont").hide();
		//Escribir en el dom los hijos
        console.log('Aqui');

		var cola=[];
		var num=0;
		$(".unidades-cont").hide();
		$(".begin-comb").hide();
		$(".cola-cont").hide();
		console.log('hided');
		//unidades = thumbnail(opciones);
		//$(unidades).appendTo(".unidades-cont");
		$(".unidad-click").click(function(){
			if (num<5){
				$('<img src="'+$(this).find("img").attr("src")+'">"').appendTo(".foto-modal"); //La imagen del modal
				$("#basicModal").modal($(document).find(".foto-modal")); //Abre el modal			
				$('#basicModal').on('hidden.bs.modal', function () {
					$(document).find(".foto-modal").find("img").remove(); //Se borra la foto
				});
			}
		});

		$(".boton-seleccionar").click(function(){
				var i=imageselected($('.foto-modal').find("img").attr("src"))
				var selected = ".uni_"+i;
				disponible=$(selected).text(); //Cantidad de unidades disponibles del personaje seleccionado
				var cantidad_seleccionada = $(document).find('.cant_select').find("input").val();
				console.log(disponible-cantidad_seleccionada);
				if(disponible-cantidad_seleccionada>=0 && cantidad_seleccionada!=0){
					$('#add-unidad').append('<div class="unidad-clicked col-lg-3 col-md-3 col-sm-3 col-xs-6"><a href="#" class="thumbnail"><img data-src="holder.js/100%x180" alt="100%x180" src="'+$('.foto-modal').find("img").attr("src")+'"></a>Cantidad: '+cantidad_seleccionada+' </div>');
					num++;
				}
				if(disponible-cantidad_seleccionada<0)
					alert("No puedes seleccionar mas unidades de las que dispones");
				if(cantidad_seleccionada==0)
					alert("Debes seleccionar al menos una unidad de las que dispones");
				
				
					
				if (num==5)
				$(".begin-comb").show();
		});

		$(document).on("click", ".unidad-clicked", function(){ //Para borrar la unidad si le doy click
			$(this).remove();
			num--;
			if (num!=5)
			$(".begin-comb").hide();
		});




		$(".temporal").click(function(){
			$(".oponentes-cont").hide();
			$(".unidades-cont").show();
			$(".cola-cont").show();
			$(".temporal").hide();

		 	for (var i = 4 - 1; i >= 0; i--) {
		 		cola[i]=
		 	};


		});


	};
})(jQuery);

var thumbnail=function (opciones){
	var aux= '';
	aux= '<div class="panel panel-default panel_preparar"><div class="panel-heading">Selecciona tus unidades</div><div class="panel-body"><div class="container unidades"><div class="bs-example "><div class="row">';
				for (j=1; j<=opciones.length; j++){
					aux = aux + '<div class="unidad-click col-lg-3 col-md-3 col-sm-3 col-xs-6"><a href="#" class="thumbnail"><img data-src="holder.js/100%x180" alt="100%x180" src="statics/images/uni_'+j+'.jpg" ></a>Cantidad Disponible:{{uni_'+j+'}}</div>';
				}
				aux = aux + '</div></div></div></div></div>';
	return aux;
};


var imageselected=function (rutaimage){

	if(rutaimage==="statics/images/uni_1.jpg") return 1;
	if(rutaimage==="statics/images/uni_2.jpg") return 2;
	if(rutaimage==="statics/images/uni_3.jpg") return 3;
	if(rutaimage==="statics/images/uni_4.jpg") return 4;
};
(function($){
	$.fn.index = function (opciones){
		var cantidades=[];
		var num=0;
		$(".unidades-cont").hide();
		$(".begin-comb").hide();
		$(".cola-cont").hide();
    	$.ajax({url:"/getOponentes",success:function(result){
      		//result tiene todas las unidades que califican
      		result=jQuery.parseJSON(result);
      		for (j=0; j<result.length; j++){
      			result[j]=jQuery.parseJSON(result[j]);
      			$(".list-group").append('<a href="#" class="list-group-item oponente" style="height: 40px;"> <div class="col-lg-1 col-md-1 col-sm-2 col-xs-1">'+j+'</div> <div class="col-lg-7 col-md-7 col-sm-5 col-xs-4">'+result[j].email+'</div> <div class="col-lg-4 col-md-4 col-sm-5 col-xs-6">'+result[j].puntuacion+'</div></a>');
      		}
      		$(".list-group").show();
   		}});
    	$(document).on("click", ".oponente",function(){
    		$(".oponentes-cont").hide();
    		$(".unidades-cont").show();
    		$(".cola-cont").show();
    		$.ajax({url:"/getUnidades",success:function(result){
    			result=jQuery.parseJSON(result);
      		for (j=0; j<result.length; j++){
      			result[j]=jQuery.parseJSON(result[j]);
      			$(".list-group").append('<a href="#" class="list-group-item oponente" style="height: 40px;"> <div class="col-lg-1 col-md-1 col-sm-2 col-xs-1">'+j+'</div> <div class="col-lg-7 col-md-7 col-sm-5 col-xs-4">'+result[j].email+'</div> <div class="col-lg-4 col-md-4 col-sm-5 col-xs-6">'+result[j].puntuacion+'</div></a>');
      		}
    		}});


    	});

		$(".unidad-click").click(function(){
			if (num==4 && ($(this).find('p').text())=='0'){
				var i=imageselected($(this).find("img").attr("src"))
				$('#add-unidad').append('<div class="unidad-clicked col-lg-3 col-md-3 col-sm-3 col-xs-6"><a href="#" class="thumbnail"><img data-src="holder.js/100%x180" alt="100%x180" src="'+$(this).find("img").attr("src")+'"></a>Cantidad: '+cantidades[i-1]+' </div>');
					num++;
					if (num==5)
				$(".begin-comb").show();
			}
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
				if(disponible-cantidad_seleccionada>=0 && cantidad_seleccionada!=0){
					$('#add-unidad').append('<div class="unidad-clicked col-lg-3 col-md-3 col-sm-3 col-xs-6"><a href="#" class="thumbnail"><img data-src="holder.js/100%x180" alt="100%x180" src="'+$('.foto-modal').find("img").attr("src")+'"></a>Cantidad: '+cantidad_seleccionada+' </div>');
					num++;
					cantidades[i-1] = cantidad_seleccionada;
					$(".uni_"+i).text(disponible-cantidad_seleccionada);
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
			var i=imageselected($(this).find("img").attr("src"));
			var cantidad_seleccionada= $(this).text()[10];
			disponible = $(".uni_"+i).text();
			$(".uni_"+i).text(parseInt(disponible)+parseInt(cantidad_seleccionada));
			num--;
			if (num!=5)
			$(".begin-comb").hide();
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

	if(rutaimage==="../statics/images/uni_1.jpg") return 1;
	if(rutaimage==="../statics/images/uni_2.jpg") return 2;
	if(rutaimage==="../statics/images/uni_3.jpg") return 3;
	if(rutaimage==="../statics/images/uni_4.jpg") return 4;
};
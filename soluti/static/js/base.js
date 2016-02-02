
function verificaTipoPessoa() {
    if ($("#id_eh_pessoa_fisica").is(":checked")) {
        $(".fieldset-pessoa-fisica").show("slow");
        $(".fieldset-pessoa-juridica").hide("slow");
    } else {
        $(".fieldset-pessoa-fisica").hide("slow");
        $(".fieldset-pessoa-juridica").show("slow");
    }
}
function verificaEnderecoCobranca() {
    if ($("#id_cobranca_copiar_endereco").is(":checked")) {
        $("#id_cobranca_copiar_endereco").parent().parent().parent().nextAll(".form-group").hide();
    } else {
        $("#id_cobranca_copiar_endereco").parent().parent().parent().nextAll(".form-group").show();
    }
}
function verificaEnderecoEntrega() {
    if ($("#id_entrega_copiar_endereco").is(":checked")) {
        $("#id_entrega_copiar_endereco").parent().parent().parent().nextAll(".form-group").hide();
    } else {
        $("#id_entrega_copiar_endereco").parent().parent().parent().nextAll(".form-group").show();
    }
}

$(document).ready(function() {

    // Tipo de Pessoa
    verificaTipoPessoa();
	$("#id_eh_pessoa_fisica").change(function(){
        verificaTipoPessoa();
	});

	// Endereço de Cobrança e Entrega
	verificaEnderecoCobranca();
    verificaEnderecoEntrega();
    $("#id_cobranca_copiar_endereco").change(function(){
        verificaEnderecoCobranca();
    });
    $("#id_entrega_copiar_endereco").change(function(){
        verificaEnderecoEntrega();
    });

});

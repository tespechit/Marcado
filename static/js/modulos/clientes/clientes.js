//Formatando os campos telefone e aniversario
jQuery(document).ready(function(){
    jQuery("#cliente_telefone").focus(function(){
        jQuery("#cliente_telefone").mask("(99) 9999-9999");
    });  
    jQuery("#cliente_telefone").click(function(){
        jQuery("#cliente_telefone").mask("(99) 9999-9999");
    });    
    
    jQuery("#cliente_aniversario").focus(function(){
        jQuery("#cliente_aniversario").mask("99/99/9999");
    });       
    jQuery("#cliente_aniversario").click(function(){
        jQuery("#cliente_aniversario").mask("99/99/9999");
    });           
});

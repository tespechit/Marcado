//Formatando os campos telefone e aniversario
jQuery(document).ready(function(){
    jQuery("#auth_user_telefone").focus(function(){
        jQuery("#auth_user_telefone").mask("(99) 9999-9999");
    });
    jQuery("#auth_user_aniversario").focus(function(){
        jQuery("#auth_user_aniversario").mask("99/99/9999");
    });
});

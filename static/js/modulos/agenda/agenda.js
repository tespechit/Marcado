//Formatando os campos data e hora
jQuery(document).ready(function(){
    jQuery("#agenda_data").focus(function(){
        jQuery("#agenda_data").mask("99/99/9999");
    });
    jQuery("#agenda_hora").focus(function(){
        jQuery("#agenda_hora").mask("99:99");
    });

    //Inserindo o calendario
    jQuery("#calendar").fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay',
        },
        editable: true,
        events: [
            {
                "start": "2011-01-18", 
                "id": 3, 
                "title": "Camilla Silva"
            }
        ]
    });
});

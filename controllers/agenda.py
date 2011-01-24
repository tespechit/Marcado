# coding: utf8

def index():
    # Consultando os servicos do usuario logado
    query = db.agenda.id > 0 and db.agenda.funcionario == session.auth.user.id and db.agenda.cliente == db.cliente.id
    agenda = db(query).select(orderby = db.agenda.data)
    teste = []
    
    for ag in agenda:
        result = dict()
        result["id"] = ag.agenda.id
        result["title"] = ag.cliente.nome
        result["start"] = ag.agenda.data.strftime('%Y-%m-%d')
        teste.append(result);
    print teste
    return dict(teste = teste)

def novo():
    return dict(form = crud.create(db.agenda))

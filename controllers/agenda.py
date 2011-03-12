# coding: utf8

def index():
    # Consultando os servicos do usuario logado
    # query = (db.agenda.funcionario == session.auth.user.id) & ()
    query = db.agenda.funcionario == int(session.auth.user.id)
    agenda = db(query).select()

    # Retorna a lista de horarios
    return dict(horarios = agenda)

@auth.requires_login()
def novo():
    return dict(form = crud.create(db.agenda))

@auth.requires_login()
def atualizar():
    # Recupera o primeiro argumento, ou redireciona
    id = request.args(0) or redirect(URL('index'))

    return dict(form = crud.update(db.agenda, id))


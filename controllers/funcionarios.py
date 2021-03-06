# coding: utf8

@auth.requires_login()
def index():
    """
        Exibindo todos os funcionarios 
        cadastrados no sistema
    """
    class Virtual(object):
        @virtualsettings(label=T('Edit'))
        def edit(self):
            return ''

    # Consultando todos os funcionarios cadastrados
    # no sistema
    query = db.auth_user.id > 0
    funcionarios = db(query).select(orderby = db.auth_user.name)

    #Preparando a tabela    
    table = plugins.powerTable
    table.datasource = funcionarios
    table.uitheme = 'le-frog'
    table.dtfeatures['sPaginationType'] = 'scrolling'
    table.keycolumn = 'auth_user.id'  
    table.columns = ['auth_user.name','auth_user.username','auth_user.telefone','auth_user.email']
    table.headers = 'labels'
    table.showkeycolumn = False
    table.dtfeatures['sScrollY'] = '200'
    table.dtfeatures['sScrollX'] = '100%'    
    table.truncate = 120
    table.extra = dict(details={
                    'detailscolumns':'auth_user.id,auth_user.name,auth_user.username,auth_user.telefone,auth_user.email'})
    table.virtualfields = Virtual()
    
    # Caso nao existir nenhum funcionario,
    # mostra a mensagem de erro.
    if funcionarios:
        return dict(funcionarios = funcionarios, table = table.create())
    else:
        return dict(funcionarios = funcionarios, mensagem = T('sem_registros'))

@auth.requires_login()
def novo():
    """
        Exibe o formulario de cadastro de
        funcionarios
    """
    form = crud.create(db.auth_user)
    return dict(form = form)

@auth.requires_login()
def editar():
    """
        Atualiza os dados do funcionario
        selecionado
    """
    # recupera o primeiro argumento ou redireciona
    id = request.args(0) or redirect(URL('index'))
    
    return dict(form = crud.update(db.auth_user, id))

@auth.requires_login()
def show():
    """
        Exibe os detalhes do funcionario
        selecionado
    """
    # recupera o primeiro argumento ou redireciona
    id = request.args(1) or redirect(URL('index'))
    
    # consulta os dados do funcionario selecionado
    query = db.auth_user.id == id
    
    funcionario= db(query).select().first()
    
    # Exibindo na view
    response.view = 'funcionarios/detalhes.html'

    return dict(funcionario = funcionario)

@auth.requires_login()
def pesquisa():
    """
        Efetua a pesquisa com nome do 
        funcionario ou seu login
    """
    # Captura o valor da pesquisa
    palavra_chave = request.vars.nome
    
    # Verifica se o valor esta vazio
    if palavra_chave:
        # Consulta os registros a partir do valor
        query_nome = db.auth_user.name.like('%'+palavra_chave+'%')
        query_username = db.auth_user.username.like('%'+palavra_chave+'%')
        resultado = db(query_nome and query_username or db.auth_user.aniversario <= request.now).select()
        
        # Define qual view sera renderizada
        response.view = 'funcionarios/index.html'
        
        # Se encontrou alguma coisa, exibe o resultado
        # da pesquisa, senao enviar mensagem que nao
        # foi encontrado nada.
        if resultado:
            return dict(funcionarios = resultado)
        else:
            return dict(funcionarios = resultado, mensagem = T('nao_encontrado'))        
    else:
        # Define e view que sera renderizada
        response.view = 'funcionarios/index.html'
        
        # consulta todos os clientes
        query = db.auth_user > 0 and db.auth_user.aniversario <= request.now
        resultado = db(query).select()
        
        if resultado:
            return dict(funcionarios = resultado)
        else:
            return dict(funcionarios = resultado, mensagem = T('sem_registros'))

@auth.requires_login()
def excluir():
    """
        Exclui o cliente selecionado
    """
    #recupera o primeiro argumento, ou redireciona
    id = request.args(0) or redirect(URL('index'))
    
    # exclui o registro
    funcionario = db(db.auth_user.id == int(id)).delete()

    # Define a view que vai ser renderizada
    response.view = 'funcionarios/index.html'
    
    if funcionario:
        # Mostra mensagem de sucesso e redireciona para a lista de clientes
        redirect(URL(request.application, 'funcionarios','index'))
        response.flash = T('excluido')
    else:
        redirect(URL(request.application, 'funcionarios','index'))
        response.flash = T('excluido')

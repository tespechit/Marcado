# coding: utf8

@auth.requires_login()
def index():
    """
        Lista todos os clientes cadastrados
    """    
    
    class Virtual(object):
        @virtualsettings(label=T('Edit'))
        def edit(self):
            return ''

    # Consultando todos os clientes
    query = db.cliente.id > 0 or db.cliente.aniversario <= request.now
    clientes = db(query).select(orderby=db.cliente.nome)
    
    #Preparando a tabela    
    table = plugins.powerTable
    table.datasource = db.cliente
    table.uitheme = 'le-flog'
    table.dtfeatures['sPaginationType'] = 'scrolling'
    table.keycolumn = 'cliente.id'  
    table.columns = ['cliente.nome','cliente.endereco','cliente.telefone']
    table.headers = 'labels'
    table.dtfeatures['sScrollY'] = '200'
    table.dtfeatures['sScrollX'] = '100%'
    table.showkeycolumn = False
    table.truncate = 120
    table.extra = dict(details={'detailscolumns':'cliente.id,cliente.nome,cliente.endereco,cliente.telefone,cliente.email,cliente.aniversario'})
    table.virtualfields = Virtual()

    
    # Caso nao tiver nenhum registro mostrar mensagem
    if clientes:
        # Retornando os registros
        return dict(clientes=clientes, table = table.create())        
    else:
        return dict(clientes = clientes, mensagem = T('sem_registros'))

@auth.requires_login()
def novo():
    """
        Exibe o formulario de cadastro dos clientes
    """
    return dict(form = crud.create(db.cliente))


@auth.requires_login()
def editar():
    """
        Exibe o formulario de edicao com os dados
        do cliente selecionado
    """
    #recupera o primeiro argumento, ou redireciona
    id = request.args(0) or redirect(URL('index'))
    
    return dict(form = crud.update(db.cliente, id))

@auth.requires_login()
def show():    
    """
        Exibe os detalhes do cliente selecionado
    """
    #recupera o primeiro argumento, ou redireciona
    id = request.args(1) or redirect(URL('index'))

    # Consulta o cliente selecionado
    query = db.cliente.id == int(id)
    
    # Renderiza na pagina especificada
    response.view = 'clientes/detalhes.html'

    return dict(cliente = db(query).select().first())

@auth.requires_login()
def pesquisa():
    """
        Efetua a pesquisa dos clientes
        a partir do seu nome
    """
    # Captura o valor do campo de pesquisa
    palavra_chave = request.vars.nome

    # Verifica se o campo esta vazio
    if palavra_chave:
        # Consulta os resultados da pesquisa
        query = db.cliente.nome.like('%'+palavra_chave+'%')
        resultado = db(query or db.cliente.aniversario <= request.now).select()
    
        # Define qual view sera renderizada
        response.view = 'clientes/index.html'
    
        # Se encontrou alguma coisa, exibe o resultado
        # da pesquisa, senao enviar mensagem que nao
        # foi encontrado nada.
        if resultado:
            return dict(clientes = resultado)
        else:
            msg = T('nao_encontrado')
            return dict(clientes = resultado, mensagem = msg)
    else:
        # Define a view que sera renderizada
        response.view = 'clientes/index.html'
    
        # consulta todos os clientes
        query = db.cliente.id > 0 and db.cliente.aniversario <= request.now
        
        # verifica se trouxe registros
        clientes = db(query).select()
        if clientes:
            return dict(clientes = clientes)
        else:
            return dict(clientes = clientes, mensagem = T('sem_registros')) 
        
@auth.requires_login()
def excluir():
    """
        Exclui o cliente selecionado
    """
    #recupera o primeiro argumento, ou redireciona
    id = request.args(0) or redirect(URL('index'))
    
    # exclui o registro
    cliente = db(db.cliente.id == int(id)).delete()

    # Define a view que vai ser renderizada
    response.view = 'clientes/index.html'
    
    if cliente:
        # Mostra mensagem de sucesso e redireciona para a lista de clientes
        redirect(URL(request.application, 'clientes','index'))
        response.flash = T('excluido')
    else:
        redirect(URL(request.application, 'clientes','index'))
        response.flash = T('excluido')

@service.json
def teste():
    return ["Segunda","Terça","Quarta","Quinta","Sexta"]

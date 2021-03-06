# coding: utf8

def index(): 
    """
        Retorna todos os serviços cadastrados.
        Esses serviços serão usados no módulo de Agendas
        para agendar os serviços dos clientes.
    """

    class Virtual(object):
        @virtualsettings(T('Edit'))
        def edit(self):
            return ''

    query = db.servicos.id > 0
    
    servicos = db(query).select(orderby = db.servicos.servico)
    
    table = plugins.powerTable
    table.datasource = servicos
    table.uitheme = 'le-frog'
    table.dtfeatures['sPaginationType'] = 'scrolling'
    table.columns = ['servicos.servico','servicos.preco']
    table.keycolumn = 'servicos.id'
    table.headers = 'labels'
    table.showkeycolumn = False
    table.dtfeatures['sScrollY'] = '200'
    table.dtfeatures['sScrollX'] = '100%'    
    table.extra = dict(details={'detailscolumns':'servicos.id,servicos.servico,servicos.preco,servicos.observacoes'})
    table.virtualfields = Virtual()   
    
    # Verifica se existem dados para ser retornados
    if servicos:
        return dict(servicos=servicos, table=table.create())
    else:
        return dict(servicos = servicos, mensagem = T('sem_registros'))

def novo():
    """
        Retorna o formulario de cadastro
        dos servicos.
    """
    return dict(form = crud.create(db.servicos))

def show():
    """
        Captura o registro selecionado e exibe
        seus dados detalhadamente.
    """
    # Captura a identificacao ou redireciona para a lista
    # de servicos
    id = request.args(1) or redirect(URL('index'))
    
    # consulta os dados do servico
    query = db.servicos.id == id
    
    servico = db(query).select().first()
   
    # renderiza a view
    response.view = 'servicos/detalhes.html'

    # retorna para pagina
    return dict(servico = servico)

def editar():
    """
        Captura o registro selecionado
        e atualiza seus dados no banco de dados.
    """
    # Captura a identificacao ou redireciona para a lista
    # de servicos
    id = request.args(0) or redirect(URL('index'))
    
    # redirecionna para outra pagina
    response.view = 'servicos/novo.html'
    
    # retorna com o formulario de edicao
    return dict(form = crud.update(db.servicos, id))
    
def excluir():
    """
        Exclui o servico selecionado
    """
    #recupera o primeiro argumento, ou redireciona
    id = request.args(0) or redirect(URL('index'))
    
    # exclui o registro
    servico = db(db.servicos.id == int(id)).delete()

    # Define a view que vai ser renderizada
    response.view = 'servicos/index.html'
    
    if servico:
        # Mostra mensagem de sucesso e redireciona para a lista de clientes
        redirect(URL(request.application, 'servicos','index'))
        response.flash = T('excluido')
    else:
        redirect(URL(request.application, 'servicos','index'))
        response.flash = T('excluido')

# coding: utf8
import datetime

"""
###################################################################################
##                            Tabela de Funcionarios
##  Esse cadastro e usado para inserir os dados do funcionario
##  como tambem para acessar o sistema.
###################################################################################
"""

db.define_table(
    auth.settings.table_user_name,
    Field('name', length=128, default=''),
    Field('username', length = 128, default = '', unique = True),
    Field('email', length=128, default=''),
    Field('password', 'password', length=512,
          readable=False, label='Password'),
    Field('endereco', notnull = True),
    Field('telefone', notnull = True),
    Field('aniversario', 'date', notnull = True, default=request.now),
    Field('registration_key', length=512,
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,
          writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.name.requires = IS_NOT_EMPTY(error_message= T('is_empty'))
custom_auth_table.username.requires = [
            IS_NOT_EMPTY(error_message = T('is_empty')),
            IS_NOT_IN_DB(db, custom_auth_table.username)
]
custom_auth_table.password.requires = [
            # Especifica a complexidade da senha
            IS_STRONG(min = 6, special = 0, upper = 0),
            CRYPT()]
custom_auth_table.email.requires = [
            IS_EMAIL(error_message=auth.messages.invalid_email)]

custom_auth_table.endereco.requires = IS_NOT_EMPTY(error_message = T('is_empty'))
custom_auth_table.telefone.requires = IS_NOT_EMPTY(error_message = T('is_empty'))
custom_auth_table.aniversario.requires = [
            IS_NOT_EMPTY(error_message = T('is_empty')),
            IS_DATE_IN_RANGE(minimum = datetime.date(1900,1,1),
            maximum = datetime.date(9999,12,31),
            format=T('%d/%m/%Y'),
            error_message = 'O formato deve ser 00/00/0000')
        ]

# Definindo os rotulos dos campos OBS.: Alterar o rotulo e inserir a mensagem no pt-br.py
custom_auth_table.name.label = T('nome_funcionario')
custom_auth_table.username.label = T('login')
custom_auth_table.email.label = T('email')
custom_auth_table.password.label = T('senha')
custom_auth_table.endereco.label = T('endereco')
custom_auth_table.telefone.label = T('telefone')

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table

# before
auth.define_tables(username = True)

"""
###################################################################################
##                            Tabela de Clientes
##  Esse cadastro e usado para inserir os dados do cliente
##  para ser usado na agenda.
###################################################################################
"""

db.define_table('cliente',
            Field('nome',unique=True,notnull=True),
            Field('endereco',notnull=True),
            Field('telefone',notnull=True),
            Field('email',notnull=True),
            Field('aniversario','date',notnull=True)
            )

# Validando os campos
db.cliente.nome.requires = [
            IS_NOT_EMPTY(error_message = T('empty')),
            IS_NOT_IN_DB(db, 'cliente.nome', error_message = T('is_not_db'))
        ]
db.cliente.endereco.requires = [
            IS_NOT_EMPTY(error_message = T('empty'))
        ]
db.cliente.telefone.requires = [
            IS_NOT_EMPTY(error_message = T('empty'))
]
db.cliente.email.requires = [
            IS_NOT_EMPTY(error_message = T('empty')),
            IS_EMAIL(error_message = T('is_email'))
        ]        
db.cliente.aniversario.requires = [
            IS_NOT_EMPTY(error_message = T('empty')),
            IS_DATE_IN_RANGE(minimum = datetime.date(1900,1,1),
            maximum = datetime.date(9999,12,31),
            format=T('%d/%m/%Y'),
            error_message = 'O formato deve ser 00/00/0000')
        ]
        
"""
###################################################################################
##                            Tabela de Serviços
##  Esse cadastro e usado para cadastrar os serviços usados no comerio.
##
###################################################################################
"""        
        
db.define_table('servicos',
        Field('servico', unique = True, notnull = True, default = ''),
        Field('preco','decimal(3,2)'),
        Field('observacoes','text', length = 150)
    )
    
# Validando os campos
db.servicos.servico.requires = [
            IS_NOT_EMPTY(error_message = T('is_empty')),
            IS_NOT_IN_DB(db, 'servicos.servico', error_message = T('is_not_db'))
    ]
db.servicos.preco.requires = IS_NOT_EMPTY(error_message = T('is_empty'))
db.servicos.observacoes.requires = IS_LENGTH(150, error_message = T('is_max'))

# Inserindo os rotulos
db.servicos.servico.label = T('servico')
db.servicos.preco.label = T('preco')
db.servicos.observacoes.label = T('observacoes')        
        
        
"""
###################################################################################
##                            Tabela de Agenda
##  Esse cadastro e usado para inserir a agenda dos clientes
##  relacionado a cada funcionario.
###################################################################################
"""        
        
db.define_table('agenda',
        Field('funcionario',db.auth_user , notnull = True),
        Field('cliente',db.cliente, notnull = True),
        Field('tipo_servico',db.servicos, notnull = True),
        Field('data', 'date', notnull = True, default = request.now),
        Field('hora', 'time', notnull = True),
        Field('observacoes','text', length = 200)
    )
        
# Validando os campos da tabela Agenda
db.agenda.funcionario.requires = IS_IN_DB(db, 'auth_user.id', 'auth_user.name', zero='-- Escolha um funcionário --')
db.agenda.cliente.requires = IS_IN_DB(db, 'cliente.id', 'cliente.nome', zero='-- Escolha um cliente --')
db.agenda.tipo_servico.requires = IS_IN_DB(db, 'servicos.id', 'servicos.servico', zero='-- Escolha um servico --')
db.agenda.observacoes.requires = IS_LENGTH(200, error_message = T('is_max'))
db.agenda.data.requires = [
        IS_NOT_EMPTY(error_message = T('is_empty')),
        IS_DATE_IN_RANGE(minimum = datetime.date(1900,1,1),
            maximum = datetime.date(9999,12,31),
            format=T('%d/%m/%Y'))
        ] 

# Rotulando os campos
db.agenda.funcionario.label = T('nome_funcionario')
db.agenda.tipo_servico.label= T('servico')
db.agenda.observacoes.label = T('observacoes')

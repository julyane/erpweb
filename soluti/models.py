# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from djangoplus.db import models
from djangoplus.decorators import subset, action, attr
from djangoplus.forms import ValidationError
from djangoplus.contrib.site.models import Unit, User
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.db.models import F, Sum


class CategoriaCnh:
    NAO_POSSUI = u'Não possui habilitação'
    A = u'A'
    B = u'B'
    AB = u'AB'
    C = u'C'
    AC = u'AC'
    D = u'D'
    AD = u'AD'
    E = u'E'
    AE = u'AE'

    CATEGORIACNH_CHOICES = [
        (NAO_POSSUI, u'Não possui habilitação'),
        (A, u'A'),
        (B, u'B'),
        (AB, u'AB'),
        (C, u'C'),
        (AC, u'AC'),
        (D, u'D'),
        (AD, u'AD'),
        (E, u'E'),
        (AE, u'AE'),
    ]


class DiasSemana:
    SEGUNDA = u'Segunda'
    TERCA = u'Terça'
    QUARTA = u'Quarta'
    QUINTA = u'Quinta'
    SEXTA = u'Sexta'

    DIASSEMANA_CHOICES = [
        (SEGUNDA, u'Segunda'),
        (TERCA, u'Terça'),
        (QUARTA, u'Quarta'),
        (QUINTA, u'Quinta'),
        (SEXTA, u'Sexta'),
    ]


class RegimeTributario:
    SIMPLES = u'Simples Nacional'
    PRESUMIDO = u'Lucro Presumido'
    REAL = u'Lucro Real'

    REGIMETRIBUTARIO_CHOICES = [
        (SIMPLES, u'Simples Nacional'),
        (PRESUMIDO, u'Lucro Presumido'),
        (REAL, u'Lucro Real'),
    ]


class Sexo:
    MASCULINO = u'Masculino'
    FEMININO = u'Feminino'

    SEXO_CHOICES = [
        (MASCULINO, u'Masculino'),
        (FEMININO, u'Feminino'),
    ]


class Atividade(models.Model):
    descricao = models.CharField(u'Descrição', unique=True, blank=False)

    class Meta:
        verbose_name = u'Atividade'
        verbose_name_plural = u'Atividades'
        ordering = ('descricao',)
        can_admin=['Administrador']
        menu = u'Vendas::Atividades'

    def __unicode__(self):
        return self.descricao


class Cargo(models.Model):
    descricao = models.CharField(u'Descrição', unique=True, blank=False)

    class Meta:
        verbose_name = u'Cargo'
        verbose_name_plural = u'Cargos'
        ordering = ('descricao',)
        can_admin = ['Administrador']
        menu = u'Recursos Humanos::Cargos'

    def __unicode__(self):
        return self.descricao


class Estado(models.Model):
    nome = models.CharField(u'Nome', unique=True, blank=False)

    class Meta:
        verbose_name = u'Estado'
        verbose_name_plural = u'Estados'
        ordering = ('nome',)
        can_admin = ['Administrador']
        menu = u'Administração::Cadastros::Estados', 'fa-list'

    def __unicode__(self):
        return self.nome


class Cidade(models.Model):
    nome = models.CharField(u'Nome', unique=True, blank=False)
    estado = models.ModelChoiceField(Estado, null=False)

    class Meta:
        verbose_name = u'Cidade'
        verbose_name_plural = u'Cidades'
        ordering = ('nome',)
        can_admin = ['Administrador']
        menu = u'Administração::Cadastros::Cidades'

    def __unicode__(self):
        return self.nome


class FormaPagamento(models.Model):
    descricao = models.CharField(u'Descrição', unique=True, blank=False)

    class Meta:
        verbose_name = u'Forma de Pagamento'
        verbose_name_plural = u'Formas de Pagamento'
        ordering = ('descricao',)
        can_admin = ['Administrador']
        menu = u'Vendas::Formas de Pagamento'

    def __unicode__(self):
        return self.descricao


class GrupoEconomico(models.Model):
    descricao = models.CharField(u'Descrição', unique=True, blank=False)

    class Meta:
        verbose_name = u'Grupo Econômico'
        verbose_name_plural = u'Grupos Econômicos'
        ordering = ('descricao',)
        can_admin = ['Administrador']
        menu = u'Clientes::Grupos Econômicos'

    def __unicode__(self):
        return self.descricao


class Empresa(Unit):
    nome = models.CharField(u'Nome Fantasia', blank=False)
    razao_social = models.CharField(u'Razão Social', blank=False)

    cnpj = models.CnpjField(u'CNPJ', blank=True)
    isentoinscricaoestadual = models.BooleanField(u'Isento de Inscrição Estadual', default=False, blank=True)
    inscricaoestadual = models.CharField(u'Inscrição Estadual', max_length=8, blank=True)
    inscricaomunicipal = models.CharField(u'Inscrição Municipal', max_length=14, blank=True)

    endereco = models.AddressField(u'Endereço', max_length=255)
    complemento = models.CharField(u'Complemento', max_length=255, blank=True)
    pontoreferencia = models.CharField(u'Ponto de Referência', max_length=255, blank=True)
    bairro = models.CharField(u'Bairro', max_length=255)
    estado = models.ModelChoiceField(Estado)
    cidade = models.ModelChoiceField(Cidade, form_filter=('estado', 'estado'))
    cep = models.CepField(u'CEP')

    telefone = models.PhoneField(u'Telefone')
    telefone2 = models.PhoneField(u'Outro Telefone', blank=True)
    celular = models.PhoneField9(u'Celular', blank=True)
    email = models.EmailField(u'E-mail', max_length=255, blank=False)

    fieldsets = ((u'Dados Gerais', {'fields': (('nome', 'razao_social'),
                                               ('cnpj', 'isentoinscricaoestadual', 'inscricaoestadual', 'inscricaomunicipal'),)}),
                 (u'Endereço', {'fields': ('endereco', ('complemento', 'pontoreferencia', 'bairro', 'cep'), ('estado', 'cidade'),)}),
                 (u'Contatos', {'fields': (('telefone', 'telefone2', 'celular', 'email'),)}),
    )

    class Meta:
        verbose_name = u'Empresa'
        verbose_name_plural = u'Empresas'
        ordering = ('nome', 'cnpj', 'telefone')
        unit_lookup = 'id'
        can_admin = ['Administrador']
        menu = u'Administração::Cadastros::Empresas'

    def __unicode__(self):
        return self.nome

    def save(self, *args, **kargs):
        if self.isentoinscricaoestadual:
            self.inscricaoestadual = u''

        super(Empresa, self).save(*args, **kargs)


class Setor(models.Model):
    descricao = models.CharField(u'Descrição', unique=True, blank=False)

    class Meta:
        verbose_name = u'Setor'
        verbose_name_plural = u'Setores'
        ordering = ('descricao',)
        can_admin = ['Administrador']
        menu = u'Recursos Humanos::Setores'

    def __unicode__(self):
        return self.descricao


## MODULO DE FORNECEDORES

class Fornecedor(models.Model):
    # Dados gerais
    empresa = models.ModelChoiceField(Empresa, filter=True)
    nome = models.CharField(u'Nome')
    atividade = models.ModelChoiceField(Atividade)
    eh_pessoa_fisica = models.BooleanField(u'É Pessoa Física?', default=False, filter=True)

    # Pessoa Fisica
    cpf = models.CpfField(u'CPF', blank=True)
    rg = models.CharField(u'RG', blank=True)

    # Pessoa Juridica
    nome_fantasia = models.CharField(u'Nome Fantasia', blank=True)
    cnpj = models.CnpjField(u'CNPJ', blank=True)
    inscricaoestadual = models.CharField(u'Inscrição Estadual', max_length=8, blank=True)
    isentoinscricaoestadual = models.BooleanField(u'Isento de Inscrição Estadual', default=False, blank=True)
    inscricaomunicipal = models.CharField(u'Inscrição Municipal', max_length=14, blank=True)

    # Endereço
    endereco = models.AddressField(u'Endereço', max_length=255)
    complemento = models.CharField(u'Complemento', max_length=255)
    pontoreferencia = models.CharField(u'Ponto de Referência', max_length=255)
    bairro = models.CharField(u'Bairro', max_length=255)
    estado = models.ModelChoiceField(Estado)
    cidade = models.ModelChoiceField(Cidade, form_filter=('estado', 'estado'), filter=True)
    cep = models.CepField(u'CEP')

    # Contatos
    telefone = models.PhoneField(u'Telefone')
    celular = models.PhoneField9(u'Celular', null=True, blank=True)
    email = models.EmailField(u'E-mail', max_length=255)
    site = models.CharField(u'Site', null=True, blank=True)

    # Outros
    ativo = models.BooleanField(u'Ativo', default=True, filter=True)
    observacao = models.TextField(u'Observação', null=True, blank=True)
    data_cadastro = models.DateField(u'Data de Cadastro', auto_now_add=True, exclude=True)

    fieldsets = ((u'Dados gerais', {'fields': ('nome', ('atividade', 'empresa'), 'eh_pessoa_fisica')}),
                 (u'Pessoa Física', {'fields': ('cpf', 'rg',)}),
                 (u'Pessoa Jurídica', {'fields': ('nome_fantasia', 'cnpj',
                                                  ('isentoinscricaoestadual', 'inscricaoestadual', 'inscricaomunicipal'),)}),
                 (u'Endereço', {'fields': ('endereco', ('complemento', 'pontoreferencia'), ('bairro', 'cep'), ('estado', 'cidade'),)}),
                 (u'Contatos', {'fields': (('telefone', 'celular', 'email', 'site'),)}),
                 (u'Dados Complementares', {'fields': ('ativo', 'observacao', 'data_cadastro')}),
    )

    class Meta:
        verbose_name = u'Fornecedor'
        verbose_name_plural = u'Fornecedores'
        ordering = ('nome',)
        list_display=['id', 'nome', 'telefone']
        unit_field = 'empresa'
        can_admin = ['Administrador',]
        menu = u'Compras::Fornecedores'

    def __unicode__(self):
        return self.nome

    def clean(self):
        if self.eh_pessoa_fisica:
            if not self.cpf:
                raise ValidationError(u'Preencha o campo CPF')
            elif not self.rg:
                raise ValidationError(u'Preencha o campo RG')
        else:
            if not self.cnpj:
                raise ValidationError(u'Preencha o campo CNPJ')
            elif not self.isentoinscricaoestadual and not self.inscricaoestadual:
                raise ValidationError(u'Preencha o campo Inscrição Estadual')

        if self.eh_pessoa_fisica and self.cpf:
            cpfs = Fornecedor.objects.filter(cpf=self.cpf)
            if self.pk:
                cpfs = cpfs.exclude(pk=self.pk)
            if cpfs.exists():
                raise ValidationError(u'Já existe um cliente cadastrado com este CPF')

        if not self.eh_pessoa_fisica and self.cnpj:
            cnpjs = Fornecedor.objects.filter(cnpj=self.cnpj)
            if self.pk:
                cnpjs = cnpjs.exclude(pk=self.pk)
            if cnpjs.exists():
                raise ValidationError(u'Já existe um cliente cadastrado com este CNPJ')

    def save(self, *args, **kargs):
        if self.eh_pessoa_fisica:
            self.nome_fantasia = u''
            self.cnpj = u''
            self.isentoinscricaoestadual = False
            self.inscricaoestadual =  u''
            self.inscricaomunicipal = u''
        else:
            self.cpf = u''
            self.rg = u''

        if self.isentoinscricaoestadual:
            self.inscricaoestadual = u''

        super(Fornecedor, self).save(*args, **kargs)


## MODULO ESTOQUE

class CSTICMSTabelaA:
    NACIONAL_0 = u'0'
    ESTRANGEIRA_1 = u'1'
    ESTRANGEIRA_2 = u'2'
    NACIONAL_3 = u'3'
    NACIONAL_4 = u'4'
    NACIONAL_5 = u'5'
    ESTRANGEIRA_6 = u'6'
    ESTRANGEIRA_7 = u'7'

    CSTICMSTABELAA_CHOICES = [
        (NACIONAL_0, u'0 – Nacional, exceto as indicadas nos códigos 3 a 5'),
        (ESTRANGEIRA_1, u'1 – Estrangeira – importação direta, exceto a indicada no código 6'),
        (ESTRANGEIRA_2, u'2 – Estrangeira – adquirida no mercado interno, exceto a indicada no código 7'),
        (NACIONAL_3, u'3 – Nacional, mercadoria ou bem com conteúdo de importação superior a 40% (quarenta por cento)'),
        (NACIONAL_4, u'4 – Nacional, cuja produção tenha sido feita em conformidade com os processos produtivos básicos de que tratam o Decreto-Lei nº 288, de 28 de fevereiro de 1967, a Lei federal        nº 8.248, de 23 de outubro de 1991, a Lei federal nº 8.387, de 30 de dezembro de 1991, a Lei federal nº 10.176, de 11 de janeiro de 2001 e a Lei federal nº 11.484, de 31 de maio de 2007'),
        (NACIONAL_5, u'5 – Nacional, mercadoria ou bem com conteúdo de importação inferior ou igual a 40% (quarenta por cento)'),
        (ESTRANGEIRA_6, u'6 – Estrangeira – importação direta, sem similar nacional, constante em lista de resolução do Conselho de Ministros da Câmara de Comércio Exterior (CAMEX)'),
        (ESTRANGEIRA_7, u'7 – Estrangeira – adquirida no mercado interno, sem similar nacional, constante em lista de resolução do CAMEX'),
    ]


class CSTICMSTabelaB:
    OPCAO_00 = u'00'
    OPCAO_10 = u'10'
    OPCAO_20 = u'20'
    OPCAO_30 = u'30'
    OPCAO_40 = u'40'
    OPCAO_41 = u'41'
    OPCAO_50 = u'50'
    OPCAO_51 = u'51'
    OPCAO_60 = u'60'
    OPCAO_70 = u'70'
    OPCAO_90 = u'90'

    CSTICMSTABELAB_CHOICES = [
        (OPCAO_00, u'00 - Tributada integralmente'),
        (OPCAO_10, u'10 - Tributada e com cobrança do ICMS por substituição tributária'),
        (OPCAO_20, u'20 - Com redução de base de cálculo'),
        (OPCAO_30, u'30 - Isenta ou não tributada e com cobrança do ICMS por substituição tributária'),
        (OPCAO_40, u'40 - Isenta'),
        (OPCAO_41, u'41 - Não tributada'),
        (OPCAO_50, u'50 - Suspensão'),
        (OPCAO_51, u'51 - Diferimento'),
        (OPCAO_50, u'60 - ICMS cobrado anteriormente por substituição tributária'),
        (OPCAO_70, u'70 - Com redução de base de cálculo e cobrança do ICMS por substituição tributária'),
        (OPCAO_90, u'90 - Outras'),
    ]


class AliquotaICMS(models.Model):
    descricao = models.CharField(u'Descrição')
    valor = models.PositiveIntegerField(help_text=u'Em %')

    class Meta:
        ordering = ['descricao']
        verbose_name = u"Alíquota de ICMS"
        verbose_name_plural = u"Alíquotas de ICMS"
        menu = u'Fiscal::Alíquotas de ICMS', 'fa-percent'

    def __unicode__(self):
        return u"%s (%s)" % (self.descricao, self.valor)


class AliquotaIPI(models.Model):
    descricao = models.CharField(u'Descrição')
    valor = models.PositiveIntegerField(help_text=u'Em %') #max_value=99

    class Meta:
        ordering = ['descricao']
        verbose_name = u"Alíquota de IPI"
        verbose_name_plural = u"Alíquotas de IPI"
        menu = u'Fiscal::Alíquotas de IPI'

    def __unicode__(self):
        return u"%s (%s)" % (self.descricao, self.valor)


class CFOP(models.Model):
    descricao = models.CharField(u'Descrição')
    valor = models.PositiveIntegerField() #max_value=9999

    class Meta:
        ordering = ['descricao']
        verbose_name = u"CFOP"
        verbose_name_plural = u"CFOP"
        menu = u'Fiscal::CFOP'

    def __unicode__(self):
        return u"%s - %s" % (self.valor, self.descricao)


class Fabricante(models.Model):
    descricao = models.CharField(u'Descrição')

    class Meta:
        ordering = ['descricao']
        verbose_name = u"Fabricante"
        verbose_name_plural = u"Fabricantes"
        menu = u'Estoque::Fabricantes'

    def __unicode__(self):
        return self.descricao


class GrupoProduto(models.Model):
    descricao = models.CharField(u'Descrição', unique=True, blank=False, search=True)

    class Meta:
        verbose_name = u'Grupo de Produtos'
        verbose_name_plural = u'Grupos de Produtos'
        ordering = ('descricao',)
        can_admin = ['Administrador']
        menu = u'Estoque::Grupos de Produtos'

    def __unicode__(self):
        return self.descricao


class SubGrupoProduto(models.Model):
    grupo = models.ModelChoiceField(GrupoProduto, null=False)
    descricao = models.CharField(u'Descrição', unique=True, blank=False, search=True)

    class Meta:
        verbose_name = u'Subgrupo de Produtos'
        verbose_name_plural = u'Subgrupos de Produtos'
        ordering = ('descricao',)
        can_admin = ['Administrador']
        menu = u'Estoque::Subgrupos de Produtos'

    def __unicode__(self):
        return self.descricao


class TipoEstoque(models.Model):
    empresa = models.ModelChoiceField(Empresa, filter=True)
    descricao = models.CharField(u'Descrição')

    class Meta:
        verbose_name = u"Tipo de Estoque"
        verbose_name_plural = u"Tipos de Estoque"
        ordering = ['descricao']
        menu = u'Estoque::Tipos de Estoque'

    def __unicode__(self):
        return self.descricao


class UnidadeMedida(models.Model):
    descricao = models.CharField(u'Descrição')
    representacao = models.CharField(u'Representação da Unidade')

    class Meta:
        verbose_name = u"Unidade de Medida"
        verbose_name_plural = u"Unidades de Medidas"
        ordering = ['descricao', 'representacao']
        menu = u'Estoque::Unidades de Medida'

    def __unicode__(self):
        return u'%s (%s)' % (self.descricao, self.representacao)


class ProdutoManager(models.Manager):
    @subset(u'Abaixo do Estoque Mínimo', observe=True)
    def abaixo_estimo(self):
        return self.filter(estoque_atual__lt=F('estoque_minimo'))


class Produto(models.Model):
    empresa = models.MultipleModelChoiceField(Empresa, help_text=u"Selecione uma ou mais empresas", filter=True)
    fabricante = models.ModelChoiceField(Fabricante, null=True, filter=True)
    titulo = models.CharField(u'Título', unique=True, blank=False, search=True)
    descricao = models.TextField(u'Descrição', blank=False, search=True)
    modelo = models.CharField(blank=False, search=True)
    valor = models.DecimalField(u'Preço de Venda', blank=False)
    preco_custo = models.DecimalField(u'Preço de Custo', blank=True)
    peso = models.DecimalField(blank=True)

    tipoestoque = models.ModelChoiceField(TipoEstoque, filter=True)
    estoque_atual = models.PositiveIntegerField(u'Estoque Atual')
    estoque_minimo = models.PositiveIntegerField(u'Estoque Mínimo')

    aliquotaicms = models.ModelChoiceField(AliquotaICMS, verbose_name=u'ICMS', null=True, blank=True, filter=True)
    aliquotaipi = models.ModelChoiceField(AliquotaIPI, verbose_name=u'IPI', null=True, blank=True, filter=True)
    cfop = models.ModelChoiceField(CFOP, verbose_name=u'CFOP', null=True, blank=True, filter=True)
    ncm = models.CharField(u'NCM', blank=False)
    cst_a = models.CharField(u'CST - Tabela A', choices=CSTICMSTabelaA.CSTICMSTABELAA_CHOICES, blank=True, filter=True)
    cst_b = models.CharField(u'CST - Tabela B', choices=CSTICMSTabelaB.CSTICMSTABELAB_CHOICES, blank=True, filter=True)

    ativo = models.BooleanField(default=True, filter=True)
    garantia = models.DateField(u'Garantia do Fornecedor/Fabricante', null=True, blank=True)
    garantia_cliente = models.PositiveIntegerField(u'Garantia para Cliente', null=True, blank=True, help_text=u'Em dias')
    fornecedor = models.ModelChoiceField(Fornecedor, null=True, blank=True)
    unidade = models.ModelChoiceField(UnidadeMedida, null=False, filter=True)

    objects = ProdutoManager()

    fieldsets = ((u'Dados Gerais', {'fields': ('empresa', 'titulo', 'descricao', ('fabricante', 'modelo', 'peso'), ('valor', 'preco_custo', 'get_margem_lucro'))}),
                 (u'Estoque', {'fields': (('tipoestoque', 'estoque_atual', 'estoque_minimo'),)}),
                 (u'Dados Fiscais', {'fields': (('aliquotaicms', 'aliquotaipi', 'cfop', 'ncm'), ('cst_a', 'cst_b'),)}),
                 (u'Dados Complementares', {'fields': ('ativo', ('garantia', 'garantia_cliente', 'fornecedor',), 'unidade',)}),
                 )

    class Meta:
        verbose_name = u'Produto'
        verbose_name_plural = u'Produtos'
        list_display = ['titulo', 'descricao', 'valor', 'preco_custo', 'get_margem_lucro', 'estoque_atual', 'ativo']
        ordering = ('titulo',)
        unit_field = 'empresa'
        can_admin = ['Administrador']
        menu = u'Estoque::Produtos', 'fa-bars'

    def __unicode__(self):
        return self.titulo

    @attr(u'Margem de Lucro')
    def get_margem_lucro(self):
        if self.preco_custo:
            return u'%s %%' % (format((self.valor - self.preco_custo) / self.valor * 100, '.2f'))
        return u'-'


class EntradaEstoque(models.Model):
    empresa = models.ModelChoiceField(Empresa, filter=True)
    produto = models.ModelChoiceField(Produto, filter=True)
    quantidade = models.PositiveIntegerField()
    data_cadastro = models.DateField(u'Data de Cadastro', default=datetime.today)

    fieldsets = ((u'Entradas em Estoque', {'fields': ('empresa', ('produto', 'quantidade'), 'data_cadastro')})),

    class Meta:
        verbose_name = u'Entrada em Estoque'
        verbose_name_plural = u'Entradas em Estoque'
        ordering = ('data_cadastro',)
        list_display = ['empresa', 'produto', 'quantidade', 'data_cadastro']
        unit_field = 'empresa'
        can_admin = ['Administrador', 'Gerente']
        menu = u'Estoque::Entradas'

    def save(self, *args, **kargs):
        estoque = self.produto.estoque_atual
        entrada_estoque = EntradaEstoque.objects.filter(id=self.id)
        if entrada_estoque.exists():
            for entrada in entrada_estoque:
                estoque = estoque - entrada.quantidade
        estoque = estoque + self.quantidade
        self.produto.estoque_atual = estoque
        self.produto.save()

        super(EntradaEstoque, self).save(*args, **kargs)


class SaidaEstoque(models.Model):
    empresa = models.ModelChoiceField(Empresa, filter=True)
    produto = models.ModelChoiceField(Produto, filter=True)
    quantidade = models.PositiveIntegerField(u'Quantidade')
    data_cadastro = models.DateField(u'Data de Cadastro', default=datetime.today)

    fieldsets = ((u'Entradas em Estoque', {'fields': ('empresa', ('produto', 'quantidade'), 'data_cadastro')}))

    class Meta:
        verbose_name = u'Saída de Estoque'
        verbose_name_plural = u'Saídas de Estoque'
        ordering = ('data_cadastro',)
        list_display = ['empresa', 'produto', 'quantidade', 'data_cadastro']
        unit_field = 'empresa'
        can_admin = ['Administrador', 'Gerente']
        menu = u'Estoque::Saídas'

    def save(self, *args, **kargs):
        estoque = self.produto.estoque_atual
        entrada_estoque = EntradaEstoque.objects.filter(id=self.id)
        if entrada_estoque.exists():
            for entrada in entrada_estoque:
                estoque = estoque + entrada.quantidade
        estoque = estoque - self.quantidade
        self.produto.estoque_atual = estoque
        self.produto.save()

        super(SaidaEstoque, self).save(*args, **kargs)


class Servico(models.Model):
    empresa = models.MultipleModelChoiceField(Empresa, help_text=u"Selecione uma ou mais empresas", filter=True)
    titulo = models.CharField(u'Título', unique=True, blank=False, search=True)
    descricao = models.TextField(u'Descrição', blank=False, search=True)
    valor = models.DecimalField(blank=False)

    class Meta:
        verbose_name = u'Serviço'
        verbose_name_plural = u'Serviços'
        list_display = ['titulo', 'descricao', 'valor',]
        ordering = ('titulo',)
        unit_field = 'empresa'
        can_admin = ['Administrador']
        menu = u'Estoque::Serviços'

    def __unicode__(self):
        return self.titulo


## MODULO DE COMPRAS

class Compra(models.Model):
    empresa = models.ModelChoiceField(Empresa, filter=True)
    fornecedor = models.ModelChoiceField(Fornecedor, queryset_filter={'ativo': True})
    numero_nfe = models.CharField(u'Número da Nota Fiscal')
    data_compra = models.DateTimeField(u'Data da Compra', default=datetime.today)
    data_entrega = models.DateTimeField(u'Data da Entrega', default=datetime.today)
    entregue = models.BooleanField(default=False, filter=True)
    faturada = models.BooleanField(default=False, filter=True)

    desconto = models.DecimalField(blank=True)
    frete = models.DecimalField(blank=True)
    adicionais = models.DecimalField(blank=True)

    forma_pagamento = models.ModelChoiceField(FormaPagamento, verbose_name=u'Forma de Pagamento')
    parcelas = models.PositiveIntegerField()

    observacoes = models.TextField(u'Observações', null=True, blank=True, search=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('empresa', 'fornecedor', 'numero_nfe', 'data_compra', 'data_entrega', 'entregue', 'faturada')}),
                 (u'Produtos', {'relations': ('compraproduto_set',)}),
                 (u'Outros', {'fields': ('desconto', 'frete', 'adicionais', 'get_total',)}),
                 (u'Pagamento', {'fields': ('forma_pagamento', 'parcelas',)}),
                 (u'Dados Complementares', {'fields': ('observacoes',)}),
                  )

    class Meta:
        verbose_name = u'Compra'
        verbose_name_plural = u'Compras'
        ordering = ('data_compra',)
        list_display = ['data_compra', 'fornecedor', 'numero_nfe', 'data_entrega', 'entregue', 'faturada', 'get_total']
        can_admin = ['Administrador',]
        menu = u'Compras::Compras', 'fa-inbox'

    def __unicode__(self):
        return u'Compra #%s' % self.pk

    @attr(u'Total')
    def get_total(self):
        total = Decimal(0.00)
        if self.compraproduto_set.all():
            total = self.compraproduto_set.aggregate(Sum('valor')).get('valor__sum', 0.00)
        total -= Decimal(self.desconto or 0.00)
        total += Decimal(self.frete or 0.00)
        total += Decimal(self.adicionais or 0.00)
        return total

    def pode_entregar(self):
        if not self.entregue and self.compraproduto_set.all():
            return True
        return False

    def pode_faturar(self):
        if not self.faturada and self.compraproduto_set.all():
            return True
        return False

    @action(u'Listar Despesas', inline=True, condition='listar_despesas', perm_or_group='soluti.list_despesa')
    def listar_despesas(self):
        return self.despesa_set.all()

    @action(u'Registrar Entrega', inline=True, condition='pode_entregar', perm_or_group='soluti.add_compra')
    def registrar_entrega(self):
        for produto in self.compraproduto_set.all():
            entradaestoque = EntradaEstoque()
            entradaestoque.empresa = self.empresa
            entradaestoque.produto = produto.produto
            entradaestoque.quantidade = produto.quantidade
            entradaestoque.data_cadastro = self.data_entrega
            entradaestoque.save()
        self.entregue = True
        self.save()

    @action(u'Faturar Compra', inline=True, condition='pode_faturar', perm_or_group='soluti.add_compra')
    def faturar_compra(self):
        if self.compraproduto_set.exists():
            valor = self.get_total() / int(self.parcelas)
            data_inicial = self.data_compra
            for x in range(int(self.parcelas)):
                despesa = Despesa()
                despesa.empresa = self.empresa
                despesa.compra = self
                despesa.categoria = CategoriaDespesa.COMPRAS
                despesa.data = data_inicial + relativedelta(months=x)
                despesa.descricao = u'Compra #%s' % self.pk
                despesa.valor = valor
                despesa.confirmada = False
                despesa.save()
        self.faturada = True
        self.save()


class CompraProduto(models.Model):
    compra = models.ModelChoiceField(Compra)
    produto = models.ModelChoiceField(Produto)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(u'Valor Total')

    class Meta:
        verbose_name = u'Produto'
        verbose_name_plural = u'Produtos'
        list_display = ['produto', 'quantidade', 'valor']
        can_admin = ['Administrador',]

    def __unicode__(self):
        return unicode(self.produto)

    def clean(self):
        if self.quantidade < 1:
            raise ValidationError(u'A quantidade do produto não pode ser menor que 1.')


## MODULO DE CLIENTES

class ProcedenciaCliente(models.Model):
    descricao = models.CharField(u'Descrição', unique=True, blank=False)

    class Meta:
        verbose_name = u'Procedência do Cliente'
        verbose_name_plural = u'Procedência dos Clientes'
        ordering = ('descricao',)
        can_admin=['Administrador']
        menu = u'Clientes::Procedência dos Clientes'

    def __unicode__(self):
        return self.descricao    


class TipoContrato(models.Model):
    nome = models.CharField(u'Nome', unique=True, blank=False)

    class Meta:
        verbose_name = u'Tipo de Contrato'
        verbose_name_plural = u'Tipos de Contratos'
        ordering = ('nome',)
        can_admin = ['Administrador']
        menu = u'Clientes::Tipos de Contratos', 'fa-list'

    def __unicode__(self):
        return self.nome


class ClienteManager(models.Manager):
    
    @subset(u'Novos', observe=True)
    def novos_clientes(self):
        return self.filter(cliente_desde__gte=date.today() - timedelta(30))


class Cliente(models.Model):
    # Dados principais
    nome = models.CharField(u'Nome/Razão Social', search=True)
    atividade = models.ModelChoiceField(Atividade)
    cliente_desde = models.DateField(u'Cliente desde', default=date.today)
    grupoeconomico = models.ModelChoiceField(GrupoEconomico, verbose_name=u'Grupo Econômico', null=True, blank=True)
    nome_responsavel = models.CharField(u'Nome do Responsável')
    eh_pessoa_fisica = models.BooleanField(u'É Pessoa Física?', default=False, filter=True)

    # Pessoa Fisica
    cpf = models.CpfField(u'CPF', blank=True)
    rg = models.CharField(u'RG', blank=True)
    nascimento = models.DateField(u'Data de Nascimento', null=True, blank=True)

    # Pessoa Juridica
    nome_fantasia = models.CharField(u'Nome Fantasia', blank=True)
    cnpj = models.CnpjField(u'CNPJ', blank=True)
    isentoinscricaoestadual = models.BooleanField(u'Isento de Inscrição Estadual', default=False, blank=True)
    inscricaoestadual = models.CharField(u'Inscrição Estadual', max_length=8, blank=True)
    inscricaomunicipal = models.CharField(u'Inscrição Municipal', max_length=14, blank=True)
    regime_tributario = models.CharField(u'Regime Tributário', choices=RegimeTributario.REGIMETRIBUTARIO_CHOICES, null=False, blank=True)
    data_fundacao = models.DateField(u'Data de Fundação', null=True, blank=True)

    # Endereço
    endereco = models.AddressField(u'Endereço', max_length=255)
    complemento = models.CharField(u'Complemento', max_length=255, blank=True)
    pontoreferencia = models.CharField(u'Ponto de Referência', max_length=255, blank=True)
    bairro = models.CharField(u'Bairro', max_length=255)
    estado = models.ModelChoiceField(Estado)
    cidade = models.ModelChoiceField(Cidade, form_filter=('estado', 'estado'))
    cep = models.CepField(u'CEP')
     
    # Contatos
    telefone = models.PhoneField9(u'Telefone')
    telefone2 = models.PhoneField9(u'Outro Telefone', blank=True)
    celular = models.PhoneField9(u'Celular', blank=True)
    email = models.EmailField(u'E-mail', max_length=255, blank=False)
    email_fiscal = models.EmailField(u'E-mail Fiscal', max_length=255, null=True, blank=True)
    site = models.CharField(u'Site', null=True, blank=True)

    # Dados da Contratação
    procedencia = models.ModelChoiceField(ProcedenciaCliente, null=True, blank=True)
    forma_pagamento = models.ModelChoiceField(FormaPagamento, verbose_name=u'Forma de Pagamento', null=True)

    # Dados Complementares
    ativo = models.BooleanField(u'Ativo', default=True)
    vendedor = models.ModelChoiceField(User)
    observacao = models.TextField(u'Observações', null=True, blank=True)
    data_cadastro = models.DateField(u'Data de Cadastro', auto_now_add=True, exclude=True)

    objects = ClienteManager()

    fieldsets = ((u'Dados Principais', {'fields': (('nome', 'nome_responsavel'), ('cliente_desde', 'atividade', 'grupoeconomico'),
                                                   ('telefone', 'telefone2', 'celular'),
                                                   ('site', 'email', 'email_fiscal'), 'eh_pessoa_fisica',)}),
                 (u'Contatos', {'relations': ('contatocliente_set',)}),
                 (u'Pessoa Física', {'fields': (('cpf', 'rg', 'nascimento'),)}),
                 (u'Pessoa Jurídica', {'fields': (('nome_fantasia', 'data_fundacao'), ('cnpj', 'regime_tributario'), ('isentoinscricaoestadual',
                    'inscricaoestadual', 'inscricaomunicipal'),)}),
                 (u'Endereço', {'fields': ('endereco', ('complemento', 'pontoreferencia'), ('bairro', 'cep'), ('estado', 'cidade'),)}),
                 (u'Dados da Contratação', {'fields': (('procedencia', 'forma_pagamento',),)}),
                 (u'Contratos', {'relations': ('contrato_set',),}),
                 (u'Visitas', {'relations': ('visitacliente_set',),}),
                 # (u'Propostas de Vendas', {'relations': ('propostavendacliente_set',),}),
                 (u'Anexos', {'relations': ('anexocliente_set',),}),
                 (u'Senhas', {'relations': ('senhacliente_set',),}),
                 (u'Dados Complementares', {'fields': ('ativo', ('vendedor'), 'observacao',),}),
    )

    class Meta:
        verbose_name = u'Cliente'
        verbose_name_plural = u'Clientes'
        ordering = ('nome',)
        list_display = ['id', 'nome', 'cnpj', 'vendedor']
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Atendente', 'Vendedor']
        menu = u'Clientes::Clientes'

    def __unicode__(self):
        return self.nome

    def __choices__(self):
        return dict(vendedor=User.objects.filter(groups__name="Vendedor"))

    def clean(self):
        if self.eh_pessoa_fisica:
            if not self.cpf:
                raise ValidationError(u'Preencha o campo CPF')
            elif not self.rg:
                raise ValidationError(u'Preencha o campo RG')
        else:
            if not self.cnpj:
                raise ValidationError(u'Preencha o campo CNPJ')
            elif not self.isentoinscricaoestadual and not self.inscricaoestadual:
                raise ValidationError(u'Preencha o campo Inscrição Estadual')
            elif not self.regime_tributario:
                raise ValidationError(u'Preencha o campo Regime Tributário')

        if not self.eh_pessoa_fisica and self.data_fundacao and self.data_fundacao > date.today():
            raise ValidationError(u'A Data de Fundação não pode ser uma data futura.')

        if self.eh_pessoa_fisica and self.cpf:
            cpfs = Cliente.objects.filter(cpf=self.cpf)
            if self.pk:
                cpfs = cpfs.exclude(pk=self.pk)
            if cpfs.exists():
                raise ValidationError(u'Já existe um cliente cadastrado com este CPF')

        if not self.eh_pessoa_fisica and self.cnpj:
            cnpjs = Cliente.objects.filter(cnpj=self.cnpj)
            if self.pk:
                cnpjs = cnpjs.exclude(pk=self.pk)
            if cnpjs.exists():
                raise ValidationError(u'Já existe um cliente cadastrado com este CNPJ')

    def save(self, *args, **kargs):
        if self.eh_pessoa_fisica:
            self.nome_fantasia = u''
            self.cnpj = u''
            self.isentoinscricaoestadual = False
            self.inscricaoestadual =  u''
            self.inscricaomunicipal = u''
            self.regime_tributario = u''
            self.data_fundacao = None
        else:
            self.cpf = u''
            self.rg = u''
            self.nascimento = None

        if self.isentoinscricaoestadual:
            self.inscricaoestadual = u''

        super(Cliente, self).save(*args, **kargs)

    @action(title=u'Listar Contratos', category=u"Listar", inline=True, condition='listar_contratos')
    def listar_contratos(self):
        return self.contrato_set.all()

    @action(title=u'Listar Propostas de Vendas', category=u"Listar", inline=True, condition='listar_propostas_vendas')
    def listar_propostas_vendas(self):
        return self.propostavendacliente_set.all()

    @action(title=u'Listar Receitas', category=u"Listar", inline=True, condition='listar_receitas')
    def listar_receitas(self):
        return self.receita_set.all()

    @action(title=u'Tickets Abertos', category='Tickets', inline=True, condition='listar_tickets_abertos')
    def listar_tickets_abertos(self):
        return self.ticket_set.filter(status=StatusTicket.ABERTO)

    @action(title=u'Tickets Pendentes', category='Tickets', inline=True, condition='listar_tickets_pendentes')
    def listar_tickets_pendentes(self):
        return self.ticket_set.filter(status=StatusTicket.PENDENTE)


class ContatoCliente(models.Model):
    cliente = models.ModelChoiceField(Cliente)
    nome = models.CharField(u'Nome', max_length=255, blank=False)
    cargo = models.ModelChoiceField(Cargo)
    setor = models.ModelChoiceField(Setor)
    telefone = models.PhoneField(u'Telefone')
    celular = models.PhoneField9(u'Celular', blank=True)
    email = models.EmailField(u'E-mail', max_length=255, blank=True)
    data_aniversario = models.DateField(u'Data de Aniversário')
    observacao = models.TextField(u'Observações', blank=True)

    fieldsets = ((u'Contatos do Cliente', {'fields': ('cliente', 'nome', ('cargo', 'setor'), ('telefone', 'celular'), 'email', 'data_aniversario', 'observacao',)}),)

    class Meta:
        verbose_name = u'Contato do Cliente'
        verbose_name_plural = u'Contatos do Cliente'
        ordering = ('nome',)
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Atendente',]

    def __unicode__(self):
        return u'Contato do Cliente #%s' % self.cliente.pk


class VisitaHorario:
    ENTRE_9_10 = u'Entre 9 e 10h'
    ENTRE_10_11 = u'Entre 10 e 11h'
    ENTRE_11_12 = u'Entre 11 e 12h'
    ENTRE_13_14 = u'Entre 13 e 14h'
    ENTRE_14_15 = u'Entre 14 e 15h'
    ENTRE_15_16 = u'Entre 15 e 16h'

    VISITAHORARIO_CHOICES = [
        (ENTRE_9_10, u'Entre 9 e 10h'),
        (ENTRE_10_11, u'Entre 10 e 11h'),
        (ENTRE_11_12, u'Entre 11 e 12h'),
        (ENTRE_13_14, u'Entre 13 e 14h'),
        (ENTRE_14_15, u'Entre 14 e 15h'),
        (ENTRE_15_16, u'Entre 15 e 16h'),
    ]


class VisitaCliente(models.Model):
    cliente = models.ModelChoiceField(Cliente)
    dias_semana = models.CharField(u'Dias da Semana', choices=DiasSemana.DIASSEMANA_CHOICES, max_length=100, blank=False)
    horario = models.CharField(u'Horário', choices=VisitaHorario.VISITAHORARIO_CHOICES, max_length=100, blank=False)
    observacao = models.TextField(u'Observações', blank=True)

    fieldsets = ((u'', {'fields': ('cliente', ('dias_semana', 'horario'), ('observacao',)),}),)

    class Meta:
        verbose_name = u'Visita ao Cliente'
        verbose_name_plural = u'Visitas ao Cliente'
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Atendente',]

    def __unicode__(self):
        return u'Visita #%s' % self.pk


class AnexoCliente(models.Model):
    cliente = models.ModelChoiceField(Cliente)
    anexo = models.FileField()

    fieldsets = ((u'', {'fields': ('cliente', 'anexo',),}),)

    class Meta:
        verbose_name = u'Anexo do Cliente'
        verbose_name_plural = u'Anexos do Cliente'
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Atendente',]

    def __unicode__(self):
        return u'Anexo #%s' % self.pk


class SenhaCliente(models.Model):
    cliente = models.ModelChoiceField(Cliente)
    servico = models.CharField(u'Serviço', max_length=255)
    descricao = models.CharField(u'Descrição', max_length=255, blank=True)
    url = models.UrlField(u'URL', blank=True)
    usuario = models.CharField(u'Usuário', max_length=255)
    senha = models.PasswordField(max_length=255)

    fieldsets = ((u'', {'fields': ('cliente', ('servico', 'descricao', 'url'), ('usuario', 'senha')),}),)

    class Meta:
        verbose_name = u'Senha do Cliente'
        verbose_name_plural = u'Senhas do Cliente'
        list_display = ['cliente', 'servico', 'descricao', 'url', 'usuario', 'senha']
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Atendente',]
        menu = u'Clientes::Senhas'

    def __unicode__(self):
        return u'Senha #%s' % self.pk


## MODULO DE VENDAS

class FormaContato:
    TELEMARKETING_ATIVO = u'Telemarketing ativo'
    TELEMARKETING_RECEPTIVO = u'Telemarketing receptivo'
    CHAT_ONLINE = u'Chat online'
    SITE_CONTATO = u'Site contato'

    FORMACONTATO_CHOICES = [
        (TELEMARKETING_ATIVO, u'Telemarketing ativo'),
        (TELEMARKETING_RECEPTIVO, u'Telemarketing receptivo'),
        (CHAT_ONLINE, u'Chat online'),
        (SITE_CONTATO, u'Site contato'),
    ]


class StatusLead:
    EM_PROSPECCAO = u'Em prospecção'
    AGUARDANDO_FEEDBACK = u'Aguardando feedback'
    AGUARDANDO_FECHAMENTO = u'Aguardando fechamento'
    NEGADO = u'Negado'
    FECHADO = u'Fechado'

    STATUSLEAD_CHOICES = [
        (EM_PROSPECCAO, u'Em prospecção'),
        (AGUARDANDO_FEEDBACK, u'Aguardando feedback'),
        (AGUARDANDO_FECHAMENTO, u'Aguardando fechamento'),
        (NEGADO, u'Negado'),
        (FECHADO, u'Fechado'),
    ]


class StatusPropostaVenda:
    ABERTA = u'Aberta'
    FINALIZADA = u'Finalizada'
    CANCELADA = u'Cancelada'

    STATUSPROPOSTAVENDA_CHOICES = [
        (ABERTA, u'Aberta'),
        (FINALIZADA, u'Finalizada'),
        (CANCELADA, u'Cancelada'),
    ]


class MotivoAlertaLead(models.Model):
    descricao = models.CharField(u'Descrição', unique=True, blank=False)

    class Meta:
        verbose_name = u'Motivo de Alerta de Lead'
        verbose_name_plural = u'Motivos de Alerta de Lead'
        ordering = ('descricao',)
        can_admin=['Administrador']
        menu = u'Vendas::Motivos de Alerta de Lead'

    def __unicode__(self):
        return self.descricao


class LeadManager(models.Manager):
    @subset(u'Alerta em 1 semana', observe=True)
    def alertas_em_uma_semana(self):
        return self.filter(alertalead__data__lte=date.today() + timedelta(7), alertalead__data__gte=date.today())

    @subset(u'Alerta em 15 dias', observe=True)
    def alertas_em_quinze_dias(self):
        return self.filter(alertalead__data__lte=date.today() + timedelta(15), alertalead__data__gte=date.today() + timedelta(8))

    @subset(u'Alerta em 1 mês', observe=True)
    def alertas_em_um_mes(self):
        return self.filter(alertalead__data__lte=date.today() + timedelta(30), alertalead__data__gte=date.today() + timedelta(16))


class Lead(models.Model):
    empresa = models.ModelChoiceField(Empresa)

    nome = models.CharField(u'Nome do Contato', search=True)
    nom_empresa = models.CharField(u'Nome da Empresa', search=True)
    cnpj = models.CnpjField(u'CNPJ', unique=True, null=True, blank=True)
    endereco = models.TextField(u'Endereço', null=True, blank=True)
    email = models.EmailField(u'E-mail', max_length=255, blank=False)
    telefone = models.PhoneField(u'Telefone')
    celular = models.PhoneField9(u'Celular', null=True, blank=True)
    procedencia = models.CharField(ProcedenciaCliente, null=True, blank=True)
    vendedor = models.ModelChoiceField(User, search=True, filter=True)
    forma_contato = models.CharField(u'Forma de Contato', choices=FormaContato.FORMACONTATO_CHOICES, max_length=100, blank=True, filter=True)
    interesse = models.MultipleModelChoiceField(Produto, help_text=u"Produto ou serviço de interesse", filter=True)
    proposta_enviada = models.BooleanField(u'Proposta enviada?', default=False)
    status = models.CharField(u'Status', choices=StatusLead.STATUSLEAD_CHOICES, max_length=100, filter=True)
    observacao = models.TextField(u'Observações', blank=True)

    objects = LeadManager()

    fieldsets = ((u'Dados Gerais', {'fields': ('empresa', 'nome', ('nom_empresa', 'cnpj'), 'endereco', 'email', ('telefone', 'celular'),
                                               'procedencia', 'vendedor', 'forma_contato', 'interesse', 'proposta_enviada', 'status',)}),
                 (u'Contatos', {'relations': ('alertalead_set',)}),
                 (u'Propostas de Venda', {'relations': ('propostavendalead_set',)}),
                 (u'Dados Complementares', {'fields': (('observacao',)),}),
    )

    class Meta:
        verbose_name = u'Lead'
        verbose_name_plural = u'Leads'
        ordering = ('empresa',)
        list_display = ['id', 'empresa', 'nome', 'email', 'telefone', 'vendedor', 'status']
        unit_field = 'empresa'
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Atendente', 'Vendedor']
        menu = u'Vendas::Leads', 'fa-shopping-cart'

    def __unicode__(self):
        return self.nom_empresa

    def __choices__(self):
        return dict(vendedor=User.objects.filter(groups__name="Vendedor"))

    @action(u'Atualizar Status', inline=True, perm_or_group='soluti.add_lead')
    def atualizar_status(self, status):
        self.save()

    @action(title=u'Listar Propostas de Vendas', category=u"Listar", inline=True, condition='listar_propostas_vendas')
    def listar_propostas_vendas(self):
        return self.propostavendalead_set.all()


class AlertaLead(models.Model):
    lead = models.ModelChoiceField(Lead)
    data = models.DateField(u'Data', null=False)
    motivo = models.ModelChoiceField(MotivoAlertaLead, filter=True)

    fieldsets = ((u'', {'fields': ('lead', ('data',), ('motivo',)),}),)

    class Meta:
        verbose_name = u'Alerta para Contato'
        verbose_name_plural = u'Alertas para Contato'
        ordering = ('data',)
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Atendente', 'Vendedor']

    def __unicode__(self):
        return u'Alerta para Contato #%s' % self.pk


class PropostaVenda(models.Model):
    empresa = models.ModelChoiceField(Empresa, filter=True)
    data = models.DateTimeField(default=datetime.today)

    forma_pagamento = models.ModelChoiceField(FormaPagamento, verbose_name=u"Forma de Pagamento")
    parcelas = models.PositiveIntegerField()
    vencimento = models.DateField(u"Primeiro Vencimento")

    vendedor = models.ModelChoiceField(User)
    status = models.CharField(u'Status', choices=StatusPropostaVenda.STATUSPROPOSTAVENDA_CHOICES, filter=True)
    faturada = models.BooleanField(default=False)
    vantagens = models.TextField(blank=True)
    observacao = models.TextField(u'Observação', null=True, blank=True)

    fieldsets = ((u'Dados Gerais', {'fields': (('empresa', 'cadastro', 'data'),)}),
                 (u'Serviços', {'relations': ('propostavendaservico_set',),}),
                 (u'Produtos', {'relations': ('propostavendaproduto_set',),}),
                 (u'Pagamento dos Produtos', {'fields': ('get_total', 'forma_pagamento', ('parcelas', 'vencimento'),),}),
                 (u'Dados Complementares', {'fields': ('vendedor', ('status', 'faturada'), 'vantagens', 'observacao',),}),
    )

    class Meta:
        verbose_name = u'Proposta de Venda'
        verbose_name_plural = u'Propostas de Vendas'
        list_display = ['data', 'status',]
        ordering = ('data',)
        unit_field = 'empresa'
        can_admin = ['Administrador']

    def __unicode__(self):
        return u'Proposta de Venda #%s' % self.pk

    def __choices__(self):
        return dict(vendedor=User.objects.filter(groups__name="Vendedor"))

    @attr(u'Total')
    def get_total(self):
        total = Decimal(0.00)
        if self.propostavendaproduto_set.all():
            total = self.propostavendaproduto_set.aggregate(Sum('valor')).get('valor__sum', 0.00)
        return total

    def pode_faturar(self):
        if self.status==StatusPropostaVenda.FINALIZADA and self.tem_produtos() and not self.faturada:
            return True
        return False

    def pode_imprimir(self):
        if self.tem_produtos() or self.tem_servicos():
            return True
        return False

    def tem_produtos(self):
        return self.propostavendaproduto_set.exists()

    def tem_servicos(self):
        return self.propostavendaservico_set.exists()

    @action(u'Listar Receitas', inline=True, condition='listar_receitas', perm_or_group='soluti.list_receita')
    def listar_receitas(self):
        return self.receita_set.all()

    @action(u'Faturar Produtos', inline=True, condition='pode_faturar', perm_or_group='soluti.add_propostavenda')
    def faturar_produtos(self):
        valor = self.get_total() / int(self.parcelas)
        data_inicial = self.vencimento
        for x in range(int(self.parcelas)):
            receita = Receita()
            receita.empresa = self.cadastro.empresa
            receita.cliente = self.cadastro
            receita.propostavenda = self
            receita.categoria = CategoriaReceita.VENDAS
            receita.data = data_inicial + relativedelta(months=x)
            receita.descricao = u'Proposta de Venda #%s' % self.pk
            receita.valor = valor
            receita.confirmada = False
            receita.save()
        self.faturada = True
        self.save()


class PropostaVendaCliente(PropostaVenda):
    cadastro = models.ModelChoiceField(Cliente, blank=True, null=True, filter=True)

    class Meta:
        verbose_name = u'Proposta de Venda ao Cliente'
        verbose_name_plural = u'Propostas de Vendas ao Cliente'
        can_admin = ['Administrador']
        menu = u'Vendas::Propostas de Vendas para Clientes'

    def __unicode__(self):
        return unicode(self.cadastro)


class PropostaVendaLead(PropostaVenda):
    cadastro = models.ModelChoiceField(Lead, blank=True, null=True, filter=True)

    class Meta:
        verbose_name = u'Proposta de Venda ao Lead'
        verbose_name_plural = u'Propostas de Vendas ao Lead'
        can_admin = ['Administrador']
        menu = u'Vendas::Propostas de Vendas para Leads'

    def __unicode__(self):
        return unicode(self.cadastro)


class PropostaVendaProduto(models.Model):
    proposta_venda = models.ModelChoiceField(PropostaVenda)

    produto = models.ModelChoiceField(Produto)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(u'Valor Total')

    fieldsets = ((u'Dados Gerais', {'fields': ('proposta_venda', 'produto', ('quantidade', 'valor'),)}),
    )

    class Meta:
        verbose_name = u'Produto'
        verbose_name_plural = u'Produtos'
        list_display = ['produto', 'quantidade', 'valor']
        can_admin = ['Administrador',]

    def __unicode__(self):
        return unicode(self.produto)

    def clean(self):
        if self.quantidade < 1:
            raise ValidationError(u'A quantidade do produto não pode ser menor que 1.')


class PropostaVendaServico(models.Model):
    proposta_venda = models.ModelChoiceField(PropostaVenda)

    servico = models.ModelChoiceField(Servico, verbose_name=u'Serviço')
    valor = models.DecimalField(u'Valor Total')

    fieldsets = ((u'Dados Gerais', {'fields': ('proposta_venda', 'servico', 'valor',)}),
    )

    class Meta:
        verbose_name = u'Serviço'
        verbose_name_plural = u'Serviços'
        list_display = ['servico', 'valor']
        can_admin = ['Administrador',]

    def __unicode__(self):
        return unicode(self.servico)

    def clean(self):
        if self.valor == 0:
            raise ValidationError(u'O valor total do serviço não pode ser igual a 0.')


class Revenda(models.Model):
    empresa = models.ModelChoiceField(Empresa, filter=True)

    nome = models.CharField(u'Nome')
    eh_pessoa_fisica = models.BooleanField(u'É Pessoa Física?', default=False, filter=True)

    cpf = models.CpfField(u'CPF', blank=True)
    rg = models.CharField(u'RG', blank=True)

    nome_fantasia = models.CharField(u'Nome Fantasia', blank=True)
    cnpj = models.CnpjField(u'CNPJ', blank=True)
    inscricaoestadual = models.CharField(u'Inscrição Estadual', max_length=8, blank=True)
    isentoinscricaoestadual = models.BooleanField(u'Isento de Inscrição Estadual', default=False, blank=True)
    inscricaomunicipal = models.CharField(u'Inscrição Municipal', max_length=14, blank=True)

    endereco = models.AddressField(u'Endereço', max_length=255)
    complemento = models.CharField(u'Complemento', max_length=255)
    pontoreferencia = models.CharField(u'Ponto de Referência', max_length=255)
    bairro = models.CharField(u'Bairro', max_length=255)
    estado = models.ModelChoiceField(Estado)
    cidade = models.ModelChoiceField(Cidade, form_filter=('estado', 'estado'))
    cep = models.CepField(u'CEP')

    telefone = models.PhoneField(u'Telefone')
    celular = models.PhoneField9(u'Celular', null=True, blank=True)
    email = models.EmailField(u'E-mail', max_length=255)

    ativo = models.BooleanField(u'Ativo', default=True)

    observacao = models.TextField(u'Observações', null=True, blank=True)

    data_cadastro = models.DateField(u'Data de Cadastro', auto_now_add=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('empresa', 'nome', 'eh_pessoa_fisica')}),
                 (u'Pessoa Física', {'fields': ('cpf', 'rg',)}),
                 (u'Pessoa Jurídica', {'fields': ('nome_fantasia', 'cnpj', ('isentoinscricaoestadual', 'inscricaoestadual'),
                                                  'inscricaomunicipal',)}),
                 (u'Endereço', {'fields': ('endereco', 'complemento', 'pontoreferencia', 'bairro', ('estado', 'cidade'), 'cep')}),
                 (u'Contatos', {'fields': (('telefone', 'celular'), 'email')}),
                 (u'Clientes', {'relations': ('clienterevenda_set',)}),
                 (u'Dados Complementares', {'fields': ('ativo', 'observacao', 'data_cadastro')}),
    )

    class Meta:
        verbose_name = u'Revenda'
        verbose_name_plural = u'Revendas'
        ordering = ('nome',)
        list_display=['nome', 'ativo']
        unit_field = 'empresa'
        can_admin = ['Administrador',]
        menu = u'Vendas::Revendas', 'fa-cog'

    def __unicode__(self):
        return self.nome

    def clean(self):
        if self.eh_pessoa_fisica:
            if not self.cpf:
                raise ValidationError(u'Preencha o campo CPF')
            elif not self.rg:
                raise ValidationError(u'Preencha o campo RG')
        else:
            if not self.cnpj:
                raise ValidationError(u'Preencha o campo CNPJ')
            elif not self.isentoinscricaoestadual and not self.inscricaoestadual:
                raise ValidationError(u'Preencha o campo Inscrição Estadual')

        if self.eh_pessoa_fisica and self.cpf:
            cpfs = Revenda.objects.filter(cpf=self.cpf)
            if self.pk:
                cpfs = cpfs.exclude(pk=self.pk)
            if cpfs.exists():
                raise ValidationError(u'Já existe um cliente cadastrado com este CPF')

        if not self.eh_pessoa_fisica and self.cnpj:
            cnpjs = Revenda.objects.filter(cnpj=self.cnpj)
            if self.pk:
                cnpjs = cnpjs.exclude(pk=self.pk)
            if cnpjs.exists():
                raise ValidationError(u'Já existe um cliente cadastrado com este CNPJ')

    def save(self, *args, **kargs):
        if self.eh_pessoa_fisica:
            self.nome_fantasia = u''
            self.cnpj = u''
            self.isentoinscricaoestadual = False
            self.inscricaoestadual =  u''
            self.inscricaomunicipal = u''
        else:
            self.cpf = u''
            self.rg = u''

        if self.isentoinscricaoestadual:
            self.inscricaoestadual = u''

        super(Revenda, self).save(*args, **kargs)


class ClienteRevenda(models.Model):
    revenda = models.ModelChoiceField(Revenda, filter=True)

    nome = models.CharField()
    cnpj = models.CnpjField(u'CNPJ', blank=True)
    telefone = models.PhoneField()
    email = models.EmailField(u'E-mail', max_length=255)

    ativo = models.BooleanField(u'Ativo', default=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('revenda', 'nome', 'cnpj', ('telefone', 'email'),)}),
                 (u'Dados Complementares', {'fields': ('ativo',)}),
    )

    class Meta:
        verbose_name = u'Cliente de Revenda'
        verbose_name_plural = u'Clientes de Revendas'
        ordering = ('nome',)
        list_display=['nome', 'cnpj', 'telefone', 'email', 'ativo']
        unit_field = 'empresa'
        can_admin = ['Administrador',]
        menu = u'Clientes::Clientes de Revendas'

    def __unicode__(self):
        return self.nome


## MODULO DE ATENDIMENTO

class SatisfacaoSuporte:
    MUITO_SATISFEITO = u'Muito satisfeito'
    RAZOAVELMENTE_SATISFEITO = u'Razoavelmente satisfeito'
    INSATISFEITO = u'Insatisfeito'

    SATISFACAOSUPORTE_CHOICES = [
        (MUITO_SATISFEITO, u'Muito satisfeito'),
        (RAZOAVELMENTE_SATISFEITO, u'Razoavelmente satisfeito'),
        (INSATISFEITO, u'Insatisfeito'),
    ]


class StatusTicket:
    ABERTO = u'Aberto'
    PENDENTE = u'Pendente'
    FINALIZADO = u'Finalizado'
    REABERTO = u'Reaberto'

    STATUSTICKET_CHOICES = [
        (ABERTO, u'Aberto'),
        (PENDENTE, u'Pendente'),
        (FINALIZADO, u'Finalizado'),
        (REABERTO, u'Reaberto'),
    ]


class TipoInteracao(models.Model):
    nome = models.CharField(u'Nome', unique=True, blank=False)

    class Meta:
        verbose_name = u'Tipo de Interação'
        verbose_name_plural = u'Tipos de Interações'
        ordering = ('nome',)
        can_admin = ['Administrador']
        menu = u'Atendimento::Tipos de Interações', 'fa-list'

    def __unicode__(self):
        return self.nome


class TicketManager(models.Manager):
    @subset(u'Abertos', observe=True)
    def abertos(self):
        return self.filter(status=StatusTicket.ABERTO)

    @subset(u'Pendentes', observe=True)
    def pendentes(self):
        return self.filter(status=StatusTicket.PENDENTE)

    @subset(u'Finalizados')
    def finalizados(self):
        return self.filter(status=StatusTicket.FINALIZADO)


class Ticket(models.Model):
    cliente = models.ModelChoiceField(Cliente, queryset_filter={"ativo": True}, help_text=u"Somente serão listados clientes ativos.", filter=True)
    observacao = models.TextField(u'Descrição', blank=True)
    responsaveis = models.MultipleModelChoiceField(User, verbose_name=u'Responsáveis', help_text=u"Selecione um ou mais responsáveis", filter=True)
    status = models.CharField(choices=StatusTicket.STATUSTICKET_CHOICES, filter=True)
    tipo_interacao = models.CharField(TipoInteracao)
    data = models.DateField(u'Data de Cadastro', auto_now_add=True, exclude=True)

    objects = TicketManager()

    fieldsets = ((u'Dados Gerais', {'fields': ('cliente', 'observacao', 'responsaveis', ('status', 'tipo_interacao'),)}),
                 (u'Interações', {'relations': ('interacaoticket_set',)}),
                 (u'Controle de Satisfação', {'relations': ('controlesatisfacao_set',)}),
    )

    class Meta:
        verbose_name = u'Ticket'
        verbose_name_plural = u'Tickets'
        ordering = ('data',)
        list_display = ['id', 'cliente', 'observacao', 'tipo_interacao', 'responsaveis', 'status']
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Atendente', 'Vendedor']
        menu = u'Atendimento::Tickets', 'fa-question-circle'

    def __unicode__(self):
        return u'Ticket #%s' % self.pk

    def __choices__(self):
        return dict(responsaveis=User.objects.filter(groups__name="Atendente"))

    def pode_finalizar(self):
        if self.status != StatusTicket.FINALIZADO:
            return True
        return False

    def pode_reabrir(self):
        if self.status == StatusTicket.FINALIZADO:
            return True
        return False

    @action(u'Finalizar Ticket', inline=True, condition='pode_finalizar', perm_or_group='soluti.change_ticket')
    def finalizar_ticket(self):
        self.status = StatusTicket.FINALIZADO
        self.save()

    @action(u'Reabrir Ticket', inline=True, condition='pode_reabrir', perm_or_group='soluti.change_ticket')
    def reabrir_ticket(self):
        self.status = StatusTicket.REABERTO
        self.save()


class InteracaoTicket(models.Model):
    ticket = models.ModelChoiceField(Ticket, filter=True)
    responsavel = models.ModelChoiceField(User, verbose_name=u'Responsável', filter=True)
    data = models.DateTimeField(u'Data/Hora', default=datetime.today)
    comentario = models.TextField(u'Comentário', blank=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('ticket', ('responsavel', 'data'),)}),
                 (u'Comentário', {'fields': ('comentario',)}),
    )

    class Meta:
        verbose_name = u'Interação'
        verbose_name_plural = u'Interações'
        ordering = ('data',)
        list_display = ['ticket', 'responsavel', 'data', 'comentario']
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Suporte']

    def __unicode__(self):
        return u'Interação #%s - Ticket #%s' % (self.pk, self.ticket)

    def __choices__(self):
        return dict(responsavel=User.objects.filter(groups__name="Atendente"))


class ControleSatisfacao(models.Model):
    ticket = models.ModelChoiceField(Ticket, filter=True)
    classificacao = models.CharField(choices=SatisfacaoSuporte.SATISFACAOSUPORTE_CHOICES, filter=True)
    data = models.DateTimeField(u'Data/Hora', default=datetime.today)
    comentario = models.TextField(u'Comentário', blank=True)
    interessado = models.CharField(u'Nome')
    cargo_interessado = models.CharField(u'Cargo')

    fieldsets = ((u'Dados Gerais', {'fields': ('ticket', ('classificacao', 'data'), 'comentario')}),
                 (u'Interessado', {'fields': ('interessado', 'cargo_interessado')}),
    )

    class Meta:
        verbose_name = u'Controle de Satisfação'
        verbose_name_plural = u'Controles de Satisfação'
        ordering = ('data',)
        list_display = ['ticket', 'classificacao', 'data', 'comentario', 'get_interessado']
        can_admin = ['Administrador', 'Gerente']
        can_list = ['Suporte']
        menu = u'Atendimento::Controles de Satisfação'

    def __unicode__(self):
        return u'Controle de Satisfação - Ticket #%s' % self.ticket.pk

    @attr(u'Interessado')
    def get_interessado(self):
        return u'%s (%s)' % (self.interessado, self.cargo_interessado)


## MODULO DE CONTRATOS




class ContratoManager(models.Manager):
    @subset(u'Em Andamento')
    def andamento(self):
        return self.filter(data_inicio__lte=date.today(), data_fim__gte=date.today())

    @subset(u'Expirado', observe=True)
    def expirado(self):
        return self.filter(data_fim__lt=date.today())

    @subset(u'Cancelado')
    def estah_cancelado(self):
        return self.filter(cancelado=True)

    @subset(u'A Vencer', observe=True)
    def a_vencer(self):
        return self.filter(data_fim__lte=date.today() + timedelta(30), data_fim__gte=date.today())


class Contrato(models.Model):
    cliente = models.ModelChoiceField(Cliente, filter=True)
    tipo_contrato = models.ModelChoiceField(TipoContrato, filter=True)
    data_inicio = models.DateField(u'Data de Início', filter=True)
    data_fim = models.DateField(u'Data de Fim', filter=True)

    forma_pagamento = models.ModelChoiceField(FormaPagamento, verbose_name=u"Forma de Pagamento")
    parcelas = models.PositiveIntegerField()
    vencimento = models.DateField(u"Primeiro Vencimento")

    anexo = models.FileField(blank=True, null=True)
    responsavel = models.ModelChoiceField(User, verbose_name=u'Responsável')
    cancelado = models.BooleanField(u'Cancelado?', default=False)
    faturado = models.BooleanField(default=False)
    observacoes = models.TextField(u'Observações', search=True, blank=True, null=True)

    objects = ContratoManager()

    fieldsets = ((u'Dados Gerais', {'fields': ('cliente', 'tipo_contrato', ('data_inicio', 'data_fim'),)}),
                 (u'Serviços', {'relations': ('contratoservico_set',),}),
                 (u'Pagamento', {'fields': ('get_total_servico', 'forma_pagamento', ('parcelas', 'vencimento'),),}),
                 (u'Dados Complementares', {'fields': ('anexo', 'responsavel', ('cancelado', 'faturado'), 'observacoes')}),
    )

    class Meta:
        verbose_name = u'Contrato'
        verbose_name_plural = u'Contratos'
        ordering = ('data_inicio',)
        list_display = ['cliente', 'tipo_contrato', 'data_inicio', 'data_fim', 'cancelado', 'faturado']
        can_admin = ['Administrador', 'Gerente']
        menu = u'Clientes::Contratos'

    def __unicode__(self):
        return u'Contrato de %s a %s' % (self.data_inicio.strftime('%d/%m/%Y'), self.data_fim.strftime('%d/%m/%Y'))

    def __choices__(self):
        return dict(responsavel=User.objects.filter(groups__name="Vendedor"))

    @attr(u'Total de Serviços')
    def get_total_servico(self):
        total = Decimal(0.00)
        if self.contratoservico_set.exists():
            total = self.contratoservico_set.aggregate(Sum('valor')).get('valor__sum', 0.00)
        return total

    @action(u'Listar Receitas', inline=True, condition='listar_receitas', perm_or_group='soluti.list_receita')
    def listar_receitas(self):
        return self.receita_set.all()

    @action(u'Faturar', inline=True, condition='not faturado', perm_or_group='soluti.add_contrato')
    def faturar(self):
        if self.contratoservico_set.exists():
            valor = self.get_total_servico() / int(self.parcelas)
            data_inicial_servico = self.vencimento
            for x in range(int(self.parcelas)):
                receita = Receita()
                receita.empresa = self.cliente.empresa
                receita.cliente = self.cliente
                receita.contrato = self
                receita.categoria = CategoriaReceita.SERVICOS
                receita.data = data_inicial_servico + relativedelta(months=x)
                receita.descricao = u'Contrato #%s' % self.pk
                receita.valor = valor
                receita.confirmada = False
                receita.save()
        self.faturado = True
        self.save()


class ContratoServico(models.Model):
    contrato = models.ModelChoiceField(Contrato)

    servico = models.ModelChoiceField(Servico, verbose_name=u'Serviço')
    valor = models.DecimalField(u'Valor Total')

    fieldsets = ((u'Dados Gerais', {'fields': ('contrato', 'servico', 'valor',)}),
    )

    class Meta:
        verbose_name = u'Serviço'
        verbose_name_plural = u'Serviços'
        list_display = ['servico', 'valor']
        can_admin = ['Administrador',]

    def __unicode__(self):
        return unicode(self.servico)

    def clean(self):
        if self.valor == 0:
            raise ValidationError(u'O valor total do serviço não pode ser igual a 0.')


## MODULO DE FINANCEIRO

class CategoriaDespesa(models.Model):
    nome = models.CharField(u'Nome', unique=True, blank=False)

    class Meta:
        verbose_name = u'Categoria de Despesa'
        verbose_name_plural = u'Categorias de Despesas'
        ordering = ('nome',)
        can_admin = ['Administrador']
        menu = u'Financeiro::Categoria de Despesa', 'fa-list'

    def __unicode__(self):
        return self.nome

class CategoriaReceita(models.Model):
    nome = models.CharField(u'Nome', unique=True, blank=False)

    class Meta:
        verbose_name = u'Categoria de Receita'
        verbose_name_plural = u'Categorias de Receitas'
        ordering = ('nome',)
        can_admin = ['Administrador']
        menu = u'Financeiro::Categoria de Receita', 'fa-list'

    def __unicode__(self):
        return self.nome


class Despesa(models.Model):
    empresa = models.ModelChoiceField(Empresa, filter=True)
    categoria = models.ModelChoiceField(CategoriaDespesa, filter=True)
    data = models.DateField(filter=True)
    descricao = models.TextField(u'Descrição', search=True)
    valor = models.DecimalField()
    confirmada = models.BooleanField(u'Paga', default=True, filter=True)
    compra = models.ModelChoiceField(Compra, null=True, blank=True, filter=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('empresa',)}),
                 (u'Dados da Despesa', {'fields': ('categoria', 'descricao', ('data', 'valor'), 'confirmada',)}),
                 (u'Relacionamentos', {'fields': ('compra',)}),
    )

    class Meta:
        verbose_name = u'Despesa'
        verbose_name_plural = u'Despesas'
        ordering = ('data',)
        list_display = ['data', 'categoria', 'valor', 'descricao', 'confirmada']
        unit_field = 'empresa'
        can_admin = ['Administrador', 'Gerente']
        menu = u'Financeiro::Despesas', 'fa-money'

    def __unicode__(self):
        return u'Despesa de %s no valor de R$ %s' % (self.categoria, self.valor)

    @action(u'Confirmar Pagamento', inline=True, condition='not confirmada')
    def confirmar(self):
        self.confirmada = True
        self.save()

    @action(u'Cancelar Pagamento', inline=True, condition='confirmada')
    def nao_confirmar(self):
        self.confirmada = False
        self.save()


class Receita(models.Model):
    categoria = models.ModelChoiceField(CategoriaReceita, filter=True)
    nota_fiscal = models.CharField(u'Nº Nota Fiscal', blank=True, search=True)
    data = models.DateField(filter=True)
    descricao = models.TextField(u'Descrição', search=True)
    valor = models.DecimalField()
    confirmada = models.BooleanField(u'Recebida', default=True)

    empresa = models.ModelChoiceField(Empresa, filter=True)
    cliente = models.ModelChoiceField(Cliente, queryset_filter={"ativo": True}, null=True, blank=True, filter=True)
    propostavenda = models.ModelChoiceField(PropostaVenda, null=True, blank=True, filter=True)
    contrato = models.ModelChoiceField(Contrato, null=True, blank=True, filter=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('categoria', 'descricao', ('data', 'valor'), 'nota_fiscal', 'confirmada',)}),
                 (u'Relacionamentos', {'fields': (('empresa', 'cliente'), ('propostavenda', 'contrato'),)}),
    )

    class Meta:
        verbose_name = u'Receita'
        verbose_name_plural = u'Receitas'
        ordering = ('data',)
        list_display = ['data', 'categoria', 'valor', 'descricao', 'confirmada']
        unit_field = 'empresa'
        can_admin = ['Administrador', 'Gerente']
        menu = u'Financeiro::Receitas'

    def __unicode__(self):
        return u'Receita de %s no valor de R$ %s' % (self.categoria, self.valor)

    @action(u'Confirmar Recebimento', inline=True, condition='not confirmada')
    def confirmar(self):
        self.confirmada = True
        self.save()

    @action(u'Cancelar Recebimento', inline=True, condition='confirmada')
    def nao_confirmar(self):
        self.confirmada = False
        self.save()


## MODULO DE RECURSOS HUMANOS

class Colaborador(models.Model):
    # Cadastro
    empresa = models.MultipleModelChoiceField(Empresa, help_text=u"Selecione uma ou mais empresas")

    # Dados gerais
    nome = models.CharField()
    sexo = models.CharField(u'Sexo', choices=Sexo.SEXO_CHOICES, filter=True)
    nascimento = models.DateField(u'Data de Nascimento')
    data_admissao = models.DateField(u'Data de Admissão')
    data_demissao = models.DateField(u'Data de Demissão', null=True, blank=True)

    # Endereço
    endereco = models.AddressField(u'Endereço')
    complemento = models.CharField(u'Complemento')
    pontoreferencia = models.CharField(u'Ponto de Referência')
    bairro = models.CharField(u'Bairro')
    estado = models.ModelChoiceField(Estado)
    cidade = models.ModelChoiceField(Cidade, form_filter=('estado', 'estado'))
    cep = models.CepField(u'CEP')

    # Contatos
    telefone = models.PhoneField(u'Telefone')
    celular = models.PhoneField9(u'Celular', null=True, blank=True)
    email = models.EmailField(u'E-mail', max_length=255)

    #Documentos
    cpf = models.CpfField(u'CPF', blank=True)
    rg = models.CharField(u'RG', blank=True)
    ctps = models.CharField(u'CTPS', blank=True)
    serie_ctps = models.CharField(u'Série CTPS', blank=True)
    estado_ctps = models.ModelChoiceField(Estado, verbose_name=u'Estado CTPS', related_name='estado_ctps')
    pis_pasep = models.CharField(u'PIS/PASEP', blank=True)
    titulo_eleitor = models.CharField(u'Título de Eleitor', blank=True)
    zona_eleitoral = models.CharField(u'Zona Eleitoral', blank=True)
    estado_eleitoral = models.ModelChoiceField(Estado, verbose_name=u'Estado Eleitoral', related_name='estado_eleitoral')
    categoria_cnh = models.CharField(u'Categoria CNH', choices=CategoriaCnh.CATEGORIACNH_CHOICES, filter=True)

    # Situação
    ativo = models.BooleanField(u'Ativo', default=True)

    # Outros
    observacao = models.TextField(u'Observação', null=True, blank=True)

    data_cadastro = models.DateField(u'Data de Cadastro', auto_now_add=True)

    fieldsets = ((u'Cadastro', {'fields': ('empresa',)}),
                 (u'Dados Gerais', {'fields': ('nome', ('sexo', 'nascimento',), ('data_admissao', 'data_demissao'))}),
                 (u'Endereço', {'fields': ('endereco', 'complemento', 'pontoreferencia', 'bairro', ('estado', 'cidade'), 'cep')}),
                 (u'Contatos', {'fields': (('telefone', 'celular'), ('email', ))}),
                 (u'Situação', {'fields': ('ativo',)}),
                 (u'Documentos', {'fields': (('cpf', 'rg'), ('ctps', 'serie_ctps', 'estado_ctps'), 'pis_pasep', ('titulo_eleitor', 'zona_eleitoral'), 'estado_eleitoral', 'categoria_cnh' )}),
                 (u'Observação', {'fields': ('observacao',)}),
    )

    class Meta:
        verbose_name = u'Colaborador'
        verbose_name_plural = u'Colaboradores'
        ordering = ('nome',)
        list_display = ['id', 'nome', 'cpf', 'rg', 'telefone']
        can_admin = ['Administrador',]
        menu = u'Recursos Humanos::Colaboradores', 'fa-users'

    def __unicode__(self):
        return self.nome

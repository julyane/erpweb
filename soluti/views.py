# -*- coding: utf-8 -*-
from djangoplus.decorators.views import view, action
from djangoplus.ui.calendar import Calendar, ModelCalendar
from djangoplus.ui.chart import DonutChart, MultipleBarChart
from djangoplus.ui.panel import ProgressPanel, IconPanel, CardPanel, FeedPanel
from itertools import chain
from operator import attrgetter
import datetime

from djangoplus.contrib.site.models import User

from django.contrib.auth.models import Group

from django.db.models import Sum
from django.template.loader_tags import register
from soluti.models import Despesa, Receita, PropostaVenda, Lead, Produto, Servico, Ticket, \
    StatusTicket, Empresa, Compra, Contrato, StatusLead, ControleSatisfacao, SatisfacaoSuporte, Revenda, Colaborador, \
    StatusPropostaVenda, Cliente, PropostaVendaCliente


@register.filter
def model_name(value):
    return value.__class__.__name__


@view(u'Dashboard', 'soluti.list_cliente')
def index(request):

    dashboard_banner = IconPanel(request)
    dashboard_banner.add('fa-inbox', u'Clientes', Cliente.objects.filter(ativo=True).count(), '/list/soluti/cliente/')
    dashboard_banner.add('fa-inbox', u'Produtos', Produto.objects.all().count(), '/list/soluti/produto/')
    dashboard_banner.add('fa-inbox', u'Serviços', Servico.objects.all().count(), '/list/soluti/servico/')
    dashboard_banner.add('fa-shopping-cart', u'Revendas', Revenda.objects.all().count(), '/list/soluti/revenda/')
    dashboard_banner.add('fa-users', u'Colaboradores', Colaborador.objects.all().count(), '/list/soluti/colaborador/')

    cards = CardPanel(request)
    cards.add('fa-user', u'Empresas ativas', Empresa.objects.all().count(), '/list/soluti/empresa/', 'bg-info')
    cards.add('fa-inbox', u'Compras realizadas', Compra.objects.all().count(), '/list/soluti/compra/', 'bg-success')
    cards.add('fa-file-text', u'Contratos realizados', Contrato.objects.filter(cancelado=False).count(), '/list/soluti/contrato/', 'bg-success')
    cards.add('fa-question-circle', u'Tickets abertos', Ticket.objects.filter(status=StatusTicket.ABERTO).count(), '/list/soluti/ticket/', 'bg-warning')

    # donut = DonutChart()
    # donut.add(u'Em prospecção', Lead.objects.filter(status=StatusLead.EM_PROSPECCAO).count())
    # donut.add(u'Aguardando feedback', Lead.objects.filter(status=StatusLead.AGUARDANDO_FEEDBACK).count())
    # donut.add(u'Aguardando fechamento', Lead.objects.filter(status=StatusLead.AGUARDANDO_FECHAMENTO).count())
    # donut.add(u'Negado', Lead.objects.filter(status=StatusLead.NEGADO).count())
    # donut.add(u'Fechado', Lead.objects.filter(status=StatusLead.FECHADO).count())

    # donut_controle_satisfacao = DonutChart()
    # donut_controle_satisfacao.add(u'Muito satisfeito', ControleSatisfacao.objects.filter(classificacao=SatisfacaoSuporte.MUITO_SATISFEITO).count())
    # donut_controle_satisfacao.add(u'Razoavelmente satisfeito', ControleSatisfacao.objects.filter(classificacao=SatisfacaoSuporte.RAZOAVELMENTE_SATISFEITO).count())
    # donut_controle_satisfacao.add(u'Insatisfeito', ControleSatisfacao.objects.filter(classificacao=SatisfacaoSuporte.INSATISFEITO).count())

    bars = MultipleBarChart(u'Propostas de Vendas por Vendedor')
    for vendedor in User.objects.filter(groups__name="Vendedor"):
        propostas = PropostaVenda.objects.filter(vendedor=vendedor)
        abertas = propostas.filter(status=StatusPropostaVenda.ABERTA)
        if abertas.exists():
            bars.add(vendedor.nome, u'Abertas', abertas.count())
        finalizadas = propostas.filter(status=StatusPropostaVenda.FINALIZADA)
        if finalizadas.exists():
            bars.add(vendedor.nome, u'Finalizadas', finalizadas.count())
        canceladas = propostas.filter(status=StatusPropostaVenda.CANCELADA)
        if canceladas.exists():
            bars.add(vendedor.nome, u'Canceladas', canceladas.count())

    calendar = ModelCalendar(request, u'Calendário Financeiro', True)
    calendar.add(Despesa.objects.all(), 'data')
    calendar.add(Receita.objects.all(), 'data')

    aniversariantes = Calendar(request, u'Aniversariantes')
    for colaborador in Colaborador.objects.all():
        aniversariantes.add(u'Colaborador: %s' % colaborador.nome, colaborador.nascimento)

    return locals()


@action(PropostaVendaCliente, u'Imprimir Proposta de Venda', 'soluti.list_propostavendacliente', inline=True, condition='pode_imprimir', style='pdf')
def proposta_venda(request, proposta):
    title = u'Proposta de Venda'

    propostavenda = PropostaVenda.objects.get(pk=proposta)

    return locals()


@view(u'Permissões', None, u'Relatórios::Listagem de Permissões')
def permissoes(request):
    title = u'Permissões'

    grupos = Group.objects.all().order_by(u'name')
    # lista_permissoes = grupo.permissions.all()

    return locals()


@view(u'Relatório Financeiro', None, u'Relatórios::Relatório Financeiro', 'fa-paperclip')
def relatorio_financeiro(request):
    title = u'Relatório Financeiro'

    total_receitas = 0
    receitas = Receita.objects.filter(confirmada=True)
    if receitas:
        total_receitas = receitas.aggregate(Sum('valor'))['valor__sum']

    total_despesas = 0
    despesas = Despesa.objects.filter(confirmada=True)
    if despesas:
        total_despesas = despesas.aggregate(Sum('valor'))['valor__sum']

    registros = sorted(chain(receitas, despesas), key=attrgetter('data'))

    resultado = total_receitas - total_despesas

    # t0 = CountReport('Receitas por Categoria', receitas, 'categoria')
    # t1 = CountReport('Despesas por Categoria', despesas, 'categoria')

    return locals()

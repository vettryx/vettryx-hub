"""
==============================================================================
Módulo: Visualizações Base (Common Views)
Caminho: apps/common/views.py
==============================================================================

Contém as Class-Based Views (CBVs) genéricas do sistema.
Estas views padronizam a renderização de listas, formulários, detalhes e
exclusões, integrando paginação, buscas dinâmicas e suporte nativo a requisições AJAX.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)


class CommonListView(LoginRequiredMixin, ListView):
    """
    Gera automaticamente: search_fields, headers, rows e page_obj
    para alimentar templates baseados em tabelas e filtros dinâmicos.
    """
    template_name = "includes/apps_list.html"
    paginate_by = 20
    title = ""
    header_buttons = []

    # Configurações que as views filhas devem definir
    search_config = []  # Ex: [{'name': 'q', 'type': 'text', 'label': 'Buscar'}]
    table_headers = []  # Ex: [{'field': 'name', 'label': 'Nome'}]

    def get_paginate_by(self, queryset):
        return self.request.GET.get("records_per_page", self.paginate_by)

    def get_ordering(self):
        order_by = self.request.GET.get("order_by")
        descending = self.request.GET.get("descending", "False")
        if order_by:
            return f"-{order_by}" if descending == "True" else order_by
        return None

    def get_queryset(self):
        queryset = super().get_queryset()

        for config in self.search_config:
            field = config.get("name")
            ftype = config.get("type")
            value = self.request.GET.get(field)

            if value:
                if ftype == "text":
                    queryset = queryset.filter(**{f"{field}__icontains": value})
                elif ftype in ("select", "boolean"):
                    if value == "True":
                        value = True
                    elif value == "False":
                        value = False
                    queryset = queryset.filter(**{field: value})

        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    def get_row_data(self, item):
        raise NotImplementedError("Implemente 'get_row_data' na view filha")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. PROCESSAMENTO DA BUSCA
        prepared_search = []
        for config in self.search_config:
            c = config.copy()
            c["value"] = self.request.GET.get(config["name"], "")
            c["id"] = f"search-{config['name']}"
            if "queryset" in config:
                c["options"] = [(o.pk, str(o)) for o in config["queryset"]]
            prepared_search.append(c)

        buttons = self.header_buttons.copy()

        # 2. BOTÕES DE AÇÃO DA BUSCA
        context["search_actions"] = [
            {"type": "submit", "label": "Buscar", "class": "btn-list"},
            {
                "type": "clear",
                "label": "Limpar",
                "class": "btn-clear",
                "url": self.request.path,
            },
        ]

        context.update(
            {
                "title": self.title,
                "header_buttons": buttons,
                "search_fields": prepared_search,
                "headers": self.table_headers,
                "rows": [self.get_row_data(item) for item in context["page_obj"]],
                "query_params": self.request.GET.urlencode(),
            }
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        """Suporte a AJAX: retorna apenas a tabela parcial se for XMLHttpRequest."""
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.response_class(
                request=self.request,
                template="includes/partial_list_results.html",
                context=context,
                **response_kwargs,
            )
        return super().render_to_response(context, **response_kwargs)


class CommonFormMixin:
    """Gera automaticamente sections e buttons para templates de formulário."""
    title = ""
    return_url = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get("form")

        if "sections" not in context and form:
            context["sections"] = [
                {
                    "id": "general",
                    "title": "Dados do Registro",
                    "fields": list(form),
                    "form": form,
                    "active": True,
                }
            ]

        sections = context.get("sections")
        if sections:
            has_active = any(s.get("active") for s in sections)
            if not has_active:
                sections[0]["active"] = True

        if "buttons" not in context:
            context["buttons"] = [
                {
                    "class": "btn-return",
                    "url": self.return_url or "#",
                    "title": "Retornar",
                    "text": "Retornar",
                },
            ]

        context["title"] = self.title
        return context


class CommonCreateView(LoginRequiredMixin, CommonFormMixin, CreateView):
    template_name = "includes/apps_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Registro criado com sucesso!")
        return super().form_valid(form)


class CommonUpdateView(LoginRequiredMixin, CommonFormMixin, UpdateView):
    template_name = "includes/apps_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Registro atualizado com sucesso!")
        return super().form_valid(form)


class CommonDeleteView(LoginRequiredMixin, DeleteView):
    """Padroniza a confirmação de exclusão estática ou via AJAX."""
    template_name = "includes/apps_confirm_delete.html"
    title = "Confirmar Exclusão"
    return_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object

        cancel_url = self.return_url or self.success_url
        context["title"] = self.title
        context["cancel_url"] = cancel_url
        context["object_name"] = str(obj)

        context["buttons"] = [
            {
                "type": "submit",
                "class": "btn-delete-confirm",
                "text": "Sim, excluir permanentemente",
                "icon": "fas fa-trash-alt",
            },
            {
                "type": "link",
                "url": cancel_url,
                "class": "btn-return",
                "text": "Cancelar operação",
            },
        ]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.response_class(
                request=self.request,
                template="includes/partial_delete_card.html",
                context=context,
                **response_kwargs,
            )
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Registro excluído com sucesso!")
        return super().form_valid(form)


class CommonTemplateView(LoginRequiredMixin, TemplateView):
    """Páginas estáticas ou dashboards."""
    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class CommonDetailView(LoginRequiredMixin, DetailView):
    """Gera automaticamente tabs e seções de visualização de detalhes (Somente Leitura)."""
    title = ""
    return_url = ""
    template_name = "includes/apps_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object

        context["title"] = self.title or str(obj)

        if "buttons" not in context:
            app = obj._meta.app_label
            try:
                edit_url = reverse_lazy(f"{app}:edit", args=[obj.pk])
                delete_url = reverse_lazy(f"{app}:delete", args=[obj.pk])
            except Exception:
                edit_url = "#"
                delete_url = "#"

            context["buttons"] = [
                {"class": "btn-edit", "url": edit_url, "title": "Editar", "text": "Editar"},
                {"class": "btn-delete", "url": delete_url, "title": "Excluir", "text": "Excluir"},
                {"class": "btn-return", "url": self.return_url, "title": "Voltar", "text": "Voltar"},
            ]

        if "sections" not in context:
            context["sections"] = [
                {
                    "title": "Dados Principais",
                    "active": True,
                    "id": "main-data",
                    "fields": [
                        {"label": field.verbose_name, "value": getattr(obj, field.name)}
                        for field in obj._meta.fields
                    ],
                }
            ]

        if "tabs" not in context:
            context["tabs"] = [
                {"id": "main-data", "label": "Geral", "icon": "fas fa-info-circle", "active": True}
            ]

        return context

# Marko Ciric 2023/0133

EMPTY_BUILD = {
    'cpu': None,
    'cpucooler': None,
    'motherboard': None,
    'ram': None,
    'storage': None,
    'gpu': None,
    'case': None,
    'powersupply': None,
}

SESSION_KEY = 'current_build_mock'


def get_current_build(request):
    """
    Mock implementacija. Vraća rečnik trenutno odabranih komponenti u aktivnoj
    sesiji (koristi se za proveru kompatibilnosti). Vrednosti su ili None ili
    instance odgovarajućeg Component podmodela (Cpu, Motherboard, ...).

    Struktura:
    {
        'cpu': CpuObject | None,
        'motherboard': MotherboardObject | None,
        'gpu': None,
        ...
    }
    """
    # TODO: Integrisati sa stvarnom request.session logikom kada bude gotova
    stored = request.session.get(SESSION_KEY)
    if not stored:
        return dict(EMPTY_BUILD)

    # Sesija čuva samo (component_type -> id), ovde se "hidrira" u objekte.
    from .utils import COMPONENT_DICT

    build = dict(EMPTY_BUILD)
    for component_type, component_id in stored.items():
        if component_id is None or component_type not in COMPONENT_DICT:
            continue
        model = COMPONENT_DICT[component_type]['model']
        build[component_type] = model.objects.filter(pk=component_id).first()

    return build


def set_component_in_build(request, component_type, component_id):
    """Dodaje/menja komponentu date kategorije u mock sesijskoj konfiguraciji."""
    stored = request.session.get(SESSION_KEY, {})
    stored[component_type] = component_id
    request.session[SESSION_KEY] = stored
    request.session.modified = True


def remove_component_from_build(request, component_type):
    stored = request.session.get(SESSION_KEY, {})
    stored[component_type] = None
    request.session[SESSION_KEY] = stored
    request.session.modified = True
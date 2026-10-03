#Aleksandar Raskovic 2023/0043
from django.db.models import Min
from django.http import Http404
from django.templatetags.static import static
from .models import *

COMPONENT_DICT = {
    "cpu": {
        "model": Cpu,
        "label": "Procesori",
        "spotlight_specs": [
            {"field": "corecount", "label": "Jezgara"},
            {"field": "socket", "label": "Soket"},
        ],
        "specs": [
            {"name": "manufacturer", "label": "Proizvođač", "kind": "choice", "field": "manufacturer"},
            {"name": "price", "label": "Cena", "kind": "range", "field": "min_price"},
            {"name": "corecount", "label": "Broj jezgara", "kind": "range", "field": "corecount"},
            {"name": "socket", "label": "Soket", "kind": "choice", "field": "socket"},
            {"name": "threadcount", "label": "Thread count", "kind": "none", "field": "threadcount"},
            {"name": "clockspeed", "label": "Clock speed", "kind": "none", "field": "clockspeed"},
            {"name": "integratedgpu", "label": "Integrated GPU", "kind": "none", "field": "integratedgpu"},
        ],
    },
    "cpucooler": {
        "model": Cpucooler,
        "label": "CPU hladnjaci",
        "spotlight_specs": [
            {"field": "coolertype", "label": ""},
            {"field": "socket", "label": "Soket"},
        ],
        "specs": [
            {"name": "manufacturer", "label": "Proizvođač", "kind": "choice", "field": "manufacturer"},
            {"name": "price", "label": "Cena", "kind": "range", "field": "min_price"},
            {"name": "coolertype", "label": "Tip", "kind": "choice", "field": "coolertype"},
            {"name": "socket", "label": "Soket", "kind": "choice", "field": "socket"},
        ],
    },
    "motherboard": {
        "model": Motherboard,
        "label": "Matične ploče",
        "spotlight_specs": [
            {"field": "socket", "label": "Soket"},
            {"field": "formfactor", "label": "Format"},
        ],
        "specs": [
            {"name": "manufacturer", "label": "Proizvođač", "kind": "choice", "field": "manufacturer"},
            {"name": "price", "label": "Cena", "kind": "range", "field": "min_price"},
            {"name": "socket", "label": "Soket", "kind": "choice", "field": "socket"},
            {"name": "formfactor", "label": "Format", "kind": "choice", "field": "formfactor"},
            {"name": "ramtype", "label": "Tip memorije", "kind": "choice", "field": "ramtype"},
            {"name": "ramslots", "label": "RAM slotovi", "kind": "range", "field": "ramslots"},
            {"name": "color", "label": "Boja", "kind": "choice", "field": "color"},
            {"name": "wifichip", "label": "Wifi chip", "kind": "none", "field": "wifichip"},
        ],
    },
    "ram": {
        "model": Ram,
        "label": "RAM",
        "spotlight_specs": [
            {"field": "memcapacity", "label": "Kapacitet"},
            {"field": "speed", "label": "Brzina"},
        ],
        "specs": [
            {"name": "manufacturer", "label": "Proizvođač", "kind": "choice", "field": "manufacturer"},
            {"name": "price", "label": "Cena", "kind": "range", "field": "min_price"},
            {"name": "type", "label": "Tip", "kind": "choice", "field": "type"},
            {"name": "speed", "label": "Brzina", "kind": "range", "field": "speed"},
            {"name": "memcapacity", "label": "Kapacitet", "kind": "choice", "field": "memcapacity"},
            {"name": "modulenum", "label": "Broj modula", "kind": "range", "field": "modulenum"},
            {"name": "color", "label": "Boja", "kind": "none", "field": "color"},
        ],
    },
    "storage": {
        "model": Storage,
        "label": "Diskovi",
        "spotlight_specs": [
            {"field": "capacity", "label": "Kapacitet"},
            {"field": "type", "label": "Tip"},
        ],
        "specs": [
            {"name": "manufacturer", "label": "Proizvođač", "kind": "choice", "field": "manufacturer"},
            {"name": "price", "label": "Cena", "kind": "range", "field": "min_price"},
            {"name": "type", "label": "Tip", "kind": "choice", "field": "type"},
            {"name": "slot", "label": "Slot", "kind": "choice", "field": "slot"},
            {"name": "capacity", "label": "Kapacitet", "kind": "choice", "field": "capacity"},
        ],
    },
    "gpu": {
        "model": Gpu,
        "label": "Grafičke kartice",
        "spotlight_specs": [
            {"field": "chip", "label": "Čip"},
            {"field": "memcapacity", "label": "Memorija"},
        ],
        "specs": [
            {"name": "manufacturer", "label": "Proizvođač", "kind": "choice", "field": "manufacturer"},
            {"name": "price", "label": "Cena", "kind": "range", "field": "min_price"},
            {"name": "chip", "label": "Čip", "kind": "choice", "field": "chip"},
            {"name": "memcapacity", "label": "Memorija", "kind": "choice", "field": "memcapacity"},
            {"name": "color", "label": "Boja", "kind": "none", "field": "color"},
        ],
    },
    "case": {
        "model": Case,
        "label": "Kućišta",
        "spotlight_specs": [
            {"field": "dimensions", "label": "Dimenzije"},
            {"field": "supportedmotherboards", "label": "Podržava"},
        ],
        "specs": [
            {"name": "manufacturer", "label": "Proizvođač", "kind": "choice", "field": "manufacturer"},
            {"name": "price", "label": "Cena", "kind": "range", "field": "min_price"},
            {"name": "color", "label": "Boja", "kind": "choice", "field": "color"},
            {"name": "supportedmotherboards", "label": "Podržane ploče", "kind": "choice_list", "field": "supportedmotherboards"},
            {"name": "dimensions", "label": "Dimenzije", "kind": "none", "field": "dimensions"},
        ],
    },
    "powersupply": {
        "model": Powersupply,
        "label": "Napajanja",
        "spotlight_specs": [
            {"field": "wattage", "label": "Snaga"},
            {"field": "efficiency", "label": "Efikasnost"},
        ],
        "specs": [
            {"name": "manufacturer", "label": "Proizvođač", "kind": "choice", "field": "manufacturer"},
            {"name": "price", "label": "Cena", "kind": "range", "field": "min_price"},
            {"name": "formfactor", "label": "Format", "kind": "choice", "field": "formfactor"},
            {"name": "efficiency", "label": "Efikasnost", "kind": "choice", "field": "efficiency"},
            {"name": "wattage", "label": "Snaga", "kind": "range", "field": "wattage"},
        ],
    },
}

def gen_spotlight_specs(result, component):
    spotlight_specs = []

    for spotlight_spec in component['spotlight_specs']:
        value = getattr(result, spotlight_spec['field'], None)
        if value in (None, ''):
            value = 'N/A'

        spotlight_specs.append({
            'label': spotlight_spec['label'],
            'value': value,
        })

    return spotlight_specs

def format_spec_value(value):
    if value in (None, ''):
        return 'N/A'

    return value

def gen_detail_specs(component_object, component_config):
    detail_specs = []

    for detail_spec in component_config['specs']:
        if detail_spec['kind'] == 'none':
            # This is a bit of a hack, but based on the requirements, 
            # kind='none' still needs to be shown in component details view.
            pass
        
        detail_specs.append({
            'label': detail_spec['label'],
            'value': format_spec_value(getattr(component_object, detail_spec['field'], None)),
        })

    return detail_specs

def get_component_image_url(component_object):
    if component_object.imagepath.startswith(('http://', 'https://')):
        return component_object.imagepath

    return static(component_object.imagepath)

def get_component_by_id(id):
    component = Component.objects.filter(id=id)
    if not component:
        raise Http404("Komponenta ne postoji!")

    for component_type, component_config in COMPONENT_DICT.items():
        component_object = component_config['model'].objects.filter(pk=id).first()
        if component_object is not None:
            return component_type, component_config, component_object

    raise Http404("Komponenta ne postoji!")

def get_build_by_id(id):
    try:
        build = Build.objects.get(pk=id)
        return build

    except Build.DoesNotExist:
        raise Http404("Racunar ne postoji!")

def gen_price_context(component_object):
    prices = list(Componentprice.objects.filter(idcomponent_id=component_object.id).order_by('price'))
    lowest_price = prices[0] if prices else None

    return {
        'prices': prices,
        'lowest_price': lowest_price,
        'lowest_price_display': f'{lowest_price.price} RSD' if lowest_price else 'N/A',
        'lowest_price_store': f'kod {lowest_price.shopname}' if lowest_price else 'Trenutno nema ponuda',
    }

def gen_search_results(filtered_results, component, type):
    results = []

    for result in filtered_results:
        results.append({
            'type': type,
            'component': result,
            'spotlight_specs': gen_spotlight_specs(result, component),
            'price_display': f'{result.min_price} RSD' if result.min_price is not None else 'N/A',
        })

    return results

def gen_filter_param_names(component):
    param_names = set()

    for spec in component['specs']:
        if spec['kind'] == 'none':
            continue
        
        name = spec['name']

        if spec['kind'] == 'choice' or spec['kind'] == 'choice_list':
            param_names.add(name)
        elif spec['kind'] == 'range':
            param_names.add(f'{name}_min')
            param_names.add(f'{name}_max')

    return param_names

def gen_hidden_params(requestGET, exclude_names):
    hidden_params = []

    for name, values in requestGET.lists():
        if name in exclude_names:
            continue

        for value in values:
            hidden_params.append({
                'name': name,
                'value': value,
            })

    return hidden_params

def gen_sidebar_filters(component, requestGET, base_queryset):
    sidebar_filters = []

    for spec in component['specs']:
        if spec['kind'] == 'none':
            continue

        novi_filter = {
            'name': spec['name'],
            'label': spec['label'],
            'kind': spec['kind'],
        }
        field = spec['field']
        if spec['kind'] == 'choice':

            possible_values = (
                base_queryset
                .values_list(field, flat=True)
                .exclude(**{f"{field}__isnull": True})
                .distinct()
                .order_by(field)
            )

            selected_values = requestGET.getlist(spec['name'])
            novi_filter['options'] = [
                {
                    'value': value,
                    'checked': str(value) in selected_values
                }
                for value in possible_values
                if value != ''
            ]
        elif spec['kind'] == 'choice_list':
            all_values = set()
            for item in base_queryset.values_list(field, flat=True).exclude(**{f"{field}__isnull": True}):
                if item and item.strip():
                    values = [v.strip() for v in item.split(',')]
                    all_values.update(values)
            
            selected_values = requestGET.getlist(spec['name'])
            novi_filter['options'] = [
                {
                    'value': value,
                    'checked': value in selected_values
                }
                for value in sorted(all_values)
                if value != ''
            ]
        elif spec['kind'] == 'range':
            novi_filter["min_name"] = f"{spec['name']}_min"
            novi_filter["max_name"] = f"{spec['name']}_max"
            novi_filter["min_value"] = requestGET.get(f"{spec['name']}_min", "")
            novi_filter["max_value"] = requestGET.get(f"{spec['name']}_max", "")
        else:
            raise Exception('nepoznat tip filtera')

        sidebar_filters.append(novi_filter)

    return sidebar_filters

def gen_compatibility_url_params(component_type, build):
    from urllib.parse import urlencode
    params = {}

    cpu = build.get('cpu')
    cooler = build.get('cpucooler')
    motherboard = build.get('motherboard')
    ram = build.get('ram')
    disk = build.get('storage')
    case = build.get('case')
    psu = build.get('powersupply')

    if component_type == 'cpu':
        if motherboard:
            params['socket'] = motherboard.socket
    if component_type == 'cpucooler':
        if motherboard:
            params['socket'] = motherboard.socket
        elif cpu:
            params['socket'] = cpu.socket
    elif component_type == 'motherboard':
        if cpu:
            params['socket'] = cpu.socket
        if ram:
            params['ramtype'] = ram.type
        if case:
            params['formfactor'] = case.supportedmotherboards.split(',')[0].strip()
    elif component_type == 'ram':
        if motherboard:
            params['type'] = motherboard.ramtype
    elif component_type == 'case':
        if motherboard:
            params['supportedmotherboards'] = motherboard.formfactor
    elif component_type == 'powersupply':
        total_consumption = sum(
            (getattr(c, 'powerconsumption', None) or 0)
            for t, c in build.items()
            if t != 'powersupply' and c is not None
        )
        if total_consumption > 0:
            params['wattage_min'] = total_consumption

    return urlencode(params) if params else ''

def serialize_recommendation(item):
    component = item['component']
    return {
        'id': component.id,
        'component_type': item['component_type'],
        'name': item['name'],
        'manufacturer': item['manufacturer'],
        'price': item['price'],
        'price_display': item['price_display'],
        'image_url': get_component_image_url(component),
    }
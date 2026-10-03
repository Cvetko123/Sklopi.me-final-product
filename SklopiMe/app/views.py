#Aleksandar Cvetkovic 2023/0150
#Aleksandar Raskovic 2023/0043
#Marko Ciric 2023/0133
import json

from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Q, Model
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods

from .auth_forms import LoginForm, RegisterForm
from .models import *
from .session_helpers import get_current_build, set_component_in_build, remove_component_from_build
from .llm import OpenAILLMProvider, MockLLMProvider
from .configurator_service import (
    ConfiguratorService, InvalidRequestError, NoResultsError,
)
from .utils import *
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from openai import OpenAI

_openrouter_client = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=os.environ.get('OPENROUTER_API_KEY'),
)

_configurator_service = ConfiguratorService(
    llm_provider=OpenAILLMProvider(
        client=_openrouter_client,
        model='google/gemma-4-31b-it:free',
    )
)


def index(request):
    """
    Naslovna strana

    **Opis:**

    Prikazuje naslovnu stranicu sa najnovijim zavrsenim racunarima.

    **Template**

    :template:`index.html`

    :param request: HTTP Zahtev
    """
    popular_builds = Build.objects.all().all().order_by('-numoflikes')[:3]
    context = {'popular_builds': popular_builds}
    return render(request, 'index.html',context)


def components(request):
    """
        Stranica za izbor tipa komponente

        **Opis:**

        Prikazuje stranicu za izbor tipa komponente koji se pretražuje.

        **Template**

        :template:`components.html`

        :param request: HTTP Zahtev
    """
    return render(request, 'components.html')


def component_search(request, type):
    """
            Stranica za pretragu komponenti

            **Opis:**

            Prikazuje stranicu za pretragu određenog tipa komponente. Rezultate pretrage moguće je filtrirati, sortirati ili pretraživati po tekstu.
            Filteri se zadaju preko GET parametara, bilo kroz sidebar stranice, bilo kroz automatsku proveru kompatibilnosti od strane konfiguratora.

            **Template**

            :template:`component_search.html`

            :param request: HTTP Zahtev
            :param type: String koji predstavlja tip komponente koja se pretražuje. Mora da bude jedan od tipova komponente definisanih u COMPONENT_DICT.
    """
    if type not in COMPONENT_DICT:
        raise Http404("Nepoznat tip komponente")
    component = COMPONENT_DICT[type]

    model = component['model']

    base_queryset = model.objects.annotate(min_price=Min('componentprice__price'))

    filtered_results = base_queryset

    sidebar_filters = gen_sidebar_filters(component, request.GET, base_queryset)
    filter_param_names = gen_filter_param_names(component)

    search_query = request.GET.get('q')
    if search_query:
        filtered_results = filtered_results.filter(
            Q(name__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    for filter in component['specs']:
        name = filter['name']
        kind = filter['kind']
        field = filter['field']

        if kind == 'choice':
            values = request.GET.getlist(name)
            if values:
                filtered_results = filtered_results.filter(**{f"{field}__in": values})
        elif kind == 'choice_list':
            values = request.GET.getlist(name)
            if values:
                query = Q()
                for value in values:
                    pattern = f"(^|,\\s*){value}(\\s*,|$)" # regex za proveru da li je izmedju zareza ok, __contains ne radi zbog substrings (npr mATX i ATX)
                    query |= Q(**{f"{field}__iregex": pattern})
                filtered_results = filtered_results.filter(query)
        elif kind == 'range':
            min_value = request.GET.get(f"{name}_min")
            max_value = request.GET.get(f"{name}_max")

            if min_value:
                filtered_results = filtered_results.filter(**{f"{field}__gte": min_value})

            if max_value:
                filtered_results = filtered_results.filter(**{f"{field}__lte": max_value})

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        filtered_results = filtered_results.order_by('min_price', 'name')
    elif sort == 'price_desc':
        filtered_results = filtered_results.order_by('-min_price', 'name')
    elif sort == 'name_asc':
        filtered_results = filtered_results.order_by('name')
    elif sort == 'name_desc':
        filtered_results = filtered_results.order_by('-name')

    context = {
        'query': request.GET,
        'search_query': search_query or '',
        'sort': sort or '',
        'component_type': type,
        'sidebar_filters': sidebar_filters,
        'filter_hidden_params': gen_hidden_params(request.GET, filter_param_names),
        'search_hidden_params': gen_hidden_params(request.GET, {'q'}),
        'sort_hidden_params': gen_hidden_params(request.GET, {'sort'}),
        'results': gen_search_results(filtered_results.all(), component, type),
    }
    return render(request, 'component_search.html', context=context)


def component_detail(request, id):
    """
        Stranica za prikaz detalja jedne komponente

        **Opis:**

        Prikazuje stranicu za prikaz detalja jedne komponente na osnovu prosleđenog ID-a.

        **Template**

        :template:`component_detail.html`

    :param request: HTTP Zahtev
    :param id: Integer koji predstavlja identifikator komponente u bazi podataka. Ukoliko komponenta ne postoji vraća se status 404.
    """
    component_type, component_config, component_object = get_component_by_id(id)
    price_context = gen_price_context(component_object)

    context = {
        'component_type': component_type,
        'component_label': component_config['label'],
        'component': component_object,
        'image_url': get_component_image_url(component_object),
        'detail_specs': gen_detail_specs(component_object, component_config),
        'prices': price_context['prices'],
        'lowest_price': price_context['lowest_price'],
        'lowest_price_display': price_context['lowest_price_display'],
        'lowest_price_store': price_context['lowest_price_store'],
    }
    return render(request, 'component_detail.html', context)


#----------------------User Auth-----------------------

def loginF(request):
    """
    Stranica za prijavu korisnika

    **Opis:**

    Prikazuje stranicu za prijavu sa formularom. Podržava prijavu pomoću email-a i lozinke.
    Nakon uspešne prijave, korisnik se redirektuje na naslovnu stranicu.

    **Template**

    :template:`login.html`

    :param request: HTTP Zahtev
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            backend = 'app.backends.EmailBackend'
            user.backend = backend
            login(request, user)
            return redirect('profile')
    else:
        form = LoginForm(request)

    return render(request, 'login.html', {'form': form})


def register(request):
    """
    Stranica za registraciju novog korisnika

    **Opis:**

    Prikazuje stranicu za registraciju sa formularom. Omogućava novom korisniku da se registruje sa email adresom, korisničkim imenom
    i lozinkom. Nakon uspešne registracije, korisniku se pravi profil i automatski se prijavljuje na sistem.

    **Template**

    :template:`register.html`

    :param request: HTTP Zahtev
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = 'app.backends.EmailBackend'
            user.backend = backend
            userprofile = UserProfile.objects.create(user=user)
            userprofile.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def logoutF(request):
    """
    Odjava korisnika

    **Opis:**

    Odjavljuje trenutno prijavljenog korisnika iz sistema i redirektuje ga na naslovnu stranicu.

    :param request: HTTP Zahtev
    """
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def profilePage(request):
    """
    Stranica korisničkog profila

    **Opis:**

    Prikazuje profil trenutno prijavljenog korisnika sa statistikom o njegovim kompjuterima.
    Prikazuje broj objavljenih kompjuterskih konfiguracija, ukupan broj primljenih lajkova i listu svih korisnikovih gotovih racunara.
    Zahteva prijavu korisnika.

    **Template**

    :template:`account.html`

    :param request: HTTP Zahtev
    """
    user_profile = UserProfile.objects.get(user=request.user)
    user_builds = (
        Build.objects.filter(iduser=user_profile)
        .prefetch_related('images')
    )


    num_of_builds = user_builds.count()
    num_of_likes = 0
    for build in user_builds:
        num_of_likes += build.numoflikes

    context = {'user': request.user, 'num_of_builds': num_of_builds, 'num_of_likes': num_of_likes, 'user_builds': user_builds}
    return render(request, 'account.html', context)

def profilePageId(request, id):
    """
        Stranica korisničkog profila na osnovu ID

        **Opis:**

        Prikazuje profil korisnika na osnovu njegovog ID-a sa statistikom o njegovim kompjuterima.
        Prikazuje broj objavljenih kompjuterskih konfiguracija, ukupan broj primljenih lajkova i listu svih korisnikovih gotovih racunara.

        **Template**

        :template:`account.html`

        :param request: HTTP Zahtev
        :param id: ID korisnika
    """
    user = User.objects.filter(id=id)
    if user is None:
        return redirect('index')
    user = user.first()
    user_profile = UserProfile.objects.get(user=user)

    user_builds = (
        Build.objects.filter(iduser=user_profile)
        .prefetch_related('images')
    )

    num_of_builds = user_builds.count()
    num_of_likes = 0
    for build in user_builds:
        num_of_likes += build.numoflikes

    context = {'user': User.objects.get(id=id), 'num_of_builds': num_of_builds, 'num_of_likes': num_of_likes, 'user_builds': user_builds}
    return render(request, 'account.html', context)


@login_required(login_url='login')
@require_POST
def delete_account(request):
    """
    Brisanje korisničkog naloga

    **Opis:**

    Briše trenutnog korisnika iz sistema i sve njegove podatke. Zahteva POST zahtev za zaštitu od slučajnog brisanja.
    Nakon brisanja, korisnik je odjavljivan i redirektovan na naslovnu stranicu.
    Zahteva prijavu korisnika.

    :param request: HTTP Zahtev
    """
    user = request.user
    logout(request)
    user.delete()
    return redirect('index')

#------------------------------------------------------------
def build_detail(request, id):
    """
        Stranica za prikaz detalja gotove konfiguracije

        **Opis:**

        Prikazuje detaljne informacije o izabranoj konfiguraciji (build-u). Učitava sve
        pripadajuće komponente, benchmark rezultate i slike. Ukoliko je korisnik prijavljen,
        proverava da li je on vlasnik konfiguracije (ili superuser) i dohvati njegov prethodni glas.

        **Template**

        :template:`build_detail.html`

        :param request: HTTP Zahtev
        :param id: Integer identifikator konfiguracije (Build) u bazi podataka.
    """
    build = get_build_by_id(id)

    build_components = (
        Buildcomponent.objects
        .filter(idbuild=build)
        .select_related('idcomponent')
    )
    benchmarks = build.benchmarks.all()
    images = build.images.all()

    user_vote = None
    is_owner = False

    if request.user.is_authenticated:
        is_owner = build.iduser.user_id == request.user.id or request.user.is_superuser

        user_profile = UserProfile.objects.filter(user=request.user).first()
        if user_profile is not None:
            existing_vote = Buildlikedislike.objects.filter(
                idbuild=build, iduser=user_profile
            ).first()
            if existing_vote is not None:
                user_vote = 'like' if existing_vote.like == 1 else 'dislike'

    context = {
        'build': build,
        'build_components': build_components,
        'benchmarks': benchmarks,
        'images': images,
        'user_vote': user_vote,
        'is_owner': is_owner,
    }
    return render(request, 'build_detail.html', context)


def build_search(request):
    """
        Stranica za pretragu i filtriranje objavljenih konfiguracija

        **Opis:**

        Prikazuje stranicu sa listom svih objavljenih konfiguracija računara. Omogućava pretragu
        preko tekstualnog upita (naziv/opis), filtriranje prema opsegu ukupne cene, kao i sortiranje
        prema ceni, popularnosti (lajkovima) i nazivu.

        **Template**

        :template:`build_search.html`

        :param request: HTTP Zahtev
    """
    builds = Build.objects.select_related('iduser', 'iduser__user').all()

    search_query = request.GET.get('q', '').strip()
    if search_query:
        builds = builds.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if min_price.isdigit():
        builds = builds.filter(totalprice__gte=int(min_price))

    if max_price.isdigit():
        builds = builds.filter(totalprice__lte=int(max_price))

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        builds = builds.order_by('totalprice')
    elif sort == 'price_desc':
        builds = builds.order_by('-totalprice')
    elif sort == 'most_liked':
        builds = builds.order_by('-numoflikes')
    elif sort == 'most_disliked':
        builds = builds.order_by('-numofdislikes')
    elif sort == 'name_asc':
        builds = builds.order_by('name')
    elif sort == 'name_desc':
        builds = builds.order_by('-name')

    context = {
        'builds': builds,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    }
    return render(request, 'build_search.html', context)


@login_required(login_url='login')
@require_POST
def rate_build(request, id):
    """
        Endpoint za ocenjivanje konfiguracije (Like/Dislike)

        **Opis:**

        Obrađuje asinhroni (AJAX) POST zahtev za dodavanje, izmenu ili uklanjanje ocene
        trenutne konfiguracije. Glas se šalje unutar JSON tela zahteva. Automatski ažurira
        i čuva ukupan broj lajkova i dislajkova na modelu konfiguracije.

        :param request: HTTP Zahtev koji sadrži JSON telo sa ključem 'vote' ('like' ili 'dislike').
        :param id: Integer identifikator konfiguracije koja se ocenjuje.
        :return: JsonResponse sa statusom operacije, trenutnim glasom i ažurnim brojačima.
    """
    build = get_build_by_id(id)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return JsonResponse({
            'error': 'Korisnički profil ne postoji. Molimo kontaktirajte podršku ili proverite podešavanja naloga.'
        }, status=400)

    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Nevalidan JSON.'}, status=400)

    vote = data.get('vote')
    if vote not in ('like', 'dislike'):
        return JsonResponse({'error': "Polje 'vote' mora biti 'like' ili 'dislike'."}, status=400)

    vote_value = 1 if vote == 'like' else 0

    existing_vote = Buildlikedislike.objects.filter(idbuild=build, iduser=user_profile).first()

    if existing_vote and existing_vote.like == vote_value:
        existing_vote.delete()
        status = 'removed'
        user_vote = None
    elif existing_vote:
        existing_vote.like = vote_value
        existing_vote.save()
        status = 'changed'
        user_vote = vote
    else:
        Buildlikedislike.objects.create(idbuild=build, iduser=user_profile, like=vote_value)
        status = 'added'
        user_vote = vote

    build.numoflikes = Buildlikedislike.objects.filter(idbuild=build, like=1).count()
    build.numofdislikes = Buildlikedislike.objects.filter(idbuild=build, like=0).count()
    build.save(update_fields=['numoflikes', 'numofdislikes'])

    return JsonResponse({
        'status': status,
        'user_vote': user_vote,
        'likes': build.numoflikes,
        'dislikes': build.numofdislikes,
    })


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def edit_build(request, id):
    """
        Endpoint za pregled i izmenu osnovnih podataka konfiguracije

        **Opis:**

        Omogućava promenu naziva i opisa konfiguracije. Pristup je dozvoljen isključivo
        autoru konfiguracije ili administratoru sistema (superuser). Ukoliko je zahtev GET,
        vraća trenutne podatke, a ukoliko je POST, vrši validaciju i čuvanje izmena.

        :param request: HTTP Zahtev (GET za čitanje, POST za ažuriranje podataka).
        :param id: Integer identifikator konfiguracije koja se menja.
        :return: JsonResponse sa statusom operacije i ažuriranim podacima.
    """
    build = get_build_by_id(id)

    if build.iduser.user_id != request.user.id and request.user.is_superuser is False:
        raise Http404('Nemate dozvolu da izmenite ovaj build.')

    if request.method == 'POST':
        new_name = request.POST.get('name', '').strip()
        new_description = request.POST.get('description', '').strip()

        if not new_name or not new_description:
            return JsonResponse({'error': 'Naslov i opis su obavezni.'}, status=400)

        build.name = new_name
        build.description = new_description
        build.save(update_fields=['name', 'description'])

        return JsonResponse({
            'status': 'ok',
            'name': build.name,
            'description': build.description,
        })

    return JsonResponse({'name': build.name, 'description': build.description})


@login_required(login_url='login')
@require_POST
def delete_build(request, id):
    """
        Brisanje objavljene konfiguracije

        **Opis:**

        Briše izabranu konfiguraciju iz baze podataka ukoliko zahtev šalje vlasnik konfiguracije
        ili superuser. Nakon uspešnog brisanja, vrši se redirekcija na pretragu konfiguracija.

        :param request: HTTP Zahtev (mora biti POST).
        :param id: Integer identifikator konfiguracije koja se briše.
    """
    build = get_build_by_id(id)

    if build.iduser.user_id != request.user.id and request.user.is_superuser is False:
        raise Http404('Nemate dozvolu da obrišete ovaj build.')

    build.delete()
    return redirect('build_search')


@login_required(login_url='login')
def publish_build(request):
    """
        Stranica i proces za objavljivanje trenutne konfiguracije iz sesije

        **Opis:**

        Prikazuje formu za unos detalja (naziv, opis, slike, benchmark rezultati) pre objave
        konfiguracije koja je sastavljena u sesiji. Prilikom POST zahteva vrši se validacija
        obaveznih komponenti (CPU, Matična ploča, RAM), čuvanje slika na fajl sistem i upisivanje
        svih podataka u bazu. Na kraju prazni konfiguraciju i istoriju četovanja iz sesije.

        **Template**

        :template:`publish_build.html`

        :param request: HTTP Zahtev.
    """
    user_profile = UserProfile.objects.get(user=request.user)
    build_session = get_current_build(request)

    build_rows = []
    total_price = 0
    components_to_save = []

    for component_type, config in COMPONENT_DICT.items():
        component = build_session.get(component_type)
        price = None
        if component is not None:
            price_context = gen_price_context(component)
            if price_context and 'lowest_price' in price_context:
                price = price_context['lowest_price']
                if price is not None:
                    total_price += price.price
            components_to_save.append(component)

        build_rows.append({
            'component_type': component_type,
            'label': config['label'],
            'component': component,
            'price_display': f'{price.price} RSD' if price else None,
        })

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        errors = []

        if not name or not description:
            errors.append("Ime i opis su obavenzna polja.")

        cpu = build_session.get('cpu')
        motherboard = build_session.get('motherboard')
        ram = build_session.get('ram')

        if not cpu or not motherboard or not ram:
            missing_components = []
            if not cpu:
                missing_components.append('CPU')
            if not motherboard:
                missing_components.append('Motherboard')
            if not ram:
                missing_components.append('RAM')
            errors.append(f"Morate izabrati sledeće komponente da bi objavili računar: {', '.join(missing_components)}.")

        uploaded_images = request.FILES.getlist('images[]')
        if len(uploaded_images) > 5:
            errors.append("Možete izabrati maksimalno 5 slika.")

        if len(uploaded_images) == 0:
            errors.append("Potrebno je dodati barem jednu sliku.")

        if errors:
            context = {
                'build_rows': build_rows,
                'total_price_display': f'{total_price} RSD',
                'errors': errors
            }
            return render(request, 'publish_build.html', context)


        new_build = Build.objects.create(
            name=name,
            description=description,
            totalprice=int(total_price),
            numoflikes=0,
            numofdislikes=0,
            iduser=user_profile
        )

        for comp in components_to_save:
            Buildcomponent.objects.create(
                idcomponent=comp,
                idbuild=new_build
            )

        target_directory = os.path.join(settings.BASE_DIR, 'static', 'build_images')

        if not os.path.exists(target_directory):
            os.makedirs(target_directory, exist_ok=True)

        storage_system = FileSystemStorage(location=target_directory)
        uploaded_images = request.FILES.getlist('images[]')
        for image_file in uploaded_images:
            saved_filename = storage_system.save(image_file.name, image_file)

            relative_path = os.path.join('build_images', saved_filename)

            Buildimage.objects.create(
                idbuild=new_build,
                image=relative_path
            )

        benchmark_names = request.POST.getlist('benchmark_name[]')
        benchmark_values = request.POST.getlist('benchmark_value[]')

        for b_name, b_value in zip(benchmark_names, benchmark_values):
            b_name = b_name.strip()
            b_value = b_value.strip()
            if b_name and b_value:
                Benchmark.objects.create(
                    name=b_name,
                    value=b_value,
                    idbuild=new_build
                )

        for component_type in COMPONENT_DICT.keys():
            remove_component_from_build(request, component_type)

        if 'chat_history' in request.session:
            del request.session['chat_history']

        return redirect('build_search')

    context = {
        'build_rows': build_rows,
        'total_price_display': f'{total_price} RSD',
    }
    return render(request, 'publish_build.html', context)


@login_required(login_url='login')
def configurator_page(request):
    """
        Glavna stranica interaktivnog AI konfiguratora

        **Opis:**

        Prikazuje radni prostor konfiguratora sa tabelom trenutno izabranih komponenti iz sesije,
        njihovim pojedinačnim i ukupnim cenama, statusom kompatibilnosti celog build-a (i obrazloženjem
        ukoliko postoji konflikt), kao i istorijom četovanja sa AI asistentom.

        **Template**

        :template:`configurator.html`

        :param request: HTTP Zahtev.
    """
    from .compatibility import CompatibilityValidator
    build = get_current_build(request)

    build_rows = []
    total_price = 0
    for component_type, config in COMPONENT_DICT.items():
        component = build.get(component_type)
        price = None
        if component is not None:
            price_context = gen_price_context(component)
            price = price_context['lowest_price']
            if price is not None:
                total_price += price.price

        filter_params = gen_compatibility_url_params(component_type, build)
        build_rows.append({
            'component_type': component_type,
            'label': config['label'],
            'component': component,
            'price_display': f'{price.price} RSD' if price else None,
            'filter_params': filter_params,
        })

    validator = CompatibilityValidator()
    compatibility_ok = True
    compatibility_reason = 'Empty'
    for component_type, component in build.items():
        if component is None:
            continue
        compatibility_reason = ''
        remaining = {k: v for k, v in build.items() if k != component_type}
        result = validator.is_compatible(component_type, component, remaining)
        if not result.compatible:
            compatibility_ok = False
            compatibility_reason = result.reason
            break

    chat_history = request.session.get('chat_history', [])

    context = {
        'build_rows': build_rows,
        'total_price_display': f'{total_price} RSD',
        'compatibility_ok': compatibility_ok,
        'compatibility_reason': compatibility_reason,
        'chat_history': chat_history
    }
    return render(request, 'configurator.html', context)


@login_required(login_url='login')
def get_all_component_links(request):
    """
    Vraća sve linkove za najniže cene komponenti iz trenutne konfiguracije.

    Prolazi kroz sve komponente u trenutnoj konfiguraciji i prikuplja
    linkove sa najnižim cenama od dostupnih prodavnica.

    :param request: HTTP Zahtev
    :return: JSON sa listom linkova komponenti
    """
    build = get_current_build(request)
    links = []

    for component_type, config in COMPONENT_DICT.items():
        component = build.get(component_type)
        if component is not None:
            price_context = gen_price_context(component)
            lowest_price = price_context['lowest_price']
            if lowest_price and lowest_price.link:
                links.append({
                    'name': component.name,
                    'url': lowest_price.link,
                    'shop': lowest_price.shopname,
                })

    return JsonResponse({'links': links})


@login_required(login_url='login')
@require_POST
def configurator_chat(request):
    """
        Endpoint za komunikaciju sa AI asistentom u konfiguratoru

        **Opis:**

        Prima korisničku poruku preko asinhronog POST zahteva, prosleđuje je servisu konfiguratora
        zajedno sa stanjem trenutnog build-a, prima generisani odgovor (preporuke ili pun build) i
        ažurira istoriju ćaskanja u sesiji korisnika.

        :param request: HTTP Zahtev sa JSON telom koje sadrži ključ 'message'.
        :return: JsonResponse sa tekstualnim odgovorom i strukturiranim preporukama komponenti.
    """
    try:
        body = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Nevalidan JSON.'}, status=400)

    user_text = (body.get('message') or '').strip()
    if not user_text:
        return JsonResponse({'error': "Polje 'message' je obavezno."}, status=400)

    current_build = get_current_build(request)

    chat_history = request.session.get('chat_history', [])

    try:
        result = _configurator_service.handle_message(user_text, current_build)
    except InvalidRequestError as exc:
        return JsonResponse({
            'status': 'invalid_request',
            'message': f'Nažalost, ne mogu da ispunim taj zahtev: {exc}',
        })
    except NoResultsError as exc:
        return JsonResponse({
            'status': 'no_results',
            'message': str(exc),
        })

    response_payload = {'status': 'ok', 'message': result['message']}

    if 'recommendations' in result:
        response_payload['recommendations'] = [
            serialize_recommendation(item) for item in result['recommendations']
        ]
    elif 'recommendations_by_category' in result:
        response_payload['recommendations_by_category'] = {
            component_type: [serialize_recommendation(item) for item in items]
            for component_type, items in result['recommendations_by_category'].items()
        }

    chat_history.append({'sender': 'user', 'message': user_text})
    chat_history.append({
        'sender': 'ai',
        'status': response_payload.get('status'),
        'message': response_payload.get('message'),
        'recommendations': response_payload.get('recommendations'),
        'recommendations_by_category': response_payload.get('recommendations_by_category')
    })

    request.session['chat_history'] = chat_history
    request.session.modified = True

    return JsonResponse(response_payload)


@login_required(login_url='login')
@require_POST
def configurator_add_component(request):
    """
    Endpoint za dodavanje komponente u trenutnu konfiguraciju uz proveru kompatibilnosti.

    Slanjem POST zahteva u JSON formatu na ovaj endpoint zahteva se dodavanje komponente u trenutnu konfiguraciju.

    Za razliku od manuelnog dodavanja, ovaj endpoint vraća JSON error ako komponenta nije kompatibilna sa prethodno izabranim.

    :component_type: Tip komponente koja se dodaje.
    :component_id: Identifikator komponente koja se dodaje.

    Ukoliko je komponenta uspesno dodata, prelazimo na stranicu konfiguratora.
    Ukoliko komponenta ne postoji, nije kompatibilna, ili tip komponente nije validan, vracamo JSON objekat sa statusom 400.

    :param request: HTTP POST zahtev gde je body JSON objekat sa argumentima zahteva.
    """
    try:
        body = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Nevalidan JSON.'}, status=400)

    component_type = body.get('component_type')
    component_id = body.get('component_id')

    if component_type not in COMPONENT_DICT or not component_id:
        return JsonResponse({'error': 'Nedostaju ili su nevalidni component_type/component_id.'}, status=400)

    model = COMPONENT_DICT[component_type]['model']
    candidate = model.objects.filter(pk=component_id).first()
    if candidate is None:
        return JsonResponse({'error': 'Komponenta ne postoji.'}, status=404)

    current_build = get_current_build(request)
    from .compatibility import CompatibilityValidator
    check = CompatibilityValidator().is_compatible(component_type, candidate, current_build)
    if not check.compatible:
        return JsonResponse({'error': f'Komponenta nije kompatibilna: {check.reason}'}, status=409)

    set_component_in_build(request, component_type, candidate.id)

    return JsonResponse({
        'status': 'added',
        'component_type': component_type,
        'component_id': candidate.id,
        'name': candidate.name,
    })


# Tu je kad korisnik rucno dodaje komponente i ne treba mu provera kompatibilnosti
@login_required(login_url='login')
@require_POST
def configurator_add_manual(request):
    """
    Endpoint za dodavanje komponente u trenutnu konfiguraciju bez provere kompatibilnosti.

    Slanjem POST zahteva na ovaj endpoint zahteva se dodavanje komponente u trenutnu konfiguraciju.

    Potrebni argumenti u POST zahtevu:

    :component_type: Tip komponente koja se dodaje.
    :component_id: Identifikator komponente koja se dodaje.

    Ukoliko je komponenta uspesno dodata, prelazimo na stranicu konfiguratora.
    Ukoliko komponenta ne postoji, ili tip komponente nije validan, vracamo JSON objekat sa statusom 400.

    :param request: HTTP POST zahtev
    """
    component_type = request.POST.get('component_type')
    component_id = request.POST.get('component_id')

    if component_type not in COMPONENT_DICT or not component_id:
        return JsonResponse({'error': 'Nedostaju ili su nevalidni component_type/component_id.'}, status=400)

    model = COMPONENT_DICT[component_type]['model']
    candidate = model.objects.filter(pk=component_id).first()
    if candidate is None:
        return JsonResponse({'error': 'Komponenta ne postoji.'}, status=404)

    set_component_in_build(request, component_type, component_id)
    return redirect('configurator')


@login_required(login_url='login')
@require_POST
def configurator_remove_component(request):
    """
    Endpoint za brisanje komponente iz trenutne konfiguracije.

    Slanjem POST zahteva na ovaj endpoint zahteva se brisanje komponente iz trenutne konfiguracije.
    Jedini argument u POST zahtevu koji je potreban jeste tip komponente koja se briše.

    Ukoliko je komponenta uspesno obrisana, se vraca na stranicu za konfigurator.
    Ukoliko komponenta ne postoji u trenutnoj konfiguraciji, ne radi se ništa i se vraca na stranicu za konfigurator.

    :param request: HTTP POST zahtev
    """
    component_type = request.POST.get('component_type')
    remove_component_from_build(request, component_type)
    return redirect('configurator')

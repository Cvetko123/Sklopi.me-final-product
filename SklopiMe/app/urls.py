# Aleksandar Cvetkovic 2023/0150
# Aleksandar Raskovic 2023/0043
import profile

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('components/', components, name='components'),
    path('components/<type>', component_search, name='component_search'),
    path('component/<int:id>', component_detail, name='component_detail'),
    path('login/',loginF,name='login'),
    path('register/',register,name='register'),
    path('logout/',logoutF,name='logout'),
    path('profile/',profilePage,name='profile'),
    path('profile/<int:id>', profilePageId, name='profile_id'),
    path('deleteAcc', delete_account, name='delete_account'),
    path('builds/', build_search, name='build_search'),
    path('build/<int:id>/', build_detail, name='build_detail'),
    path('build/<int:id>/rate', rate_build, name='rate_build'),
    path('build/<int:id>/edit', edit_build, name='edit_build'),
    path('build/<int:id>/delete', delete_build, name='delete_build'),
    path('build/publish/', publish_build, name='publish_build_page'),
    path('configurator/', configurator_page, name='configurator'),
    path('configurator/chat/', configurator_chat, name='configurator_chat'),
    path('configurator/links/', get_all_component_links, name='get_all_component_links'),
    path('configurator/add/', configurator_add_component, name='configurator_add'),
    path('configurator/remove', configurator_remove_component, name='configurator_remove'),
    path('configurator/testing', configurator_add_manual, name='configurator_add_manual')
]
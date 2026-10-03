import json
import tempfile
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from app.configurator_service import InvalidRequestError
from app.models import (
    User,
    UserProfile,
    Cpu,
    Componentprice,
    Build,
    Buildcomponent,
    Buildlikedislike,
    Motherboard,
    Ram,
)


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User setup
        cls.user = User.objects.create_user(
            username='testuser',
            email='tester@testing.com',
            password='DovoljnoDugacakPass123!'
        )
        cls.userprofile = UserProfile.objects.create(
            user=cls.user
        )

        # CPU setup
        cls.cpu1 = Cpu.objects.create(
            name="AMD Ryzen 5 5600",
            description="Gaming CPU",
            manufacturer="AMD",
            imagepath="cpu.png",
            powerconsumption=65,
            corecount=6,
            threadcount=12,
            clockspeed=3.5,
            socket="AM4",
            integratedgpu=0,
        )

        cls.cpu2 = Cpu.objects.create(
            name="Intel Core i5-12400",
            description="Intel CPU",
            manufacturer="Intel",
            imagepath="cpu2.png",
            powerconsumption=65,
            corecount=6,
            threadcount=12,
            clockspeed=2.5,
            socket="LGA1700",
            integratedgpu=1,
        )

        cls.cpu3 = Cpu.objects.create(
            name="AMD Ryzen 9 7950X",
            description="High end",
            manufacturer="AMD",
            imagepath="cpu3.png",
            powerconsumption=170,
            corecount=16,
            threadcount=32,
            clockspeed=4.5,
            socket="AM5",
            integratedgpu=1,
        )

        Componentprice.objects.create(
            idcomponent=cls.cpu1,
            shopname="Gigatron",
            price=20000,
            link="a"
        )

        Componentprice.objects.create(
            idcomponent=cls.cpu2,
            shopname="Gigatron",
            price=25000,
            link="b"
        )

        Componentprice.objects.create(
            idcomponent=cls.cpu3,
            shopname="Gigatron",
            price=50000,
            link="c"
        )

    def setUp(self):
        self.client = Client()

    def login_user(self):
        self.client.login(
            username="testuser",
            password="DovoljnoDugacakPass123!"
        )

    def test_index(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    # ---------- components ----------

    def test_components_page(self):
        response = self.client.get(reverse("components"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components.html")


    # ---------- component_search ----------

    def test_invalid_component_type(self):
        response = self.client.get(
            reverse("component_search", args=["xyz"])
        )

        self.assertEqual(response.status_code, 404)


    def test_cpu_page_loads(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "component_search.html")


    def test_search_by_name(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"q": "7950"}
        )

        self.assertContains(response, "7950X")
        self.assertNotContains(response, "12400")


    def test_search_by_manufacturer(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"q": "Intel"}
        )

        self.assertContains(response, "12400")
        self.assertNotContains(response, "7950X")


    def test_filter_manufacturer(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"manufacturer": "AMD"}
        )

        self.assertContains(response, "5600")
        self.assertContains(response, "7950X")
        self.assertNotContains(response, "12400")


    def test_filter_socket(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"socket": "AM4"}
        )

        self.assertContains(response, "5600")
        self.assertNotContains(response, "7950X")
        self.assertNotContains(response, "12400")


    def test_filter_price_min(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"price_min": 30000}
        )

        self.assertContains(response, "7950X")
        self.assertNotContains(response, "5600")
        self.assertNotContains(response, "12400")


    def test_filter_price_max(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"price_max": 22000}
        )

        self.assertContains(response, "5600")
        self.assertNotContains(response, "12400")
        self.assertNotContains(response, "7950X")


    def test_filter_corecount(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {
                "corecount_min": 12,
                "corecount_max": 20,
            }
        )

        self.assertContains(response, "7950X")
        self.assertNotContains(response, "5600")


    def test_sort_price_ascending(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"sort": "price_asc"}
        )

        results = response.context["results"]

        self.assertEqual(
            results[0]["component"].name,
            "AMD Ryzen 5 5600"
        )


    def test_sort_price_descending(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"sort": "price_desc"}
        )

        results = response.context["results"]

        self.assertEqual(
            results[0]["component"].name,
            "AMD Ryzen 9 7950X"
        )


    def test_sort_name(self):
        response = self.client.get(
            reverse("component_search", args=["cpu"]),
            {"sort": "name_asc"}
        )

        results = response.context["results"]

        names = [r["component"].name for r in results]

        self.assertEqual(names, sorted(names))


    # ---------- component_detail ----------

    def test_component_detail(self):
        response = self.client.get(
            reverse("component_detail", args=[self.cpu1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "component_detail.html")

        self.assertEqual(
            response.context["component"].name,
            "AMD Ryzen 5 5600"
        )

        self.assertEqual(
            response.context["lowest_price"].price,
            20000
        )


    def test_component_detail_404(self):
        response = self.client.get(
            reverse("component_detail", args=[999999])
        )

        self.assertEqual(response.status_code, 404)

    # ---------- configurator ----------

    def test_configurator_requires_login(self):
        response = self.client.get(
            reverse("configurator")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_configurator_page_loads(self):
        self.login_user()

        response = self.client.get(
            reverse("configurator")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "configurator.html"
        )

        self.assertIn(
            "build_rows",
            response.context
        )

    # ---------- configurator_add_manual ----------

    def test_add_manual_cpu_updates_session(self):
        self.login_user()

        response = self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "cpu",
                "component_id": self.cpu1.id,
            },
        )

        self.assertEqual(response.status_code, 302)

        session = self.client.session

        self.assertEqual(
            int(session["current_build_mock"]["cpu"]),
            self.cpu1.id
        )

    def test_add_manual_replaces_existing_cpu(self):
        self.login_user()

        self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "cpu",
                "component_id": self.cpu1.id,
            },
        )

        self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "cpu",
                "component_id": self.cpu2.id,
            },
        )

        session = self.client.session

        self.assertEqual(
            int(session["current_build_mock"]["cpu"]),
            self.cpu2.id
        )

    def test_add_manual_invalid_component_type_does_not_update_session(self):
        self.login_user()

        response = self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "invalid",
                "component_id": self.cpu1.id,
            },
        )

        self.assertEqual(response.status_code, 400)

        session = self.client.session

        self.assertNotIn(
            "invalid",
            session.get("current_build_mock", {})
        )

    def test_add_manual_missing_component_id(self):
        self.login_user()

        response = self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "cpu",
            },
        )

        self.assertEqual(response.status_code, 400)

        session = self.client.session

        self.assertNotIn(
            "cpu",
            session.get("current_build_mock", {})
        )

    def test_add_manual_nonexistent_component(self):
        self.login_user()

        response = self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "cpu",
                "component_id": 999999,
            },
        )

        self.assertEqual(response.status_code, 404)

        session = self.client.session

        self.assertNotIn(
            "cpu",
            session.get("current_build_mock", {})
        )

    def test_add_manual_redirects_to_configurator(self):
        self.login_user()

        response = self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "cpu",
                "component_id": self.cpu1.id,
            },
        )

        self.assertRedirects(
            response,
            reverse("configurator")
        )

    # ---------- configurator_remove ----------

    def test_remove_component_updates_session(self):
        self.login_user()

        # Add CPU
        self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "cpu",
                "component_id": self.cpu1.id,
            },
        )

        session = self.client.session

        self.assertEqual(
            int(session["current_build_mock"]["cpu"]),
            self.cpu1.id
        )

        # Remove CPU
        response = self.client.post(
            reverse("configurator_remove"),
            {
                "component_type": "cpu",
            },
        )

        self.assertEqual(response.status_code, 302)

        session = self.client.session

        self.assertIsNone(
            session["current_build_mock"]["cpu"]
        )

    def test_configurator_reads_saved_component(self):
        self.login_user()

        self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": "cpu",
                "component_id": self.cpu1.id,
            },
        )

        response = self.client.get(
            reverse("configurator")
        )

        self.assertEqual(response.status_code, 200)

        rows = response.context["build_rows"]

        cpu_row = next(
            row for row in rows
            if row["component_type"] == "cpu"
        )

        self.assertEqual(
            cpu_row["component"].name,
            "AMD Ryzen 5 5600"
        )

    def test_remove_nonexistent_component_does_not_fail(self):
        self.login_user()

        response = self.client.post(
            reverse("configurator_remove"),
            {
                "component_type": "gpu",
            },
        )

        self.assertEqual(response.status_code, 302)

        session = self.client.session

        self.assertIsNone(
            session["current_build_mock"]["gpu"]
        )

    # ---------- helpers ----------

    def create_build(self, name="Test Build", description="A build",
                     totalprice=100000, numoflikes=0, numofdislikes=0,
                     user_profile=None):
        return Build.objects.create(
            name=name,
            description=description,
            totalprice=totalprice,
            numoflikes=numoflikes,
            numofdislikes=numofdislikes,
            iduser=user_profile or self.userprofile,
        )

    def create_motherboard(self):
        return Motherboard.objects.create(
            name="MSI B550",
            description="Motherboard",
            manufacturer="MSI",
            imagepath="mb.png",
            powerconsumption=30,
            socket="AM4",
            formfactor="ATX",
            ramslots=4,
            ramtype="DDR4",
            color="Black",
            wifichip="None",
        )

    def create_ram(self):
        return Ram.objects.create(
            name="Corsair Vengeance 16GB",
            description="RAM",
            manufacturer="Corsair",
            imagepath="ram.png",
            powerconsumption=10,
            type="DDR4",
            speed=3200,
            memcapacity="16GB",
            modulenum=2,
            color="Black",
        )

    # ---------- build_search ----------

    def test_build_search_context_defaults(self):
        response = self.client.get(reverse("build_search"))

        self.assertEqual(response.context["search_query"], "")
        self.assertEqual(response.context["min_price"], "")
        self.assertEqual(response.context["max_price"], "")
        self.assertEqual(response.context["sort"], "newest")

    def test_build_search_by_name_and_description(self):
        self.create_build(name="Gaming Beast bonus", description="Fast")
        self.create_build(name="Office PC", description="Cheap bonus")

        self.create_build(name="Ne treba da se pojavi 1", description="Fast")
        self.create_build(name="Ne treba da se pojavi 2", description="Cheap")

        response = self.client.get(
            reverse("build_search"),
            {"q": "bonus"}
        )

        self.assertContains(response, "Gaming Beast bonus")
        self.assertContains(response, "Office PC")

        self.assertNotContains(response, "Ne treba da se pojavi 1")
        self.assertNotContains(response, "Ne treba da se pojavi 2")

    def test_build_search_filter_min_price(self):
        self.create_build(name="Cheap Build", totalprice=50000)
        self.create_build(name="Expensive Build", totalprice=200000)

        response = self.client.get(
            reverse("build_search"),
            {"min_price": 100000}
        )

        self.assertContains(response, "Expensive Build")
        self.assertNotContains(response, "Cheap Build")

    def test_build_search_filter_max_price(self):
        self.create_build(name="Cheap Build", totalprice=50000)
        self.create_build(name="Expensive Build", totalprice=200000)

        response = self.client.get(
            reverse("build_search"),
            {"max_price": 100000}
        )

        self.assertContains(response, "Cheap Build")
        self.assertNotContains(response, "Expensive Build")

    def test_build_search_non_digit_price_ignored(self):
        self.create_build(name="Cheap Build", totalprice=50000)
        self.create_build(name="Expensive Build", totalprice=200000)

        response = self.client.get(
            reverse("build_search"),
            {"min_price": "abc", "max_price": "xyz"}
        )

        self.assertContains(response, "Cheap Build")
        self.assertContains(response, "Expensive Build")

    def test_build_search_sort_price_ascending(self):
        self.create_build(name="Expensive Build", totalprice=200000)
        self.create_build(name="Cheap Build", totalprice=50000)

        response = self.client.get(
            reverse("build_search"),
            {"sort": "price_asc"}
        )

        builds = list(response.context["builds"])

        self.assertEqual(builds[0].name, "Cheap Build")

    def test_build_search_sort_price_descending(self):
        self.create_build(name="Expensive Build", totalprice=200000)
        self.create_build(name="Cheap Build", totalprice=50000)

        response = self.client.get(
            reverse("build_search"),
            {"sort": "price_desc"}
        )

        builds = list(response.context["builds"])

        self.assertEqual(builds[0].name, "Expensive Build")

    def test_build_search_sort_most_liked(self):
        self.create_build(name="Popular Build", numoflikes=10)
        self.create_build(name="Unpopular Build", numoflikes=1)

        response = self.client.get(
            reverse("build_search"),
            {"sort": "most_liked"}
        )

        builds = list(response.context["builds"])

        self.assertEqual(builds[0].name, "Popular Build")

    def test_build_search_sort_most_disliked(self):
        self.create_build(name="Hated Build", numofdislikes=10)
        self.create_build(name="Fine Build", numofdislikes=1)

        response = self.client.get(
            reverse("build_search"),
            {"sort": "most_disliked"}
        )

        builds = list(response.context["builds"])

        self.assertEqual(builds[0].name, "Hated Build")

    def test_build_search_sort_name_ascending(self):
        self.create_build(name="Zeta Build")
        self.create_build(name="Alpha Build")

        response = self.client.get(
            reverse("build_search"),
            {"sort": "name_asc"}
        )

        names = [b.name for b in response.context["builds"]]

        self.assertEqual(names, sorted(names))

    def test_build_search_sort_name_descending(self):
        self.create_build(name="Zeta Build")
        self.create_build(name="Alpha Build")

        response = self.client.get(
            reverse("build_search"),
            {"sort": "name_desc"}
        )

        names = [b.name for b in response.context["builds"]]

        self.assertEqual(names, sorted(names, reverse=True))

    # ---------- build_detail ----------

    def test_build_detail_page(self):
        build = self.create_build(name="Detailed Build")

        response = self.client.get(
            reverse("build_detail", args=[build.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "build_detail.html")

        self.assertEqual(
            response.context["build"].name,
            "Detailed Build"
        )

    def test_build_detail_404(self):
        response = self.client.get(
            reverse("build_detail", args=[676767])
        )

        self.assertEqual(response.status_code, 404)


    def test_build_detail_user_vote_like(self):
        self.login_user()
        build = self.create_build()

        Buildlikedislike.objects.create(
            idbuild=build,
            iduser=self.userprofile,
            like=1
        )

        response = self.client.get(
            reverse("build_detail", args=[build.pk])
        )

        self.assertEqual(response.context["user_vote"], "like")

    def test_build_detail_user_vote_dislike(self):
        self.login_user()
        build = self.create_build()

        Buildlikedislike.objects.create(
            idbuild=build,
            iduser=self.userprofile,
            like=0
        )

        response = self.client.get(
            reverse("build_detail", args=[build.pk])
        )

        self.assertEqual(response.context["user_vote"], "dislike")

    # ---------- rate_build ----------

    def test_rate_build_requires_login(self):
        build = self.create_build()

        response = self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({"vote": "like"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_rate_build_requires_post(self):
        self.login_user()
        build = self.create_build()

        response = self.client.get(
            reverse("rate_build", args=[build.pk])
        )

        self.assertEqual(response.status_code, 405)

    def test_rate_build_add_like(self):
        self.login_user()
        build = self.create_build()

        response = self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({"vote": "like"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "added")
        self.assertEqual(data["user_vote"], "like")
        self.assertEqual(data["likes"], 1)
        self.assertEqual(data["dislikes"], 0)

    def test_rate_build_add_dislike(self):
        self.login_user()
        build = self.create_build()

        response = self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({"vote": "dislike"}),
            content_type="application/json"
        )

        data = response.json()

        self.assertEqual(data["status"], "added")
        self.assertEqual(data["user_vote"], "dislike")
        self.assertEqual(data["likes"], 0)
        self.assertEqual(data["dislikes"], 1)

    def test_rate_build_change_vote(self):
        self.login_user()
        build = self.create_build()

        self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({"vote": "like"}),
            content_type="application/json"
        )

        response = self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({"vote": "dislike"}),
            content_type="application/json"
        )

        data = response.json()

        self.assertEqual(data["status"], "changed")
        self.assertEqual(data["user_vote"], "dislike")
        self.assertEqual(data["likes"], 0)
        self.assertEqual(data["dislikes"], 1)

    def test_rate_build_remove_vote(self):
        self.login_user()
        build = self.create_build()

        self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({"vote": "like"}),
            content_type="application/json"
        )

        response = self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({"vote": "like"}),
            content_type="application/json"
        )

        data = response.json()

        self.assertEqual(data["status"], "removed")
        self.assertIsNone(data["user_vote"])
        self.assertEqual(data["likes"], 0)
        self.assertEqual(data["dislikes"], 0)

    def test_rate_build_invalid_vote_value(self):
        self.login_user()
        build = self.create_build()

        response = self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({"vote": "necu da glasam"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_rate_build_missing_vote(self):
        self.login_user()
        build = self.create_build()

        response = self.client.post(
            reverse("rate_build", args=[build.pk]),
            data=json.dumps({}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_rate_build_invalid_json(self):
        self.login_user()
        build = self.create_build()

        response = self.client.post(
            reverse("rate_build", args=[build.pk]),
            data="not-json",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_rate_build_nonexistent_build(self):
        self.login_user()

        response = self.client.post(
            reverse("rate_build", args=[676767]),
            data=json.dumps({"vote": "like"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)

    # ---------- edit_build ----------

    def test_edit_build_get_returns_data(self):
        self.login_user()
        build = self.create_build(name="My Build", description="Some desc")

        response = self.client.get(
            reverse("edit_build", args=[build.pk])
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["name"], "My Build")
        self.assertEqual(data["description"], "Some desc")

    def test_edit_build_post_updates_data(self):
        self.login_user()
        build = self.create_build()

        response = self.client.post(
            reverse("edit_build", args=[build.pk]),
            {
                "name": "New Name",
                "description": "New description",
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["name"], "New Name")
        self.assertEqual(data["description"], "New description")

        build.refresh_from_db()

        self.assertEqual(build.name, "New Name")
        self.assertEqual(build.description, "New description")

    def test_edit_build_post_missing_fields(self):
        self.login_user()
        build = self.create_build()

        response = self.client.post(
            reverse("edit_build", args=[build.pk]),
            {
                "name": "",
                "description": "",
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_edit_build_not_owner(self):
        other_user = User.objects.create_user(
            username="editother",
            email="editother@testing.com",
            password="DovoljnoDugacakPass123!"
        )
        other_profile = UserProfile.objects.create(user=other_user)
        build = self.create_build(user_profile=other_profile)

        self.login_user()

        response = self.client.get(
            reverse("edit_build", args=[build.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_edit_build_superuser_allowed(self):
        other_user = User.objects.create_user(
            username="editowner",
            email="editowner@testing.com",
            password="DovoljnoDugacakPass123!"
        )
        other_profile = UserProfile.objects.create(user=other_user)
        build = self.create_build(user_profile=other_profile)

        superuser = User.objects.create_superuser(
            username="editadmin",
            email="editadmin@testing.com",
            password="DovoljnoDugacakPass123!"
        )
        UserProfile.objects.create(user=superuser)

        self.client.login(
            username="editadmin",
            password="DovoljnoDugacakPass123!"
        )

        response = self.client.get(
            reverse("edit_build", args=[build.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_edit_build_nonexistent(self):
        self.login_user()

        response = self.client.get(
            reverse("edit_build", args=[999999])
        )

        self.assertEqual(response.status_code, 404)

    def test_edit_build_invalid_method(self):
        self.login_user()
        build = self.create_build()

        response = self.client.put(
            reverse("edit_build", args=[build.pk])
        )

        self.assertEqual(response.status_code, 405)

    # ---------- delete_build ----------

    def test_delete_build_requires_post(self):
        self.login_user()
        build = self.create_build()

        response = self.client.get(
            reverse("delete_build", args=[build.pk])
        )

        self.assertEqual(response.status_code, 405)

    def test_delete_build_owner_deletes(self):
        self.login_user()
        build = self.create_build()

        response = self.client.post(
            reverse("delete_build", args=[build.pk])
        )

        self.assertRedirects(response, reverse("build_search"))
        self.assertFalse(Build.objects.filter(pk=build.pk).exists())

    def test_delete_build_not_owner(self):
        other_user = User.objects.create_user(
            username="delother",
            email="delother@testing.com",
            password="DovoljnoDugacakPass123!"
        )
        other_profile = UserProfile.objects.create(user=other_user)
        build = self.create_build(user_profile=other_profile)

        self.login_user()

        response = self.client.post(
            reverse("delete_build", args=[build.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Build.objects.filter(pk=build.pk).exists())

    def test_delete_build_superuser_allowed(self):
        other_user = User.objects.create_user(
            username="delowner",
            email="delowner@testing.com",
            password="DovoljnoDugacakPass123!"
        )
        other_profile = UserProfile.objects.create(user=other_user)
        build = self.create_build(user_profile=other_profile)

        superuser = User.objects.create_superuser(
            username="deladmin",
            email="deladmin@testing.com",
            password="DovoljnoDugacakPass123!"
        )
        UserProfile.objects.create(user=superuser)

        self.client.login(
            username="deladmin",
            password="DovoljnoDugacakPass123!"
        )

        response = self.client.post(
            reverse("delete_build", args=[build.pk])
        )

        self.assertRedirects(response, reverse("build_search"))
        self.assertFalse(Build.objects.filter(pk=build.pk).exists())

    def test_delete_build_nonexistent(self):
        self.login_user()

        response = self.client.post(
            reverse("delete_build", args=[999999])
        )

        self.assertEqual(response.status_code, 404)

    # ---------- publish_build ----------

    def add_component_to_session(self, component_type, component_id):
        self.client.post(
            reverse("configurator_add_manual"),
            {
                "component_type": component_type,
                "component_id": component_id,
            },
        )

    def test_publish_build_requires_login(self):
        response = self.client.get(
            reverse("publish_build_page")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_publish_build_post_missing_components(self):
        self.login_user()

        response = self.client.post(
            reverse("publish_build_page"),
            {
                "name": "My Build",
                "description": "Nice build",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["errors"]) > 0)
        self.assertEqual(Build.objects.count(), 0)

    def test_publish_build_post_missing_name_and_description(self):
        self.login_user()

        motherboard = self.create_motherboard()
        ram = self.create_ram()

        self.add_component_to_session("cpu", self.cpu1.id)
        self.add_component_to_session("motherboard", motherboard.id)
        self.add_component_to_session("ram", ram.id)

        image = SimpleUploadedFile(
            "image.jpg", b"file_content", content_type="image/jpeg"
        )

        response = self.client.post(
            reverse("publish_build_page"),
            {
                "name": "",
                "description": "",
                "images[]": [image],
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["errors"]) > 0)
        self.assertEqual(Build.objects.count(), 0)

    def test_publish_build_post_no_images(self):
        self.login_user()

        motherboard = self.create_motherboard()
        ram = self.create_ram()

        self.add_component_to_session("cpu", self.cpu1.id)
        self.add_component_to_session("motherboard", motherboard.id)
        self.add_component_to_session("ram", ram.id)

        response = self.client.post(
            reverse("publish_build_page"),
            {
                "name": "My Build",
                "description": "Nice build",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["errors"]) > 0)
        self.assertEqual(Build.objects.count(), 0)

    def test_publish_build_post_too_many_images(self):
        self.login_user()

        motherboard = self.create_motherboard()
        ram = self.create_ram()

        self.add_component_to_session("cpu", self.cpu1.id)
        self.add_component_to_session("motherboard", motherboard.id)
        self.add_component_to_session("ram", ram.id)

        images = [
            SimpleUploadedFile(
                f"image{i}.jpg", b"file_content", content_type="image/jpeg"
            )
            for i in range(6)
        ]

        response = self.client.post(
            reverse("publish_build_page"),
            {
                "name": "My Build",
                "description": "Nice build",
                "images[]": images,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["errors"]) > 0)
        self.assertEqual(Build.objects.count(), 0)

    def test_publish_build_post_success(self):
        self.login_user()

        motherboard = self.create_motherboard()
        ram = self.create_ram()

        self.add_component_to_session("cpu", self.cpu1.id)
        self.add_component_to_session("motherboard", motherboard.id)
        self.add_component_to_session("ram", ram.id)

        image = SimpleUploadedFile(
            "image.jpg", b"file_content", content_type="image/jpeg"
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            with override_settings(BASE_DIR=tmp_dir):
                response = self.client.post(
                    reverse("publish_build_page"),
                    {
                        "name": "My Build",
                        "description": "Nice build",
                        "images[]": [image],
                        "benchmark_name[]": ["Cinebench"],
                        "benchmark_value[]": ["12345"],
                    }
                )

        self.assertRedirects(response, reverse("build_search"))
        self.assertEqual(Build.objects.count(), 1)

        build = Build.objects.first()

        self.assertEqual(build.name, "My Build")
        self.assertEqual(build.description, "Nice build")
        self.assertEqual(
            Buildcomponent.objects.filter(idbuild=build).count(),
            3
        )


    # ---------- Autentifikacija i Profil ----------

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_profile_page_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_profile_page_loads_for_logged_user(self):
        self.login_user()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')

    def test_profile_page_id_loads(self):
        self.login_user()
        response = self.client.get(reverse('profile_id', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects(self):
        self.login_user()
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    # ---------- Registracija ----------

    def test_registration_successful(self):
        response = self.client.post(reverse('register'), {
            'username': 'novikorisnik',
            'email': 'novi@testing.com',
            'password1': 'JakaLozinka123!',
            'password2': 'JakaLozinka123!'
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(User.objects.filter(username='novikorisnik').exists())

    def test_registration_missing_username(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': 'novi@testing.com',
            'password1': 'JakaLozinka123!',
            'password2': 'JakaLozinka123!'
        })
        self.assertIn(response.status_code, [200, 400])
        self.assertTrue(len(response.content) > 0)

    def test_registration_missing_email(self):
        response = self.client.post(reverse('register'), {
            'username': 'novikorisnik',
            'email': '',
            'password1': 'JakaLozinka123!',
            'password2': 'JakaLozinka123!'
        })
        self.assertIn(response.status_code, [200, 400])

    def test_registration_missing_password(self):
        response = self.client.post(reverse('register'), {
            'username': 'novikorisnik',
            'email': 'novi@testing.com',
            'password1': '',
            'password2': 'JakaLozinka123!'
        })
        self.assertIn(response.status_code, [200, 400])

    def test_registration_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'novikorisnik',
            'email': 'novi@testing.com',
            'password1': 'JakaLozinka123!',
            'password2': 'DrugaLozinka!'
        })
        self.assertIn(response.status_code, [200, 400])

    # ---------- Prijava i Brisanje naloga ----------

    def test_login_successful(self):
        korisnik = User.objects.create_user(username='logintest', email='login@test.com',
                                            password='DovoljnoDugacakPass123!')

        response = self.client.post(reverse('login'), {
            'username': 'logintest',
            'password': 'DovoljnoDugacakPass123!'
        })
        self.assertIn(response.status_code, [200, 302])

    def test_login_wrong_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'nepostojeci',
            'password': 'DovoljnoDugacakPass123!'
        })
        self.assertTrue(response.context['form'].errors)

    def test_login_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'PogresnaLozinka!'
        })
        self.assertTrue(response.context['form'].errors)

    def test_delete_account_requires_login(self):
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)

    def test_delete_account_successful(self):
        self.login_user()
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    # ---------- Chatbot (MockLLMProvider) ----------

    def _post_chat(self, message):
        return self.client.post(
            reverse("configurator_chat"),
            data=json.dumps({"message": message}),
            content_type="application/json",
        )

    @patch('app.views._configurator_service.handle_message')
    def test_chatbot_prompt_recommend_component(self, mock_handle_message):
        self.login_user()

        mock_handle_message.return_value = {
            'message': 'Pronašao sam 1 predlog.',
            'recommendations': [
                {
                    'component': self.cpu1,
                    'component_type': 'cpu',
                    'name': self.cpu1.name,
                    'manufacturer': self.cpu1.manufacturer,
                    'price': 20000,
                    'price_display': '20000 RSD',
                }
            ],
        }

        response = self._post_chat("Preporuci mi AMD procesor")

        self.assertEqual(response.status_code, 200)
        mock_handle_message.assert_called_once()

        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertIn('message', data)
        self.assertIn('recommendations', data)
        self.assertEqual(len(data['recommendations']), 1)

    @patch('app.views._configurator_service.handle_message')
    def test_chatbot_prompt_full_build(self, mock_handle_message):
        self.login_user()

        mock_handle_message.return_value = {
            'message': 'Evo predloga konfiguracije na osnovu zadatog budžeta.',
            'recommendations_by_category': {
                'cpu': [
                    {
                        'component': self.cpu1,
                        'component_type': 'cpu',
                        'name': self.cpu1.name,
                        'manufacturer': self.cpu1.manufacturer,
                        'price': 20000,
                        'price_display': '20000 RSD',
                    }
                ],
            },
        }

        response = self._post_chat("Sklopi mi gaming racunar za 120000 rsd")

        self.assertEqual(response.status_code, 200)
        mock_handle_message.assert_called_once()

        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertIn('recommendations_by_category', data)
        self.assertIn('cpu', data['recommendations_by_category'])

    @patch('app.views._configurator_service.handle_message')
    def test_chatbot_invalid_request_returns_400(self, mock_handle_message):
        self.login_user()

        mock_handle_message.side_effect = InvalidRequestError(
            "Zahtev nema veze sa računarima."
        )

        response = self._post_chat("Kako da skuvam kafu?")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['status'], 'invalid_request')
        self.assertIn('message', data)
        self.assertIn('Zahtev nema veze sa računarima.', data['message'])

    @patch('app.views._configurator_service.handle_message')
    def test_chatbot_history_increments(self, mock_handle_message):
        self.login_user()

        mock_handle_message.return_value = {
            'message': 'Kako vam mogu pomoći?',
            'recommendations': [],
        }

        response = self._post_chat("Zdravo")
        self.assertEqual(response.status_code, 200)

        history_after_first = self.client.session['chat_history']
        self.assertEqual(len(history_after_first), 2)  # user + ai poruka
        self.assertEqual(history_after_first[0]['sender'], 'user')
        self.assertEqual(history_after_first[0]['message'], 'Zdravo')
        self.assertEqual(history_after_first[1]['sender'], 'ai')

        response = self._post_chat("Treba mi grafička karta")
        self.assertEqual(response.status_code, 200)

        history_after_second = self.client.session['chat_history']
        self.assertEqual(len(history_after_second), 4)

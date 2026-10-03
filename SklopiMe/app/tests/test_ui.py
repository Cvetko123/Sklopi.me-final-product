from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Model
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from app.models import User, Cpu, Componentprice, Build, Motherboard, Ram, Buildcomponent, UserProfile

import logging
import time
import os
import tempfile

logging.getLogger("django.server").setLevel(logging.ERROR)


class TestSystem(StaticLiveServerTestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            email="tester@testing.com",
            password="DovoljnoDugacakPass123!"
        )

        self.cpu = Cpu.objects.create(
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

        Componentprice.objects.create(
            idcomponent=self.cpu,
            shopname="Gigatron",
            price=20000,
            link="https://example.com"
        )

        self.cpu2 = Cpu.objects.create(
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

        Componentprice.objects.create(
            idcomponent=self.cpu2,
            shopname="Gigatron",
            price=25000,
            link="https://example.com"
        )

        self.cpu3 = Cpu.objects.create(
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
            idcomponent=self.cpu3,
            shopname="Gigatron",
            price=50000,
            link="https://example.com"
        )

        from app.models import UserProfile
        self.userprofile = UserProfile.objects.create(
            user=self.user
        )

        self.motherboard = Motherboard.objects.create(
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

        Componentprice.objects.create(
            idcomponent=self.motherboard,
            shopname="Gigatron",
            price=15000,
            link="https://example.com"
        )

        self.ram = Ram.objects.create(
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

        Componentprice.objects.create(
            idcomponent=self.ram,
            shopname="Gigatron",
            price=10000,
            link="https://example.com"
        )

        self.build = Build.objects.create(
            name="Gaming Build",
            description="A powerful gaming build",
            totalprice=100000,
            numoflikes=0,
            numofdislikes=0,
            iduser=self.userprofile,
        )

        Buildcomponent.objects.create(
            idbuild=self.build,
            idcomponent=self.cpu,
        )

        Buildcomponent.objects.create(
            idbuild=self.build,
            idcomponent=self.motherboard,
        )

        Buildcomponent.objects.create(
            idbuild=self.build,
            idcomponent=self.ram,
        )

        self.build2 = Build.objects.create(
            name="Workstation Build",
            description="A powerful workstation",
            totalprice=200000,
            numoflikes=1,
            numofdislikes=0,
            iduser=self.userprofile,
        )

        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome( options=options )


    def tearDown(self):
        self.driver.quit()

    def login_ui(self):
        self.driver.get(self.live_server_url + reverse("login"))
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("DovoljnoDugacakPass123!")
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1)

    def test_components_page_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse("components")
        )

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Pretraži Komponente",
            body.text
        )


    def test_open_cpu_components_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse("components")
        )


        cpu_button = self.driver.find_element(
            By.LINK_TEXT,
            "CPU"
        )

        cpu_button.click()

        time.sleep(1)

        self.assertIn(
            "/components/cpu",
            self.driver.current_url
        )

    def test_all_component_links_exist(self):
        self.driver.get(
            self.live_server_url +
            reverse("components")
        )

        links = [
            "CPU",
            "CPU Hladnjaci",
            "Matične ploče",
            "RAM",
            "Diskovi",
            "GPU",
            "Kućišta",
            "Napajanja",
        ]



        for link in links:
            element = self.driver.find_element(
                By.LINK_TEXT,
                link
            )

            time.sleep(1)

            self.assertTrue(
                element.is_displayed()
            )

    def test_component_search_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_search",
                args=["cpu"]
            )
        )


        search = self.driver.find_element(
            By.NAME,
            "q"
        )

        time.sleep(1)

        search.send_keys(
            "5600"
        )

        time.sleep(1)


        self.driver.find_element(
            By.CLASS_NAME,
            "primary"
        ).click()


        time.sleep(1)


        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )


        self.assertIn(
            "Ryzen 5 5600",
            body.text
        )


    def test_component_detail_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        time.sleep(1)


        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )


        self.assertIn(
            "AMD Ryzen 5 5600",
            body.text
        )


        self.assertIn(
            "20000",
            body.text
        )


    def test_add_component_requires_login_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )


        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()


        time.sleep(1)


        self.assertIn(
            "/login",
            self.driver.current_url
        )


    def test_logged_user_can_add_component_ui(self):

        self.driver.get(
            self.live_server_url +
            "/login"
        )

        time.sleep(1)


        self.driver.find_element(
            By.NAME,
            "username"
        ).send_keys(
            "testuser"
        )

        self.driver.find_element(
            By.NAME,
            "password"
        ).send_keys(
            "DovoljnoDugacakPass123!"
        )


        self.driver.find_element(
            By.CLASS_NAME,
            "submit-btn"
        ).click()


        time.sleep(1)


        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )


        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()


        time.sleep(1)


        self.assertIn(
            "/configurator",
            self.driver.current_url
        )

    # ---------------- FILTERS ----------------

    def test_manufacturer_filter_ui(self):
        self.driver.get(
            self.live_server_url +
            reverse(
                "component_search",
                args=["cpu"]
            )
        )

        amd_checkbox = self.driver.find_element(
            By.CSS_SELECTOR,
            "input[name='manufacturer'][value='AMD']"
        )

        amd_checkbox.click()

        self.driver.find_element(
            By.CLASS_NAME,
            "search-action-btn"
        ).click()

        time.sleep(1)

        results = self.driver.find_element(
            By.CLASS_NAME,
            "results-list"
        )

        self.assertIn(
            "AMD Ryzen 5 5600",
            results.text
        )

        self.assertNotIn(
            "Intel Core i5-12400",
            results.text
        )

    def test_price_min_filter_ui(self):
        self.driver.get(
            self.live_server_url +
            reverse(
                "component_search",
                args=["cpu"]
            )
        )

        price_min = self.driver.find_element(
            By.NAME,
            "price_min"
        )

        price_min.send_keys("30000")

        self.driver.find_element(
            By.CLASS_NAME,
            "search-action-btn"
        ).click()

        time.sleep(1)

        results = self.driver.find_element(
            By.CLASS_NAME,
            "results-list"
        )

        self.assertIn(
            "AMD Ryzen 9 7950X",
            results.text
        )

        self.assertNotIn(
            "AMD Ryzen 5 5600",
            results.text
        )

    def test_search_no_results_ui(self):
        self.driver.get(
            self.live_server_url +
            reverse(
                "component_search",
                args=["cpu"]
            )
        )

        time.sleep(1)

        search = self.driver.find_element(
            By.CLASS_NAME,
            "search-box"
        )

        search.send_keys("THIS_DOES_NOT_EXIST")

        self.driver.find_element(
            By.CSS_SELECTOR,
            ".search-action-btn.primary"
        ).click()

        time.sleep(1)

        empty = self.driver.find_element(
            By.CLASS_NAME,
            "empty-state"
        )

        self.assertIn(
            "Nema rezultata",
            empty.text
        )

    def test_sort_price_descending_ui(self):
        self.driver.get(
            self.live_server_url +
            reverse(
                "component_search",
                args=["cpu"]
            )
        )

        time.sleep(1)

        # open sort dropdown
        sort_button = self.driver.find_element(
            By.CLASS_NAME,
            "sort-btn"
        )

        sort_button.click()

        time.sleep(1)

        sort = self.driver.find_element(
            By.CSS_SELECTOR,
            "input[value='price_desc']"
        )

        sort.click()

        time.sleep(1)

        results = self.driver.find_elements(
            By.CLASS_NAME,
            "item-name"
        )

        self.assertIn(
            "7950X",
            results[0].text
        )

    # ---------------- CONFIGURATOR ----------------

    def login_ui(self):
        self.driver.get(
            self.live_server_url +
            reverse("login")
        )

        self.driver.find_element(
            By.NAME,
            "username"
        ).send_keys(
            "tester@testing.com"
        )

        self.driver.find_element(
            By.NAME,
            "password"
        ).send_keys(
            "DovoljnoDugacakPass123!"
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "submit-btn"
        ).click()

        time.sleep(1)

        self.assertNotIn(
            "/login",
            self.driver.current_url
        )

    def test_configurator_requires_login_ui(self):
        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        time.sleep(1)

        self.assertIn(
            "/login",
            self.driver.current_url
        )

    def test_configurator_page_loads_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Trenutna konfiguracija",
            body.text
        )

    def test_configurator_add_cpu_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.assertIn(
            "/configurator",
            self.driver.current_url
        )

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "AMD Ryzen 5 5600",
            body.text
        )

    def test_configurator_remove_cpu_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "AMD Ryzen 5 5600",
            body.text
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "remove-btn"
        ).click()

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Izaberite",
            body.text
        )

    def test_configurator_saved_component_after_reload_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        self.driver.refresh()

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "AMD Ryzen 5 5600",
            body.text
        )

    def test_configurator_total_price_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "20000",
            body.text
        )

    # ---------------- BUILD SEARCH ----------------

    def test_build_search_page_loads_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse("build_search")
        )

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Gaming Build",
            body.text
        )

    def test_build_search_with_search_query_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse("build_search")
        )

        search = self.driver.find_element(
            By.CLASS_NAME,
            "search-box"
        )

        search.send_keys(
            "Gaming"
        )

        self.driver.find_element(
            By.CSS_SELECTOR,
            ".search-action-btn.primary"
        ).click()

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Gaming Build",
            body.text
        )

    def test_build_search_price_filter_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse("build_search")
        )

        min_price = self.driver.find_element(
            By.CSS_SELECTOR,
            "input[name='min_price'][type='number']"
        )

        min_price.send_keys("150000")

        self.driver.find_element(
            By.CLASS_NAME,
            "search-action-btn"
        ).click()

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Workstation Build",
            body.text
        )

        self.assertNotIn(
            "Gaming Build",
            body.text
        )

    def test_build_search_sort_price_descending_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse("build_search")
        )

        sort_button = self.driver.find_element(
            By.CLASS_NAME,
            "sort-btn"
        )

        sort_button.click()

        time.sleep(1)

        sort = self.driver.find_element(
            By.CSS_SELECTOR,
            "input[value='price_desc']"
        )

        sort.click()

        time.sleep(1)

        results = self.driver.find_elements(
            By.CLASS_NAME,
            "item-name"
        )

        self.assertIn(
            "Workstation Build",
            results[0].text
        )

    def test_build_search_sort_most_liked_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse("build_search")
        )

        sort_button = self.driver.find_element(
            By.CLASS_NAME,
            "sort-btn"
        )

        sort_button.click()

        time.sleep(1)

        sort = self.driver.find_element(
            By.CSS_SELECTOR,
            "input[value='most_liked']"
        )

        sort.click()

        time.sleep(1)

        results = self.driver.find_elements(
            By.CLASS_NAME,
            "item-name"
        )

        self.assertIn(
            "Workstation Build",
            results[0].text
        )

    # ---------------- BUILD DETAIL ----------------

    def test_build_detail_page_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[self.build.id]
            )
        )

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Gaming Build",
            body.text
        )

        self.assertIn(
            "A powerful gaming build",
            body.text
        )

    def test_build_detail_components_shown_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[self.build.id]
            )
        )

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "AMD Ryzen 5 5600",
            body.text
        )

        self.assertIn(
            "MSI B550",
            body.text
        )

        self.assertIn(
            "Corsair Vengeance 16GB",
            body.text
        )

    def test_build_detail_likes_dislikes_shown_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[self.build.id]
            )
        )

        like_count = self.driver.find_element(
            By.ID,
            "likeCount"
        )

        dislike_count = self.driver.find_element(
            By.ID,
            "dislikeCount"
        )

        self.assertEqual(
            like_count.text,
            "0"
        )

        self.assertEqual(
            dislike_count.text,
            "0"
        )

    # ---------------- RATE BUILD ----------------

    def test_build_detail_like_button_exists_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[self.build.id]
            )
        )

        like_btn = self.driver.find_element(
            By.ID,
            "likeBtn"
        )

        self.assertTrue(
            like_btn.is_displayed()
        )

    def test_build_detail_dislike_button_exists_ui(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[self.build.id]
            )
        )

        dislike_btn = self.driver.find_element(
            By.ID,
            "dislikeBtn"
        )

        self.assertTrue(
            dislike_btn.is_displayed()
        )

    def test_build_detail_user_can_like_build_ui(self):

        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[self.build.id]
            )
        )

        time.sleep(1)


        like_count_element = self.driver.find_element(
            By.ID,
            "likeCount"
        )

        initial_like_count = int(like_count_element.text)

        like_btn = self.driver.find_element(
            By.ID,
            "likeBtn"
        )

        like_btn.click()

        time.sleep(1)

        like_count_element = self.driver.find_element(
            By.ID,
            "likeCount"
        )

        self.assertEqual(
            int(like_count_element.text),
            initial_like_count + 1
        )

    # ---------------- EDIT BUILD ----------------

    def test_build_detail_owner_can_edit_build_ui(self):

        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[self.build.id]
            )
        )

        original_name = self.driver.find_element(
            By.ID,
            "buildTitle"
        ).text

        edit_btn = self.driver.find_element(
            By.ID,
            "editBtn"
        )

        edit_btn.click()

        time.sleep(1)

        name_input = self.driver.find_element(
            By.ID,
            "editTitle"
        )

        self.assertIsNotNone(
            name_input
        )

        self.assertEqual(
            name_input.get_attribute("value"),
            original_name
        )

    def test_build_detail_owner_can_delete_build_ui(self):

        self.login_ui()

        build_id = self.build.id

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[build_id]
            )
        )

        delete_btn = self.driver.find_element(
            By.ID,
            "deleteBtn"
        )

        delete_btn.click()

        time.sleep(1)

        confirm_delete_btn = self.driver.find_element(
            By.CSS_SELECTOR,
            ".delete-confirmation .delete-btn"
        )

        confirm_delete_btn.click()

        time.sleep(1)

        self.assertIn(
            "/builds",
            self.driver.current_url
        )

    def test_build_detail_edit_button_not_shown_to_non_owner(self):

        self.driver.get(
            self.live_server_url +
            reverse(
                "build_detail",
                args=[self.build.id]
            )
        )

        edit_btns = self.driver.find_elements(
            By.ID,
            "editBtn"
        )

        self.assertEqual(
            len(edit_btns),
            0
        )

    # ---------------- PUBLISH BUILD ----------------

    def test_publish_build_page_ui_opens(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.motherboard.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.ram.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        publish_btn = self.driver.find_element(
            By.CLASS_NAME,
            "publish-btn"
        )

        publish_btn.click()

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Objavi svoj gotov računar",
            body.text
        )

    def test_publish_build_requires_login_ui(self):
        self.driver.get(
            self.live_server_url +
            reverse("publish_build_page")
        )

        time.sleep(1)

        self.assertIn(
            "/login",
            self.driver.current_url
        )

    def test_publish_build_missing_components_shows_error_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        publish_btn = self.driver.find_element(
            By.CLASS_NAME,
            "publish-btn"
        )

        publish_btn.click()

        time.sleep(1)

        name_input = self.driver.find_element(
            By.ID,
            "name"
        )

        name_input.send_keys("Ultimate Gaming Build")

        description_input = self.driver.find_element(
            By.ID,
            "description"
        )

        description_input.send_keys("A great gaming build for 2026 with excellent performance")

        submit_btn = self.driver.find_element(
            By.ID,
            "publishBtn"
        )

        submit_btn.click()

        time.sleep(1)

        error_container = self.driver.find_element(
            By.CLASS_NAME,
            "error-container"
        )

        self.assertIn(
            "Morate izabrati sledeće komponente",
            error_container.text
        )

    def test_publish_build_missing_name_shows_error_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.motherboard.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.ram.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        publish_btn = self.driver.find_element(
            By.CLASS_NAME,
            "publish-btn"
        )

        publish_btn.click()

        time.sleep(1)

        description_input = self.driver.find_element(
            By.ID,
            "description"
        )

        description_input.send_keys("A great gaming build")

        time.sleep(1)

        submit_btn = self.driver.find_element(
            By.ID,
            "publishBtn"
        )

        submit_btn.click()

        time.sleep(1)


        self.assertIn( # posto nije moguce required popup proveriti samo pogledaj da li je i dalje na istoj stranici
            reverse("publish_build_page"),
            self.driver.current_url
        )

    def test_publish_build_missing_description_shows_error_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.motherboard.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.ram.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        publish_btn = self.driver.find_element(
            By.CLASS_NAME,
            "publish-btn"
        )

        publish_btn.click()

        time.sleep(1)

        name_input = self.driver.find_element(
            By.ID,
            "name"
        )

        name_input.send_keys("Ultimate Gaming Build")

        time.sleep(1)

        submit_btn = self.driver.find_element(
            By.ID,
            "publishBtn"
        )

        submit_btn.click()

        time.sleep(1)

        self.assertIn(  # isto
            reverse("publish_build_page"),
            self.driver.current_url
        )

    def test_publish_build_missing_images_shows_error_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.motherboard.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.ram.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        publish_btn = self.driver.find_element(
            By.CLASS_NAME,
            "publish-btn"
        )

        publish_btn.click()

        time.sleep(1)

        name_input = self.driver.find_element(
            By.ID,
            "name"
        )

        name_input.send_keys("Ultimate Gaming Build")

        description_input = self.driver.find_element(
            By.ID,
            "description"
        )

        description_input.send_keys("A great gaming build for 2026")

        time.sleep(1)

        submit_btn = self.driver.find_element(
            By.ID,
            "publishBtn"
        )

        submit_btn.click()

        time.sleep(1)

        body = self.driver.find_element(
            By.TAG_NAME,
            "body"
        )

        self.assertIn(
            "Potrebno je dodati barem jednu sliku",
            body.text
        )

    def test_publish_build_success_ui(self):
        self.login_ui()

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.cpu.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.motherboard.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse(
                "component_detail",
                args=[self.ram.id]
            )
        )

        self.driver.find_element(
            By.CLASS_NAME,
            "add-btn"
        ).click()

        time.sleep(1)

        self.driver.get(
            self.live_server_url +
            reverse("configurator")
        )

        publish_btn = self.driver.find_element(
            By.CLASS_NAME,
            "publish-btn"
        )

        publish_btn.click()

        time.sleep(1)

        name_input = self.driver.find_element(
            By.ID,
            "name"
        )

        name_input.send_keys("Ultimate Gaming Build")

        description_input = self.driver.find_element(
            By.ID,
            "description"
        )

        description_input.send_keys("A great gaming build for 2026 with excellent performance")

        time.sleep(1)

        image_input = self.driver.find_element(
            By.ID,
            "imageInput"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            test_image_path = os.path.join(temp_dir, "test_image.png")
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='red')
            img.save(test_image_path)

            image_input.send_keys(test_image_path)

            time.sleep(2)

            add_benchmark_btn = self.driver.find_element(
                By.ID,
                "addBenchmarkBtn"
            )

            add_benchmark_btn.click()

            time.sleep(1)

            benchmark_name_inputs = self.driver.find_elements(
                By.NAME,
                "benchmark_name[]"
            )

            benchmark_value_inputs = self.driver.find_elements(
                By.NAME,
                "benchmark_value[]"
            )

            if benchmark_name_inputs:
                benchmark_name_inputs[-1].send_keys("Cinebench R23")

            if benchmark_value_inputs:
                benchmark_value_inputs[-1].send_keys("12450 points")

            time.sleep(1)

            submit_btn = self.driver.find_element(
                By.ID,
                "publishBtn"
            )

            submit_btn.click()

            time.sleep(2)

            self.assertIn(
                reverse("build_search"),
                self.driver.current_url
            )


    def test_ui_successful_registration_flow(self):
        self.driver.get(self.live_server_url + reverse("register"))

        self.driver.find_element(By.NAME, "username").send_keys("novikorisnikui")
        self.driver.find_element(By.NAME, "email").send_keys("noviui@testing.com")
        self.driver.find_element(By.NAME, "password1").send_keys("Lozinka123!")
        self.driver.find_element(By.NAME, "password2").send_keys("Lozinka123!")

        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1)

        self.assertNotIn("/register", self.driver.current_url)

    def test_ui_login_wrong_username_shows_error(self):
        self.driver.get(self.live_server_url + reverse("login"))

        self.driver.find_element(By.NAME, "username").send_keys("nepostojeci_korisnik_123")
        self.driver.find_element(By.NAME, "password").send_keys("NekaLozinka123!")
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()

        time.sleep(1.5)

        grecke = self.driver.find_elements(By.CLASS_NAME, "errorlist")
        self.assertTrue(len(grecke) > 0, "Selenium nije pronašao 'errorlist' klasu za greške na formi.")

    def test_ui_login_wrong_password_shows_error(self):
        self.driver.get(self.live_server_url + reverse("login"))

        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("PogresnaLozinka999!")
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()

        time.sleep(1.5)

        grecke = self.driver.find_elements(By.CLASS_NAME, "errorlist")
        self.assertTrue(len(grecke) > 0, "Selenium nije pronašao 'errorlist' klasu za greške na formi.")

    # ---------- Registracija: dodatni neuspešni scenariji ----------

    def test_ui_registration_password_mismatch_shows_error(self):
        self.driver.get(self.live_server_url + reverse("register"))
        self.driver.find_element(By.NAME, "username").send_keys("mismatchuser")
        self.driver.find_element(By.NAME, "email").send_keys("mismatch@testing.com")
        self.driver.find_element(By.NAME, "password1").send_keys("Lozinka123!")
        self.driver.find_element(By.NAME, "password2").send_keys("DrugacijaLozinka123!")
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1.5)

        self.assertIn("/register", self.driver.current_url)
        greske = self.driver.find_elements(By.CLASS_NAME, "errorlist")
        self.assertTrue(len(greske) > 0, "Selenium nije pronašao grešku za nepoklapanje šifara.")

    def test_ui_registration_duplicate_username_shows_error(self):
        self.driver.get(self.live_server_url + reverse("register"))
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "email").send_keys("drugimejl@testing.com")
        self.driver.find_element(By.NAME, "password1").send_keys("Lozinka123!")
        self.driver.find_element(By.NAME, "password2").send_keys("Lozinka123!")
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1.5)

        self.assertIn("/register", self.driver.current_url)
        greske = self.driver.find_elements(By.CLASS_NAME, "errorlist")
        self.assertTrue(len(greske) > 0, "Selenium nije pronašao grešku za zauzeto korisničko ime.")

    def test_ui_registration_duplicate_email_shows_error(self):
        self.driver.get(self.live_server_url + reverse("register"))
        self.driver.find_element(By.NAME, "username").send_keys("nekidrugikorisnik")
        self.driver.find_element(By.NAME, "email").send_keys("tester@testing.com")
        self.driver.find_element(By.NAME, "password1").send_keys("Lozinka123!")
        self.driver.find_element(By.NAME, "password2").send_keys("Lozinka123!")
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1.5)

        self.assertIn("/register", self.driver.current_url)
        greske = self.driver.find_elements(By.CLASS_NAME, "errorlist")
        self.assertTrue(len(greske) > 0, "Selenium nije pronašao grešku za zauzetu email adresu.")

    def test_ui_registration_weak_password_shows_error(self):
        self.driver.get(self.live_server_url + reverse("register"))
        self.driver.find_element(By.NAME, "username").send_keys("slabalozinkauser")
        self.driver.find_element(By.NAME, "email").send_keys("slabalozinka@testing.com")
        self.driver.find_element(By.NAME, "password1").send_keys("samomalaslova")
        self.driver.find_element(By.NAME, "password2").send_keys("samomalaslova")
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1.5)

        self.assertIn("/register", self.driver.current_url)
        greske = self.driver.find_elements(By.CLASS_NAME, "errorlist")
        self.assertTrue(len(greske) > 0, "Selenium nije pronašao grešku za slabu šifru.")

    def test_ui_registration_empty_fields_blocks_submit(self):
        self.driver.get(self.live_server_url + reverse("register"))
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1)

        self.assertIn("/register", self.driver.current_url)

    # ---------- Prijava: dodatni scenariji ----------

    def test_ui_login_successful_redirects(self):
        self.driver.get(self.live_server_url + reverse("login"))
        self.driver.find_element(By.NAME, "username").send_keys("tester@testing.com")
        self.driver.find_element(By.NAME, "password").send_keys("DovoljnoDugacakPass123!")
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1.5)

        self.assertNotIn("/login", self.driver.current_url)

    def test_ui_login_empty_fields_blocks_submit(self):
        self.driver.get(self.live_server_url + reverse("login"))
        self.driver.find_element(By.CLASS_NAME, "submit-btn").click()
        time.sleep(1)

        self.assertIn("/login", self.driver.current_url)

    def test_ui_profile_display_data(self):
        self.login_ui()
        self.driver.get(self.live_server_url + reverse("profile"))

        username_display = self.driver.find_element(By.ID, "displayUsername").text
        self.assertIn("testuser", username_display)

    # ---------- Chatbot Interakcija UI ----------

    def test_ui_chatbot_recommend_flow(self):
        self.login_ui()
        self.driver.get(self.live_server_url + reverse("configurator"))

        chat_input = self.driver.find_element(By.ID, "chat-input")
        chat_input.send_keys("Preporuči mi procesor do 200e")

        send_btn = self.driver.find_element(By.ID, "chat-send-btn")
        send_btn.click()

        time.sleep(2)
        chat_history = self.driver.find_element(By.ID, "chat-history").text

        self.assertIn("Preporuči mi procesor do 200e", chat_history)

    def test_ui_chatbot_full_build_flow(self):
        self.login_ui()
        self.driver.get(self.live_server_url + reverse("configurator"))

        chat_input = self.driver.find_element(By.ID, "chat-input")
        chat_input.send_keys("Sklopi mi konfiguraciju za gaming do 1000e")

        self.driver.find_element(By.ID, "chat-send-btn").click()
        time.sleep(2)

        chat_history = self.driver.find_element(By.ID, "chat-history").text
        self.assertIn("Sklopi mi konfiguraciju za gaming do 1000e", chat_history)

    def test_ui_chatbot_bad_prompt_shows_error(self):
        self.login_ui()
        self.driver.get(self.live_server_url + reverse("configurator"))

        chat_input = self.driver.find_element(By.ID, "chat-input")
        chat_input.send_keys("")
        self.driver.find_element(By.ID, "chat-send-btn").click()

        time.sleep(1)
        chat_history = self.driver.find_element(By.ID, "chat-history").text
        self.assertIn("Zdravo!", chat_history)
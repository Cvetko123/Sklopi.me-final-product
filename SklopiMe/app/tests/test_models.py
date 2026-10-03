"""
Comprehensive unit tests for Sklopi.me models (app/models.py).

Run with:
    python manage.py test app
"""

import os
import shutil
import tempfile
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings

# Upload path used by Buildimage.image (must match models.py upload_to=).
BUILD_IMAGES_UPLOAD_DIR = 'app/static/build_images'

from ..models import (
    Benchmark,
    UserProfile,
    Build,
    Buildcomponent,
    Buildimage,
    Buildlikedislike,
    Component,
    Case,
    Componentprice,
    Cpu,
    Cpucooler,
    Gpu,
    Motherboard,
    Powersupply,
    Ram,
    Storage,
)


class BaseTestSetupMixin:
    """
    Shared setUp logic: creates a Django User, a UserProfile, a base
    Component, and a Build so individual test classes don't repeat
    this boilerplate.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', email='test@example.com'
        )
        self.profile = UserProfile.objects.create(user=self.user)

        self.component = Component.objects.create(
            name='Generic Component',
            description='A generic test component',
            imagepath='images/generic.png',
            powerconsumption=50,
            manufacturer='TestManufacturer',
        )

        self.build = Build.objects.create(
            name='My Test Build',
            description='A build used for testing',
            totalprice=150000,
            numoflikes=0,
            numofdislikes=0,
            iduser=self.profile,
        )


class UserProfileModelTest(BaseTestSetupMixin, TestCase):
    """Tests for UserProfile (OneToOne extension of Django's User)."""

    def test_userprofile_creation_and_retrieval(self):
        """UserProfile should save and link correctly to a User."""
        profile = UserProfile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.user.username, 'testuser')

    def test_userprofile_str_method(self):
        """__str__ should return the underlying user's username."""
        self.assertEqual(str(self.profile), 'testuser')

    def test_userprofile_user_can_be_null(self):
        """user field allows null, per model definition."""
        profile = UserProfile.objects.create(user=None)
        self.assertIsNone(profile.user)

    def test_userprofile_onetoone_uniqueness(self):
        """A User should only be able to have one UserProfile (OneToOne)."""
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserProfile.objects.create(user=self.user)

    def test_userprofile_cascade_delete_with_user(self):
        """Deleting the related User should cascade-delete the UserProfile."""
        profile_pk = self.profile.pk
        self.user.delete()
        self.assertFalse(UserProfile.objects.filter(pk=profile_pk).exists())


class BuildModelTest(BaseTestSetupMixin, TestCase):
    """Tests for the Build model."""

    def test_build_creation_and_retrieval(self):
        """Build should save all provided field values correctly."""
        build = Build.objects.get(pk=self.build.pk)
        self.assertEqual(build.name, 'My Test Build')
        self.assertEqual(build.description, 'A build used for testing')
        self.assertEqual(build.totalprice, 150000)
        self.assertEqual(build.numoflikes, 0)
        self.assertEqual(build.numofdislikes, 0)
        self.assertEqual(build.iduser, self.profile)

    def test_build_str_method(self):
        """__str__ should return the build's name."""
        self.assertEqual(str(self.build), 'My Test Build')

    def test_build_default_name(self):
        """name field should default to 'My build' when not specified."""
        build = Build.objects.create(
            totalprice=100,
            numoflikes=0,
            numofdislikes=0,
            iduser=self.profile,
        )
        self.assertEqual(build.name, 'My build')

    def test_build_description_can_be_blank_or_null(self):
        """description is optional (blank=True, null=True)."""
        build = Build.objects.create(
            totalprice=999,
            numoflikes=1,
            numofdislikes=1,
            iduser=self.profile,
        )
        self.assertIsNone(build.description)

    def test_build_cascade_delete_with_userprofile(self):
        """Deleting the owning UserProfile should cascade-delete the Build."""
        build_pk = self.build.pk
        self.profile.delete()
        self.assertFalse(Build.objects.filter(pk=build_pk).exists())


class BenchmarkModelTest(BaseTestSetupMixin, TestCase):
    """Tests for the Benchmark model."""

    def test_benchmark_creation_and_retrieval(self):
        """Benchmark should save and retrieve exact name/value/build link."""
        benchmark = Benchmark.objects.create(
            name='FPS Cyberpunk 2077',
            value='144',
            idbuild=self.build,
        )
        retrieved = Benchmark.objects.get(pk=benchmark.pk)
        self.assertEqual(retrieved.name, 'FPS Cyberpunk 2077')
        self.assertEqual(retrieved.value, '144')
        self.assertEqual(retrieved.idbuild, self.build)

    def test_benchmark_related_name_on_build(self):
        """Build.benchmarks related_name should return linked Benchmarks."""
        Benchmark.objects.create(name='Cinebench', value='2500', idbuild=self.build)
        Benchmark.objects.create(name='3DMark', value='9800', idbuild=self.build)
        self.assertEqual(self.build.benchmarks.count(), 2)

    def test_benchmark_cascade_delete_with_build(self):
        """Deleting a Build should cascade-delete its Benchmarks."""
        benchmark = Benchmark.objects.create(name='FPS', value='60', idbuild=self.build)
        benchmark_pk = benchmark.pk
        self.build.delete()
        self.assertFalse(Benchmark.objects.filter(pk=benchmark_pk).exists())


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(prefix='sklopime_test_media_'))
class BuildimageModelTest(BaseTestSetupMixin, TestCase):
    """
    Tests for the Buildimage model.

    IMPORTANT: these tests never write into the project's real
    'static/build_images' folder. MEDIA_ROOT is overridden to a
    temporary directory for the whole test class (see
    @override_settings above), so Django resolves uploads to
    <temp_dir>/app/static/build_images instead of touching anything
    under the actual project tree. The temp directory is removed
    entirely in tearDownClass.
    """

    UPLOAD_DIR = 'app/static/build_images'

    @classmethod
    def tearDownClass(cls):
        from django.conf import settings
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def _make_image_file(self, filename, content=b'file_content'):
        """Helper to build a SimpleUploadedFile for image tests."""
        return SimpleUploadedFile(filename, content, content_type='image/jpeg')

    def _create_buildimage(self, filename, idbuild=None, content=b'file_content'):
        """Create a Buildimage with a real uploaded file (written to the temp MEDIA_ROOT)."""
        image_file = self._make_image_file(filename, content)
        return Buildimage.objects.create(idbuild=idbuild or self.build, image=image_file)

    def _assert_uploaded_under_build_images_dir(self, image_field):
        """Assert the saved image's relative path starts with the expected upload dir."""
        self.assertTrue(
            image_field.name.startswith(f'{self.UPLOAD_DIR}/'),
            msg=f"Expected image path to start with '{self.UPLOAD_DIR}/', "
                f"got '{image_field.name}'",
        )

    def test_buildimage_creation_and_retrieval(self):
        """Buildimage should save the uploaded image and its Build link."""
        buildimage = self._create_buildimage('test_image.jpg')
        retrieved = Buildimage.objects.get(pk=buildimage.pk)
        self.assertEqual(retrieved.idbuild, self.build)
        self.assertIn('test_image', retrieved.image.name)

    def test_buildimage_uploads_to_build_images_directory(self):
        """
        Buildimage.image should resolve to app/static/build_images
        (relative to MEDIA_ROOT), matching the model's upload_to setting.
        """
        buildimage = self._create_buildimage('upload_dir_check.jpg')
        retrieved = Buildimage.objects.get(pk=buildimage.pk)
        self._assert_uploaded_under_build_images_dir(retrieved.image)
        # The file should actually exist on disk at that computed path
        # (inside the temporary MEDIA_ROOT, not the real project folder).
        self.assertTrue(retrieved.image.storage.exists(retrieved.image.name))

    def test_buildimage_related_name_on_build(self):
        """Build.images related_name should return linked Buildimages."""
        buildimage = self._create_buildimage('another.jpg')
        self.assertEqual(self.build.images.count(), 1)
        self._assert_uploaded_under_build_images_dir(buildimage.image)

    def test_buildimage_cascade_delete_with_build(self):
        """Deleting a Build should cascade-delete its Buildimages."""
        buildimage = self._create_buildimage('del.jpg')
        buildimage_pk = buildimage.pk
        self.build.delete()
        self.assertFalse(Buildimage.objects.filter(pk=buildimage_pk).exists())

    def test_buildimage_multiple_uploads_all_use_build_images_directory(self):
        """
        Multiple Buildimage uploads for the same build should all resolve
        under app/static/build_images, even if filenames collide.
        """
        first = self._create_buildimage('shared_name.jpg')
        second = self._create_buildimage('shared_name.jpg')
        self._assert_uploaded_under_build_images_dir(first.image)
        self._assert_uploaded_under_build_images_dir(second.image)
        # Django should have de-duplicated the filenames within the dir.
        self.assertNotEqual(first.image.name, second.image.name)


class BuildlikedislikeModelTest(BaseTestSetupMixin, TestCase):
    """Tests for the Buildlikedislike model."""

    def test_buildlikedislike_creation_and_retrieval(self):
        """Buildlikedislike should save like value plus user/build links."""
        vote = Buildlikedislike.objects.create(
            like=1, iduser=self.profile, idbuild=self.build
        )
        retrieved = Buildlikedislike.objects.get(pk=vote.pk)
        self.assertEqual(retrieved.like, 1)
        self.assertEqual(retrieved.iduser, self.profile)
        self.assertEqual(retrieved.idbuild, self.build)

    def test_buildlikedislike_cascade_delete_with_build(self):
        """Deleting a Build should cascade-delete related votes."""
        vote = Buildlikedislike.objects.create(
            like=-1, iduser=self.profile, idbuild=self.build
        )
        vote_pk = vote.pk
        self.build.delete()
        self.assertFalse(Buildlikedislike.objects.filter(pk=vote_pk).exists())

    def test_buildlikedislike_cascade_delete_with_userprofile(self):
        """Deleting a UserProfile should cascade-delete related votes."""
        vote = Buildlikedislike.objects.create(
            like=1, iduser=self.profile, idbuild=self.build
        )
        vote_pk = vote.pk
        self.profile.delete()
        self.assertFalse(Buildlikedislike.objects.filter(pk=vote_pk).exists())


class ComponentModelTest(BaseTestSetupMixin, TestCase):
    """Tests for the base Component model, including unique constraint."""

    def test_component_creation_and_retrieval(self):
        """Component should save and retrieve exact field values."""
        component = Component.objects.get(pk=self.component.pk)
        self.assertEqual(component.name, 'Generic Component')
        self.assertEqual(component.description, 'A generic test component')
        self.assertEqual(component.imagepath, 'images/generic.png')
        self.assertEqual(component.powerconsumption, 50)
        self.assertEqual(component.manufacturer, 'TestManufacturer')

    def test_component_str_method(self):
        """__str__ should return the component's name."""
        self.assertEqual(str(self.component), 'Generic Component')

    def test_component_name_unique_constraint_validation_error(self):
        """
        full_clean() should raise ValidationError when 'name' duplicates
        an existing Component's name (unique=True enforced at validation level).
        """
        duplicate = Component(
            name='Generic Component',
            description='Different description',
            imagepath='images/dup.png',
            powerconsumption=75,
            manufacturer='OtherManufacturer',
        )
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_component_name_unique_constraint_integrity_error(self):
        """
        Saving a Component with a duplicate 'name' directly (bypassing
        full_clean) should raise an IntegrityError at the database level.
        """
        duplicate = Component(
            name='Generic Component',
            description='Different description',
            imagepath='images/dup.png',
            powerconsumption=75,
            manufacturer='OtherManufacturer',
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                duplicate.save()


class ComponentpriceModelTest(BaseTestSetupMixin, TestCase):
    """Tests for the Componentprice model."""

    def test_componentprice_creation_and_retrieval(self):
        """Componentprice should save shop name, link, price, and component link."""
        price = Componentprice.objects.create(
            shopname='TechShop',
            link='https://techshop.example.com/product/1',
            price=29999,
            idcomponent=self.component,
        )
        retrieved = Componentprice.objects.get(pk=price.pk)
        self.assertEqual(retrieved.shopname, 'TechShop')
        self.assertEqual(retrieved.link, 'https://techshop.example.com/product/1')
        self.assertEqual(retrieved.price, 29999)
        self.assertEqual(retrieved.idcomponent, self.component)

    def test_componentprice_cascade_delete_with_component(self):
        """Deleting a Component should cascade-delete its Componentprices."""
        price = Componentprice.objects.create(
            shopname='TechShop', link='https://x.example.com', price=100,
            idcomponent=self.component,
        )
        price_pk = price.pk
        self.component.delete()
        self.assertFalse(Componentprice.objects.filter(pk=price_pk).exists())


class BuildcomponentModelTest(BaseTestSetupMixin, TestCase):
    """Tests for the Buildcomponent (Build <-> Component) join model."""

    def test_buildcomponent_creation_and_retrieval(self):
        """Buildcomponent should correctly link a Build and a Component."""
        link = Buildcomponent.objects.create(
            idcomponent=self.component, idbuild=self.build
        )
        retrieved = Buildcomponent.objects.get(pk=link.pk)
        self.assertEqual(retrieved.idcomponent, self.component)
        self.assertEqual(retrieved.idbuild, self.build)

    def test_buildcomponent_allows_multiple_components_per_build(self):
        """A Build should be able to have several linked Components."""
        second_component = Component.objects.create(
            name='Second Component',
            description='Another component',
            imagepath='images/second.png',
            powerconsumption=20,
            manufacturer='OtherManufacturer',
        )
        Buildcomponent.objects.create(idcomponent=self.component, idbuild=self.build)
        Buildcomponent.objects.create(idcomponent=second_component, idbuild=self.build)
        self.assertEqual(
            Buildcomponent.objects.filter(idbuild=self.build).count(), 2
        )

    def test_buildcomponent_cascade_delete_with_build(self):
        """Deleting a Build should cascade-delete its Buildcomponent links."""
        link = Buildcomponent.objects.create(
            idcomponent=self.component, idbuild=self.build
        )
        link_pk = link.pk
        self.build.delete()
        self.assertFalse(Buildcomponent.objects.filter(pk=link_pk).exists())

    def test_buildcomponent_cascade_delete_with_component(self):
        """Deleting a Component should cascade-delete its Buildcomponent links."""
        link = Buildcomponent.objects.create(
            idcomponent=self.component, idbuild=self.build
        )
        link_pk = link.pk
        self.component.delete()
        self.assertFalse(Buildcomponent.objects.filter(pk=link_pk).exists())


class CaseModelTest(BaseTestSetupMixin, TestCase):
    """Tests for Case (multi-table inheritance from Component)."""

    def test_case_creation_and_retrieval(self):
        """Case should save both Component (parent) and Case (child) fields."""
        case = Case.objects.create(
            name='Sleek Tower',
            description='A sleek mid-tower case',
            imagepath='images/case.png',
            powerconsumption=0,
            manufacturer='CaseMaker',
            color='Black',
            dimensions='450x210x450mm',
            supportedmotherboards='ATX,mATX,ITX',
        )
        retrieved = Case.objects.get(pk=case.pk)
        # Parent (Component) fields
        self.assertEqual(retrieved.name, 'Sleek Tower')
        self.assertEqual(retrieved.manufacturer, 'CaseMaker')
        # Child (Case) fields
        self.assertEqual(retrieved.color, 'Black')
        self.assertEqual(retrieved.dimensions, '450x210x450mm')
        self.assertEqual(retrieved.supportedmotherboards, 'ATX,mATX,ITX')

    def test_case_component_ptr_links_to_component_table(self):
        """
        Case should be accessible through the base Component table via
        multi-table inheritance (component_ptr), and str() should use
        Component's __str__.
        """
        case = Case.objects.create(
            name='Ptr Test Case',
            description='desc',
            imagepath='images/case2.png',
            powerconsumption=0,
            manufacturer='CaseMaker',
            color='White',
            dimensions='400x200x400mm',
            supportedmotherboards='ATX',
        )
        component_row = Component.objects.get(pk=case.pk)
        self.assertEqual(component_row.name, 'Ptr Test Case')
        self.assertEqual(str(case), 'Ptr Test Case')
        self.assertIsInstance(case.component_ptr, Component)

    def test_case_inherits_component_unique_name_constraint(self):
        """Case name field should still enforce Component's unique constraint."""
        Case.objects.create(
            name='Unique Case', description='d', imagepath='p', powerconsumption=0,
            manufacturer='m', color='Black', dimensions='d', supportedmotherboards='ATX',
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Case.objects.create(
                    name='Unique Case', description='d2', imagepath='p2',
                    powerconsumption=0, manufacturer='m2', color='White',
                    dimensions='d2', supportedmotherboards='mATX',
                )


class CpuModelTest(BaseTestSetupMixin, TestCase):
    """Tests for Cpu (multi-table inheritance from Component)."""

    def test_cpu_creation_and_retrieval(self):
        """Cpu should save both parent and child fields correctly."""
        cpu = Cpu.objects.create(
            name='TestCPU 9000',
            description='A fast test CPU',
            imagepath='images/cpu.png',
            powerconsumption=125,
            manufacturer='CPUMaker',
            corecount=8,
            threadcount=16,
            clockspeed=Decimal('4.50'),
            socket='AM5',
            integratedgpu=1,
        )
        retrieved = Cpu.objects.get(pk=cpu.pk)
        self.assertEqual(retrieved.name, 'TestCPU 9000')
        self.assertEqual(retrieved.corecount, 8)
        self.assertEqual(retrieved.threadcount, 16)
        self.assertEqual(retrieved.clockspeed, Decimal('4.50'))
        self.assertEqual(retrieved.socket, 'AM5')
        self.assertEqual(retrieved.integratedgpu, 1)

    def test_cpu_component_ptr_links_to_component_table(self):
        """Cpu should be reachable as a Component row via component_ptr."""
        cpu = Cpu.objects.create(
            name='Ptr Test CPU', description='d', imagepath='p', powerconsumption=65,
            manufacturer='m', corecount=4, threadcount=8, clockspeed=Decimal('3.60'),
            socket='AM4', integratedgpu=0,
        )
        component_row = Component.objects.get(pk=cpu.pk)
        self.assertEqual(component_row.name, 'Ptr Test CPU')
        self.assertEqual(str(cpu), 'Ptr Test CPU')

    def test_cpu_cascade_delete_from_parent_component(self):
        """Deleting the parent Component row should delete the Cpu row too."""
        cpu = Cpu.objects.create(
            name='Delete Test CPU', description='d', imagepath='p', powerconsumption=65,
            manufacturer='m', corecount=4, threadcount=8, clockspeed=Decimal('3.60'),
            socket='AM4', integratedgpu=0,
        )
        cpu_pk = cpu.pk
        Component.objects.get(pk=cpu_pk).delete()
        self.assertFalse(Cpu.objects.filter(pk=cpu_pk).exists())


class CpucoolerModelTest(BaseTestSetupMixin, TestCase):
    """Tests for Cpucooler (multi-table inheritance from Component)."""

    def test_cpucooler_creation_and_retrieval(self):
        """Cpucooler should save both parent and child fields correctly."""
        cooler = Cpucooler.objects.create(
            name='ChillMax 240',
            description='AIO liquid cooler',
            imagepath='images/cooler.png',
            powerconsumption=10,
            manufacturer='CoolerMaker',
            coolertype='AIO',
            socket='AM5,LGA1700',
        )
        retrieved = Cpucooler.objects.get(pk=cooler.pk)
        self.assertEqual(retrieved.name, 'ChillMax 240')
        self.assertEqual(retrieved.coolertype, 'AIO')
        self.assertEqual(retrieved.socket, 'AM5,LGA1700')

    def test_cpucooler_component_ptr_links_to_component_table(self):
        """Cpucooler should be reachable as a Component row via component_ptr."""
        cooler = Cpucooler.objects.create(
            name='Ptr Test Cooler', description='d', imagepath='p', powerconsumption=5,
            manufacturer='m', coolertype='Air', socket='AM4',
        )
        component_row = Component.objects.get(pk=cooler.pk)
        self.assertEqual(component_row.manufacturer, 'm')
        self.assertEqual(str(cooler), 'Ptr Test Cooler')


class GpuModelTest(BaseTestSetupMixin, TestCase):
    """Tests for Gpu (multi-table inheritance from Component)."""

    def test_gpu_creation_and_retrieval(self):
        """Gpu should save both parent and child fields correctly."""
        gpu = Gpu.objects.create(
            name='TestGPU RTX X090',
            description='A powerful test GPU',
            imagepath='images/gpu.png',
            powerconsumption=350,
            manufacturer='GPUMaker',
            chip='TX090',
            memcapacity='24GB',
            color='Black',
        )
        retrieved = Gpu.objects.get(pk=gpu.pk)
        self.assertEqual(retrieved.chip, 'TX090')
        self.assertEqual(retrieved.memcapacity, '24GB')
        self.assertEqual(retrieved.color, 'Black')
        self.assertEqual(retrieved.powerconsumption, 350)

    def test_gpu_component_ptr_links_to_component_table(self):
        """Gpu should be reachable as a Component row via component_ptr."""
        gpu = Gpu.objects.create(
            name='Ptr Test GPU', description='d', imagepath='p', powerconsumption=200,
            manufacturer='m', chip='chipX', memcapacity='8GB', color='White',
        )
        component_row = Component.objects.get(pk=gpu.pk)
        self.assertEqual(component_row.name, 'Ptr Test GPU')
        self.assertEqual(str(gpu), 'Ptr Test GPU')


class MotherboardModelTest(BaseTestSetupMixin, TestCase):
    """Tests for Motherboard (multi-table inheritance from Component)."""

    def test_motherboard_creation_and_retrieval(self):
        """Motherboard should save both parent and child fields correctly."""
        mobo = Motherboard.objects.create(
            name='TestBoard Z900',
            description='A feature-rich motherboard',
            imagepath='images/mobo.png',
            powerconsumption=15,
            manufacturer='MoboMaker',
            socket='AM5',
            formfactor='ATX',
            ramslots=4,
            ramtype='DDR5',
            color='Black',
            wifichip='WiFi6E',
        )
        retrieved = Motherboard.objects.get(pk=mobo.pk)
        self.assertEqual(retrieved.socket, 'AM5')
        self.assertEqual(retrieved.formfactor, 'ATX')
        self.assertEqual(retrieved.ramslots, 4)
        self.assertEqual(retrieved.ramtype, 'DDR5')
        self.assertEqual(retrieved.color, 'Black')
        self.assertEqual(retrieved.wifichip, 'WiFi6E')

    def test_motherboard_component_ptr_links_to_component_table(self):
        """Motherboard should be reachable as a Component row via component_ptr."""
        mobo = Motherboard.objects.create(
            name='Ptr Test Mobo', description='d', imagepath='p', powerconsumption=15,
            manufacturer='m', socket='AM4', formfactor='mATX', ramslots=2,
            ramtype='DDR4', color='White', wifichip='None',
        )
        component_row = Component.objects.get(pk=mobo.pk)
        self.assertEqual(component_row.name, 'Ptr Test Mobo')
        self.assertEqual(str(mobo), 'Ptr Test Mobo')


class PowersupplyModelTest(BaseTestSetupMixin, TestCase):
    """Tests for Powersupply (multi-table inheritance from Component)."""

    def test_powersupply_creation_and_retrieval(self):
        """Powersupply should save both parent and child fields correctly."""
        psu = Powersupply.objects.create(
            name='TestPSU 850W',
            description='An efficient PSU',
            imagepath='images/psu.png',
            powerconsumption=0,
            manufacturer='PSUMaker',
            formfactor='ATX',
            efficiency='80+ Gold',
            wattage=850,
        )
        retrieved = Powersupply.objects.get(pk=psu.pk)
        self.assertEqual(retrieved.formfactor, 'ATX')
        self.assertEqual(retrieved.efficiency, '80+ Gold')
        self.assertEqual(retrieved.wattage, 850)

    def test_powersupply_component_ptr_links_to_component_table(self):
        """Powersupply should be reachable as a Component row via component_ptr."""
        psu = Powersupply.objects.create(
            name='Ptr Test PSU', description='d', imagepath='p', powerconsumption=0,
            manufacturer='m', formfactor='SFX', efficiency='80+ Bronze', wattage=550,
        )
        component_row = Component.objects.get(pk=psu.pk)
        self.assertEqual(component_row.name, 'Ptr Test PSU')
        self.assertEqual(str(psu), 'Ptr Test PSU')


class RamModelTest(BaseTestSetupMixin, TestCase):
    """Tests for Ram (multi-table inheritance from Component)."""

    def test_ram_creation_and_retrieval(self):
        """Ram should save both parent and child fields correctly."""
        ram = Ram.objects.create(
            name='TestRAM Kit',
            description='High speed RAM kit',
            imagepath='images/ram.png',
            powerconsumption=5,
            manufacturer='RAMMaker',
            type='DDR5',
            speed=6000,
            memcapacity='32GB',
            modulenum=2,
            color='Black',
        )
        retrieved = Ram.objects.get(pk=ram.pk)
        self.assertEqual(retrieved.type, 'DDR5')
        self.assertEqual(retrieved.speed, 6000)
        self.assertEqual(retrieved.memcapacity, '32GB')
        self.assertEqual(retrieved.modulenum, 2)
        self.assertEqual(retrieved.color, 'Black')

    def test_ram_component_ptr_links_to_component_table(self):
        """Ram should be reachable as a Component row via component_ptr."""
        ram = Ram.objects.create(
            name='Ptr Test RAM', description='d', imagepath='p', powerconsumption=5,
            manufacturer='m', type='DDR4', speed=3200, memcapacity='16GB',
            modulenum=2, color='White',
        )
        component_row = Component.objects.get(pk=ram.pk)
        self.assertEqual(component_row.name, 'Ptr Test RAM')
        self.assertEqual(str(ram), 'Ptr Test RAM')


class StorageModelTest(BaseTestSetupMixin, TestCase):
    """Tests for Storage (multi-table inheritance from Component)."""

    def test_storage_creation_and_retrieval(self):
        """Storage should save both parent and child fields correctly."""
        storage = Storage.objects.create(
            name='TestSSD 2TB',
            description='Fast NVMe SSD',
            imagepath='images/storage.png',
            powerconsumption=7,
            manufacturer='StorageMaker',
            type='SSD',
            slot='M.2',
            capacity='2TB',
        )
        retrieved = Storage.objects.get(pk=storage.pk)
        self.assertEqual(retrieved.type, 'SSD')
        self.assertEqual(retrieved.slot, 'M.2')
        self.assertEqual(retrieved.capacity, '2TB')

    def test_storage_component_ptr_links_to_component_table(self):
        """Storage should be reachable as a Component row via component_ptr."""
        storage = Storage.objects.create(
            name='Ptr Test Storage', description='d', imagepath='p', powerconsumption=7,
            manufacturer='m', type='HDD', slot='SATA', capacity='1TB',
        )
        component_row = Component.objects.get(pk=storage.pk)
        self.assertEqual(component_row.name, 'Ptr Test Storage')
        self.assertEqual(str(storage), 'Ptr Test Storage')


class MultiTableInheritanceCrossModelTest(BaseTestSetupMixin, TestCase):
    """
    Extra cross-cutting checks that different Component subclasses
    don't collide and each queries independently via Component.
    """

    def test_polymorphic_components_are_distinct_rows(self):
        """
        Different Component subclasses should all appear in the base
        Component table, while each subclass table only contains its
        own rows.
        """
        cpu = Cpu.objects.create(
            name='Distinct CPU', description='d', imagepath='p', powerconsumption=65,
            manufacturer='m', corecount=6, threadcount=12, clockspeed=Decimal('3.80'),
            socket='AM4', integratedgpu=0,
        )
        gpu = Gpu.objects.create(
            name='Distinct GPU', description='d', imagepath='p', powerconsumption=220,
            manufacturer='m', chip='chipY', memcapacity='12GB', color='Black',
        )
        # Both appear in base Component table (plus the one from setUp).
        self.assertEqual(Component.objects.count(), 3)
        # Each subclass table has exactly one row.
        self.assertEqual(Cpu.objects.count(), 1)
        self.assertEqual(Gpu.objects.count(), 1)
        self.assertNotEqual(cpu.pk, gpu.pk)
from .test_base import TestInstitutionBase
from general.models import Institution
from common.utilities import make_add_link, make_edit_link, make_changelist_link


class TestInstitutionAdminViewPage(TestInstitutionBase):
    def setUp(self):
        self.institution_obj = self.create_institution()
        self.user = self.create_fake_user()

    def test_institution_add_admin_view_without_login(self):
        url = make_add_link(Institution)
        resp = self.client.get(url)
        self.assertEqual(302, resp.status_code)

    def test_institution_add_admin_view_with_login(self):
        ret = self.client.force_login(self.user)
        url = make_add_link(Institution)
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)

    def test_institution_change_admin_view_with_login(self):
        ret = self.client.force_login(self.user)
        url = make_edit_link(self.institution_obj)
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)

    def test_institution_list_admin_view(self):
        ret = self.client.force_login(self.user)
        url = make_changelist_link(Institution)
        # url = "/admin/general/institution/"
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)

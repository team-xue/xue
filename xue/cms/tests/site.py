# -*- coding: utf-8 -*-
from __future__ import with_statement
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from cms.models import Page
from cms.test.testcases import CMSTestCase
from cms.test.util.context_managers import SettingsOverride

class SiteTestCase(CMSTestCase):
    """Site framework specific test cases.
    
    All stuff which is changing settings.SITE_ID for tests should come here.
    """
    def setUp(self):
        with SettingsOverride(SITE_ID=1):
            
            u = User(username="test", is_staff = True, is_active = True, is_superuser = True)
            u.set_password("test")
            u.save()
            
            # setup sites
            Site(domain="sample2.com", name="sample2.com").save() # pk 2
            Site(domain="sample3.com", name="sample3.com").save() # pk 3
            
            self.login_user(u)
    
    
    def test_01_site_framework(self):
        #Test the site framework, and test if it's possible to disable it
        with SettingsOverride(SITE_ID=2):
            page_2a = self.create_page(site=2)
    
            response = self.client.get("/admin/cms/page/?site__exact=3")
            self.assertEqual(response.status_code, 200)
            page_3b = self.create_page(site=3)
            
        with SettingsOverride(SITE_ID=3):
            page_3a = self.create_page(site=3)
            
            # with param
            self.assertEqual(Page.objects.on_site(2).count(), 1)
            self.assertEqual(Page.objects.on_site(3).count(), 2)
            
            self.assertEqual(Page.objects.drafts().on_site().count(), 2)
            
        with SettingsOverride(SITE_ID=2):
            # without param
            self.assertEqual(Page.objects.drafts().on_site().count(), 1)

        

# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django import forms
from django.db import transaction

# from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupForm, EditProfileForm

from xue.accounts.models import DMUserProfile
from xue.common.choices import ETHNIC_CHOICES, GENDER_CHOICES, POLITICAL_BKGND_CHOICES
from xue.classes.models import LogicalClass
from xue.infocenter.models import CentralStudentInfo

from xue.prepopulate.querier import querier

MAX_IDENT_LENGTH = 20


class SignupFormExtra(SignupForm):
    nickname = forms.CharField(label=u'昵称', required=False, max_length=32,
            help_text=u'所有人都可以看见；这个可以不填，以后也能修改'
            )
    sign_line = forms.CharField(label=u'个性签名', required=False, max_length=32,
            help_text=u'同上'
            )
    id_number = forms.RegexField(label=u'学号/工号',
            regex=ur'^(?:\d{7}|\d{10})$',
            max_length=MAX_IDENT_LENGTH,  # in line w/ profile model
            error_messages={'invalid': u'学号或者工号的格式不正确。'},
            help_text=u'抱歉不对非学院人员开放注册',
            )

    def __init__(self, *args, **kw):
        super(SignupFormExtra, self).__init__(*args, **kw)
        # all the zh_CN l10n work has been done (by me), so remove some of the
        # overriding.
        f = self.fields
        f['username'].help_text = u'不论是否登录都可见，请不要用姓名、学号、身份证号之类的敏感信息作为 ID'
        f['username'].label = u'ID'
        f['password1'].help_text = u'可以使用任何字符，为了安全，最好不要使用纯数字或者 8 位以下的弱密码'

    def clean_id_number(self):
        num = self.cleaned_data['id_number'].strip()[:MAX_IDENT_LENGTH]
        if not querier.have(num):
            raise forms.ValidationError(u'输入的学号或者工号不被认可。')

        # duplication check
        try:
            DMUserProfile.objects.get(id_number=num)
            raise forms.ValidationError(u'输入的学号或者工号已注册帐号。')
        except DMUserProfile.DoesNotExist:
            pass

        return num

    def clean_username(self):
        super(SignupFormExtra, self).clean_username()
        if len(self.cleaned_data['username']) < 2:
            raise forms.ValidationError(u'用户名至少为 2 个字符。')
        if self.cleaned_data['username'].startswith(u'.'):
            raise forms.ValidationError(u'用户名非法。')
        return self.cleaned_data['username']

    def save(self):
        """
        Override the save method to lookup the identification number first.

        """

        with transaction.commit_on_success():
            # First save the parent form and get the user.
            new_user = super(SignupFormExtra, self).save()

            # get prepopulated things
            id_num = self.cleaned_data['id_number']
            prep_data = querier.lookup(id_num)
            is_student = False

            # fill in the data
            new_profile = new_user.profile
            new_profile.id_number = id_num
            new_profile.realname = prep_data[u'name']
            if prep_data[u'role'] == u'S':
                new_profile.role = 0  # student
                is_student = True
            elif prep_data[u'role'] == u'T':
                new_profile.role = 1  # teacher

            new_profile.nickname = self.cleaned_data['nickname']
            new_profile.sign_line = self.cleaned_data['sign_line']
            # new_profile.gender = self.cleaned_data['gender']

            # feed form data
            if is_student:
                new_info = CentralStudentInfo()
                new_info.user = new_user
                new_info.phone = prep_data[u'phone']
                # new_info.ethnic = self.cleaned_data['ethnic']
                # new_info.location = self.cleaned_data['location']
                # new_info.political = self.cleaned_data['political']

                # init klass relationship
                # go ahead w/ class association
                # separate out major code, recruit year and seq
                # XXX DUPLICATE CODE IN DATA MIGRATION, SEEK TO REFACTOR!!
                # UPDATE: the format CHANGED in 2012... dammit, have to
                # implement a generic logic in querier to work around...
                yr, major_code, cls_seq = querier.extract_org(id_num)

                klass = LogicalClass.objects.filter(
                        date__year=yr,
                        major__code=major_code,
                        seq=cls_seq,
                        )

                if len(klass) != 0:
                    new_info.klass = klass[0]

                # save centralized info
                new_info.save()

            new_profile.save()
            new_user.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user


class LimitedEditProfileForm(EditProfileForm):
    class Meta:
        model = EditProfileForm.Meta.model
        exclude = EditProfileForm.Meta.exclude
        exclude += [
                'first_name',
                'last_name',
                'role',
                'realname',
                'id_number',
                ]


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:

# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

import re

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x

# TODO: extract this into common module!
DEPUNCTUATIONER = re.compile(r'''[\s,.;:'"()\[\]，。；：“”‘’《》、·「」…！？?]+''')


class MaterialEntry(models.Model):
    class Meta:
        verbose_name = _('材料条目')
        verbose_name_plural = _('材料条目')

    user = models.ForeignKey(User,
            verbose_name=_u('user'),
            )
    title = models.CharField(_('材料标题'), max_length=256)
    content = models.TextField(_('内容'))

    ctime = models.DateTimeField(_('创建日期'), auto_now_add=True)
    mtime = models.DateTimeField(_('修改日期'), auto_now=True)

    is_locked = models.BooleanField(_('已锁定'), default=False)

    def __unicode__(self):
        return '%(realname)s (%(username)s) 的材料: %(title)s [%(length)d 字]' % {
                'realname': self.user.profile.realname,
                'username': self.user.username,
                'title': self.title,
                'length': self.get_length(),
                }

    def get_realname(self):
        return self.user.profile.realname
    get_realname.short_description = _('真实姓名')

    def get_username(self):
        return self.user.username
    get_username.short_description = _('用户名')

    def get_length(self):
        effective_content = DEPUNCTUATIONER.sub('', self.content)
        return len(effective_content)
    get_length.short_description = _('字数')

    def get_paragraphs(self):
        lines = self.content.splitlines()

        paras, tmp = [], []
        for ln in lines:
            ln_stripped = ln.rstrip()
            if len(ln_stripped) == 0:
                # New paragraph detected
                paras.append(tmp)
                tmp = []
                continue
            tmp.append(ln_stripped)

        # don't chew off the last paragraph
        if len(tmp) > 0:
            paras.append(tmp)

        return paras


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:

# -*- coding: utf-8 -*-

from django.conf import settings
import re

from django.core.exceptions import ObjectDoesNotExist

APPEND_TO_SLUG = "-copy"
COPY_SLUG_REGEX = re.compile(r'^.*-copy(?:-(\d)*)?$')

TAGS_REMOVER = re.compile(ur'</?.*?/?\s*>')
PUNCTUATION_CHOPPER = re.compile(ur'(.*?[，。；：,.;: 　“”\r\n\t\v])')
WHITESPACE_SHRINKER = re.compile(ur'[ 　\r\n\t\v]+')
TARGET_CHAR_LIMIT = 80
ELLIPSIS_FORMAT = u'%s ...'


def is_valid_page_slug(page, parent, lang, slug, site):
    """Validates given slug depending on settings.
    """
    from cms.models import Title
    qs = Title.objects.filter(page__site=site, slug=slug).exclude(page=page).exclude(page=page.publisher_public)
    
    if settings.i18n_installed:
        qs = qs.filter(language=lang)
    
    if not settings.CMS_FLAT_URLS:
        if parent and not parent.is_home(): 
            qs = qs.filter(page__parent=parent)
        else:
            qs = qs.filter(page__parent__isnull=True)

    if page.pk:
        qs = qs.exclude(language=lang, page=page)
    if qs.count():
        return False
    return True


def get_available_slug(title, new_slug=None):
    """Smart function generates slug for title if current title slug cannot be
    used. Appends APPEND_TO_SLUG to slug and checks it again.
    
    (Used in page copy function)
    
    Returns: slug
    """
    slug = new_slug or title.slug
    if is_valid_page_slug(title.page, title.page.parent, title.language, slug, title.page.site):
        return slug
    
    # add nice copy attribute, first is -copy, then -copy-2, -copy-3, .... 
    match = COPY_SLUG_REGEX.match(slug)
    if match:
        try:
            next = int(match.groups()[0]) + 1
            slug = "-".join(slug.split('-')[:-1]) + "-%d" % next
        except TypeError:
            slug = slug + "-2"
         
    else:
        slug = slug + APPEND_TO_SLUG
    return get_available_slug(title, slug)


def check_title_slugs(page):
    """Checks page title slugs for duplicity if required, used after page move/
    cut/paste.
    """
    for title in page.title_set.all():
        old_slug = title.slug
        title.slug = get_available_slug(title)
        if title.slug != old_slug:
            title.save()


def _excerpt_preprocess(txt):
    tmp = TAGS_REMOVER.sub(u'', txt)
    tmp = tmp.replace(u'&ldquo;', u'“')
    tmp = tmp.replace(u'&rdquo;', u'”')
    tmp = tmp.replace(u'&nbsp;', u' ')
    tmp = tmp.replace(u'\n', u' ')
    return tmp


def get_text_excerpt(txt):
    # chop text on a punctuation boundary.
    txt = _excerpt_preprocess(txt).strip()
    if not txt:
        return u''

    frags = (frag.groups()[0] for frag in PUNCTUATION_CHOPPER.finditer(txt))
    if not frags:
        # Fallback to the traditional and not-so-beautiful way of chopping...
        if len(txt) <= TARGET_CHAR_LIMIT:
            return txt
        return ELLIPSIS_FORMAT % txt[:TARGET_CHAR_LIMIT]

    # The least number of fragments needed to reach at least
    # TARGET_CHAR_LIMIT chars...
    taken_frags, curr_len = [], 0
    for frag in frags:
        # By using genexprs, only needed frags are realized in memory twice,
        # reducing memory footprint (hopefully, maybe i'm wrong on this).
        if curr_len >= TARGET_CHAR_LIMIT:
            break
        taken_frags.append(frag)
        curr_len += len(frag)

    shrunk_frags = WHITESPACE_SHRINKER.split(u''.join(taken_frags))

    return ELLIPSIS_FORMAT % (u' '.join(shrunk_frags).strip())


def get_text_content(page):
    # attr['excerpt'] = u'blah blah blah blah test test 123'
    # extracting excerpt...
    # XXX EXPENSIVE OPERATION!!!
    # TODO: Move this code to Page manipulation
    content_list = []
    for placeholder in page.placeholders.all():
        if u'text' in placeholder.slot.lower():
            # considered a Text placeholder
            # XXX This code is NOT going to be versatile!!!!
            for plugin in placeholder.get_plugins():
                try:
                    if plugin.plugin_type == u'TextPlugin':
                        content_list.append(plugin.text.body)
                except ObjectDoesNotExist:
                    pass

    return u'\n'.join(content_list)


# vim:ai:et:ts=4:sw=4:sts=4:ff=unix:fenc=utf-8:

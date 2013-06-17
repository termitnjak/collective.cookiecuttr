from collective.cookiecuttr.interfaces import ICookieCuttrSettings
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.analytics.view import AnalyticsViewlet
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

import logging
import re

logger = logging.getLogger('collective.cookiecuttr')


class CookieCuttrViewlet(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(CookieCuttrViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.settings = getUtility(IRegistry).forInterface(
                                                        ICookieCuttrSettings)

    def update(self):
        pass

    def available(self):
        return self.settings and self.settings.cookiecuttr_enabled

    def text(self):
        """Return text to display in the pop-up window (language aware)"""
        portal_url = getToolByName(self, 'portal_url')
        portal = portal_url.getPortalObject()
        path = self.settings.text_page_path

        if not path:
            return u''

        try:
            path = path.encode('utf-8')
            page_en = portal.restrictedTraverse(path)
        except (KeyError, AttributeError):
            logger.exception('Path to the page that contains text is not '
                             'valid.')
            return u''

        lang = portal.portal_languages.getPreferredLanguage()
        page = page_en.getTranslation(lang)
        if page:
            text = page.getText()
        else:
            text = page_en.getText()
        # remove newlines and tabs
        text = re.sub(r"\s+", " ", text.decode('utf-8'))
        return text

    def render(self):
        if self.available():
            text = self.text() or self.settings.text
            snippet = safe_unicode(js_template % (self.settings.link,
                                                  text,
                                                  self.settings.accept_button))
            return snippet
        return ""


class CookieCuttrAwareAnalyticsViewlet(AnalyticsViewlet):

    def render(self):
        settings = getUtility(IRegistry).forInterface(ICookieCuttrSettings)

        available = settings and settings.cookiecuttr_enabled

        # Render if CookieCuttr is enabled and Cookies were accepted
        if available and \
            self.request.cookies.get('cc_cookie_accept', None) == \
                'cc_cookie_accept':
            return super(CookieCuttrAwareAnalyticsViewlet, self).render()

        return ""

js_template = """
<script type="text/javascript">

    (function($) {
        $(document).ready(function () {
            if($.cookieCuttr) {
                $.cookieCuttr({cookieAnalytics: false,
                               cookiePolicyLink: "%s",
                               cookieMessage: "%s",
                               cookieAcceptButtonText: "%s"
                               });
                }
        })
    })(jQuery);
</script>

"""

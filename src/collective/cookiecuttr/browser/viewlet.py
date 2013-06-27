from collective.cookiecuttr.interfaces import _
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.analytics.view import AnalyticsViewlet
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
        properties = getToolByName(self.context, 'portal_properties')
        self.settings = properties.cookiecuttr_properties

    def update(self):
        pass

    def available(self):
        return self.settings and self.settings.getProperty(
            'cookiecuttr_enabled', False)

    def text(self):
        """Return text to display in the pop-up window (language aware)"""
        portal_url = getToolByName(self, 'portal_url')
        portal = portal_url.getPortalObject()
        path = self.settings.getProperty('text_page_path', None)

        if not path:
            return u''
        try:
            path = path.encode('utf-8')
            page_en = portal.restrictedTraverse(path.strip('/'))
        except (KeyError, AttributeError):
            logger.exception('Path to the page that contains text is not '
                             'valid.')
            return u''

        lang = portal.portal_languages.getPreferredLanguage()
        text = page_en.getText()

        try:
            page = page_en.getTranslation(lang)
            if page:
                text = page.getText()
        except AttributeError:
            # LinguaPlone not installed
            pass

        # remove newlines and tabs
        text = re.sub(r"\s+", " ", text.decode('utf-8'))
        return text

    def render(self):
        if self.available():
            text = self.text()
            accept_button = self.settings.getProperty(
                'accept_button', 'Accept cookies')
            show_decline_button = self.settings.getProperty(
                'show_decline_button', None)
            show_decline_button = show_decline_button and 'true' or 'false'
            decline_button = self.settings.getProperty(
                'decline_button', 'Decline cookies')
	    popup_position_bottom =  self.settings.getProperty(
		'popup_position_bottom', None)
	    popup_position_bottom = popup_position_bottom and 'true' or 'false'
	    snippet = safe_unicode(
                js_template % (
                    text,
                    self.context.translate(_(accept_button)),
                    self.context.translate(_(decline_button)),
                    show_decline_button,
		    popup_position_bottom
                )
            )
            return snippet
        return ""


class CookieCuttrAwareAnalyticsViewlet(AnalyticsViewlet):

    def render(self):
        properties = getToolByName(self.context, 'portal_properties')
        settings = properties.cookiecuttr_properties
        available = settings and settings.getProperty(
            'cookiecuttr_enabled', False)

        # Render if CookieCuttr is enabled and Cookies were accepted
        if available and \
            self.request.cookies.get('cc_cookie_accept', None) == \
                'cc_cookie_accept':
            return super(CookieCuttrAwareAnalyticsViewlet, self).render()

        return ""

js_template = """
<script type="text/javascript">

    (function(jQuery) {
        jQuery(document).ready(function () {
            if(jQuery.cookieCuttr) {
                jQuery.cookieCuttr({cookieAnalytics: false,
                               cookieMessage: '%s',
                               cookieAcceptButtonText: '%s',
                               cookieDeclineButtonText: '%s',
                               cookieDeclineButton: %s,
			       cookieNotificationLocationBottom: %s
			});
                }
        })
    })(jQuery);
</script>

"""

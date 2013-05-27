from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.cookiecuttr')


class ICookieCuttr(Interface):
    """This interface is registered in profiles/default/browserlayer.xml,
    and is referenced in the 'layer' option of various browser resources.
    When the product is installed, this marker interface will be applied
    to every request, allowing layer-specific customisation.
    """


class ICookieCuttrSettings(Interface):
    """Global CookieCuttr settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    cookiecuttr_enabled = schema.Bool(title=_(u"Enable CookieCuttr"),
                                  description=_(u"help_cookiecuttr_enable",
                                  default=u"Toggle this to enable"
                                                " loading of the CookieCuttr"
                                                " plugin."),
                                  required=False,
                                  default=False,)

    text = schema.TextLine(title=_(u"Text to show your visitor"),
                                       description=_(u"", default=u""),
                                       required=False,
                                       default=u"We use cookies."
                                       " <a href='{{cookiePolicyLink}}' "
                                       "title='read about our cookies'>"
                                       "Read everything</a>")

    text_page_path = schema.TextLine(
        title=_(u"Path to the page that contains the text"),
        description=_(
            u"help_text_page_path",
            default=u"Instead of entering the text directly in the previous "
            "field, you can enter path to the page that contains the text "
            "to show to your visitor (e.g. 'cookie-policy/message'). This "
            "is useful if you want the text to be language aware - "
            "translated version of the page will be used, if available. "
            "Note that this field takes precedence before the manual text "
            "input."),
        required=False
    )

    link = schema.TextLine(title=_(u"Link to page"),
                                 required=False,)

    accept_button = schema.TextLine(title=_(u"Text to show in"
                                             " the Accept button"),
                                    description=_(u"", default=u""),
                                    required=False,
                                    default=_(u"Accept cookies"))

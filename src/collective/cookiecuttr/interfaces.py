from zope.interface import Interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.cookiecuttr')


class ICookieCuttr(Interface):
    """This interface is registered in profiles/default/browserlayer.xml,
    and is referenced in the 'layer' option of various browser resources.
    When the product is installed, this marker interface will be applied
    to every request, allowing layer-specific customisation.
    """

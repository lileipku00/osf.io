import datetime as dt

from django.utils import timezone
from modularodm import Q

from framework.auth import Auth

from website.util import permissions
from osf.models import MetaSchema

from tests.base import OsfTestCase
from osf_tests.factories import AuthUserFactory, ProjectFactory, DraftRegistrationFactory

class RegistrationsTestBase(OsfTestCase):
    def setUp(self):
        super(RegistrationsTestBase, self).setUp()

        self.user = AuthUserFactory()
        self.auth = Auth(self.user)
        self.node = ProjectFactory(creator=self.user)
        self.non_admin = AuthUserFactory()
        self.node.add_contributor(
            self.non_admin,
            permissions.DEFAULT_CONTRIBUTOR_PERMISSIONS,
            auth=self.auth,
            save=True
        )
        self.non_contrib = AuthUserFactory()

        self.meta_schema = MetaSchema.find_one(
            Q('name', 'eq', 'Open-Ended Registration') &
            Q('schema_version', 'eq', 2)
        )
        self.draft = DraftRegistrationFactory(
            initiator=self.user,
            branched_from=self.node,
            registration_schema=self.meta_schema,
            registration_metadata={
                'summary': {'value': 'Some airy'}
            }
        )

        current_month = timezone.now().strftime("%B")
        current_year = timezone.now().strftime("%Y")

        valid_date = timezone.now() + dt.timedelta(days=180)
        self.embargo_payload = {
            u'embargoEndDate': unicode(valid_date.strftime('%a, %d, %B %Y %H:%M:%S')) + u' GMT',
            u'registrationChoice': 'embargo'
        }
        self.invalid_embargo_date_payload = {
            u'embargoEndDate': u"Thu, 01 {month} {year} 05:00:00 GMT".format(
                month=current_month,
                year=str(int(current_year) - 1)
            ),
            u'registrationChoice': 'embargo'
        }
        self.immediate_payload = {
            'registrationChoice': 'immediate'
        }
        self.invalid_payload = {
            'registrationChoice': 'foobar'
        }

    def draft_url(self, view_name):
        return self.node.web_url_for(view_name, draft_id=self.draft._id)

    def draft_api_url(self, view_name):
        return self.node.api_url_for(view_name, draft_id=self.draft._id)

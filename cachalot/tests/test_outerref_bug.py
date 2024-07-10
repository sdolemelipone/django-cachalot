from django.db.models import Subquery, OuterRef
from django.test import TransactionTestCase

from cachalot.tests.models import Test

from .tests_decorators import no_final_sql_check

def check_nested_outerref():
    test_instance = Test(name="foo")

    subquery2 = Test.objects.filter(id=OuterRef(OuterRef(OuterRef("id"))))

    subquery1 = Test.objects.annotate(
        public_from_subquery2=Subquery(subquery2.values("public")[:1])
    )

    Test.objects.annotate(
        public_from_subquery1=Subquery(subquery1.values("public_from_subquery2")[:1])
    ).get(pk=test_instance.pk)

@no_final_sql_check
class TestOuterRefx3NoFinalSQL(TransactionTestCase):
    databases = ["default"]

    def test_nested_outerref(self):
        check_nested_outerref()


class TestOuterRefx3WithFinalSQL(TransactionTestCase):
    databases = ["default"]

    def test_nested_outerref(self):
        check_nested_outerref()


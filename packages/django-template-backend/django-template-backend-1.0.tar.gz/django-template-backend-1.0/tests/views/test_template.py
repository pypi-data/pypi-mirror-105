import pytest
from assertpy import assert_that
from pytest_common_subject import precondition_fixture
from pytest_drf import (Returns200, Returns201, Returns204, UsesDeleteMethod, UsesDetailEndpoint, UsesGetMethod,
                        UsesListEndpoint, UsesPostMethod, UsesPutMethod, ViewSetTest)
from pytest_drf.util import pluralized, url_for
from pytest_lambda import lambda_fixture, static_fixture

from template.models import Template


def model_to_json(t: Template):
    return {
        'id': str(t.id),
        'date_created': t.date_created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'date_updated': t.date_updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'value': t.value,
    }


models_to_json = pluralized(model_to_json)


@pytest.mark.django_db
class TestTemplateViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for('template-lc'))
    detail_url = lambda_fixture(lambda template: url_for('template-rud', template.pk))

    class TestList(UsesGetMethod, UsesListEndpoint, Returns200):
        templates = lambda_fixture(lambda: [
            Template.objects.create(value=v) for v in ['list1', 'list2', 'list3']
        ], autouse=True)

        def test_list_api(self, templates, results):
            actual_response = results
            expected_response = models_to_json(sorted(templates, key=lambda t: t.date_created, reverse=True))
            assert_that(actual_response).is_equal_to(expected_response)

    class TestCreate(UsesPostMethod, UsesListEndpoint, Returns201):
        initial_template_ids = precondition_fixture(lambda: set(Template.objects.values_list('id', flat=True)))
        data = static_fixture({'value': 'create'})

        def test_create_db(self, initial_template_ids, json, data):
            actual_length = Template.objects.count()
            expected_length = len(initial_template_ids) + 1
            assert_that(expected_length).is_equal_to(actual_length)
            actual_data = model_to_json(Template.objects.get(pk=json['id']))
            expected_data = data
            assert_that(expected_data).is_subset_of(actual_data)

        def test_create_api(self, data, json):
            expected_response = model_to_json(Template.objects.get(pk=json['id']))
            actual_response = json
            assert_that(actual_response).is_equal_to(expected_response)

    class TestRetrieve(UsesGetMethod, UsesDetailEndpoint, Returns200):
        template = lambda_fixture(lambda: Template.objects.create(value='retrieve'))

        def test_retrieve_api(self, template, json):
            actual_response = json
            expected_response = model_to_json(template)
            assert_that(actual_response).is_equal_to(expected_response)

    class TestUpdate(UsesPutMethod, UsesDetailEndpoint, Returns200):
        template = lambda_fixture(lambda: Template.objects.create(value='update'))
        data = static_fixture({'value': 'update'})

        def test_update_db(self, data, template):
            template.refresh_from_db()
            actual_data = model_to_json(template)
            expected_data = data
            assert_that(expected_data).is_subset_of(actual_data)

        def test_update_api(self, template, json):
            template.refresh_from_db()
            actual_response = json
            expected_response = model_to_json(template)
            assert_that(actual_response).is_equal_to(expected_response)

    class TestDestroy(UsesDeleteMethod, UsesDetailEndpoint, Returns204):
        template = lambda_fixture(lambda: Template.objects.create(value='destroy'))
        initial_template_ids = precondition_fixture(lambda: set(Template.objects.values_list('id')))

        def test_destroy_db(self, initial_template_ids, template):
            actual_data = set(Template.objects.values_list('id', flat=True))
            expected_data = initial_template_ids - {template.id}
            assert_that(actual_data).is_equal_to(expected_data)

from mlflow.store.tracking.rest_store import RestStore
from mlflow.utils.rest_utils import MlflowHostCreds
from infinstor_mlflow_plugin.tokenfile import get_token
from os.path import expanduser
from os.path import sep as separator
from mlflow.entities import (
        ViewType
        )
import requests
from requests.exceptions import HTTPError
import json
from mlflow.entities.model_registry.model_version_stages import (
    get_canonical_stage,
    DEFAULT_STAGES_FOR_GET_LATEST_VERSIONS,
    STAGE_DELETED_INTERNAL,
    STAGE_ARCHIVED,
)
from mlflow.entities.model_registry.registered_model import RegisteredModel
from mlflow.store.entities.paged_list import PagedList

class CognitoModelVersion():
    def __init__(self, name, user_id, version, creation_timestamp, last_updated_timestamp,
            current_stage, source, run_id, status):
        self.name = name
        self.user_id = user_id
        self.version = version
        self.creation_timestamp = creation_timestamp
        self.last_updated_timestamp = last_updated_timestamp
        self.current_stage = current_stage
        self.source = source
        self.run_id = status

class CognitoAuthenticatedRestStore(RestStore):
    def cognito_host_creds(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return MlflowHostCreds('https://mlflow.' + service + ':443/', token=token)

    def get_service(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return service

    def get_token_string(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return token

    def get_headers(self):
        headers = {'Content-Type': 'application/x-amz-json-1.1'}
        if (self.get_token_string().startswith('Custom')):
            headers['Authorization'] = self.get_token_string()
        else:
            headers['Authorization'] = 'Bearer ' + self.get_token_string()
        return headers

    def _hard_delete_run(self, run_id):
        """
        Permanently delete a run (metadata and metrics, tags, parameters).
        This is used by the ``mlflow gc`` command line and is not intended to be used elsewhere.
        """
        print('_hard_delete_run: Entered. run_id=' + str(run_id))
        headers = self.get_headers()
        url = 'https://mlflow.' + self.get_service() + '/api/2.0/mlflow/runs/hard-delete'

        body = dict()
        body['run_id'] = run_id

        try:
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        else:
            return

    def _get_deleted_runs(self):
        print('_get_deleted_runs: Entered')
        experiments = self.list_experiments(view_type=ViewType.ALL)
        experiment_ids = map(lambda x: x.experiment_id, experiments)
        print('_get_deleted_runs: experiment_ids=' + str(experiment_ids))
        deleted_runs = self.search_runs(
            experiment_ids=experiment_ids, filter_string="", run_view_type=ViewType.DELETED_ONLY
        )
        rv = [deleted_run.info.run_uuid for deleted_run in deleted_runs]
        print('_get_deleted_runs: deleted_runs=' + str(rv))
        return rv

    def get_latest_versions(self, name, stages=None):
        """
        Latest version models for each requested stage. If no ``stages`` argument is provided,
        returns the latest version for each stage.

        :param name: Registered model name.
        :param stages: List of desired stages. If input list is None, return latest versions for
                       for 'Staging' and 'Production' stages.
        :return: List of :py:class:`mlflow.entities.model_registry.ModelVersion` objects.
        """
        #print('get_latest_versions: Entered. name=' + str(name) + ', stages=' + str(stages),
        #        flush=True)
        headers = self.get_headers()
        url = 'https://mlflow.' + self.get_service() + '/api/2.0/mlflow/registered-models/get'

        try:
            response = requests.get(url, params={'name':name}, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        respjson = json.loads(response.text)
        model = respjson['registered_model']
        staging = None
        production = None
        archived = None
        for lv in model['latest_versions']:
            if (lv['current_stage'] == 'Staging'):
                if (not staging):
                    staging = lv
                elif (int(lv['version']) > int(staging['version'])):
                    staging = lv
            elif (lv['current_stage'] == 'Production'):
                if (not production):
                    production = lv
                elif (int(lv['version']) > int(production['version'])):
                    production = lv
            elif (lv['current_stage'] == 'Archived'):
                if (not archived):
                    archived = lv
                elif (int(lv['version']) > int(archived['version'])):
                    archived = lv

        latest_versions = []
        if (staging):
            latest_versions.append(CognitoModelVersion(staging['name'],
                staging['user_id'], staging['version'], staging['creation_timestamp'],
                staging['last_updated_timestamp'], staging['current_stage'],
                staging['source'], staging['run_id'], staging['status']))
        if (production):
            latest_versions.append(CognitoModelVersion(production['name'],
                production['user_id'], production['version'], production['creation_timestamp'],
                production['last_updated_timestamp'], production['current_stage'],
                production['source'], production['run_id'], production['status']))
        if (archived):
            latest_versions.append(CognitoModelVersion(archived['name'],
                archived['user_id'], archived['version'], archived['creation_timestamp'],
                archived['last_updated_timestamp'], archived['current_stage'],
                archived['source'], archived['run_id'], archived['status']))

        if stages is None or len(stages) == 0 or stages[0] == '':
            expected_stages = set(
                [get_canonical_stage(stage) for stage in DEFAULT_STAGES_FOR_GET_LATEST_VERSIONS]
            )
        else:
            expected_stages = set([get_canonical_stage(stage) for stage in stages])
        return [mv for mv in latest_versions if mv.current_stage in expected_stages]

    def get_model_version_download_uri(self, name, version):
        #print('get_model_version_download_uri: Entered. name=' + str(name)
        #        + ', version=' + str(version), flush=True)
        headers = self.get_headers()
        url = 'https://mlflow.' + self.get_service() + '/api/2.0/mlflow/model-versions/get'

        try:
            response = requests.get(url, params={'name':name, 'version':version}, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        respjson = json.loads(response.text)
        model_version = respjson['model_version']
        return model_version['source']

    def create_registered_model(self, name, tags=None, description=None):
        """
        Create a new registered model in backend store.

        :param name: Name of the new model. This is expected to be unique in the backend store.
        :param tags: A list of :py:class:`mlflow.entities.model_registry.RegisteredModelTag`
                     instances associated with this registered model.
        :param description: Description of the model.
        :return: A single object of :py:class:`mlflow.entities.model_registry.RegisteredModel`
                 created in the backend.
        """
        headers = self.get_headers()
        url = 'https://mlflow.' + self.get_service() + '/api/2.0/mlflow/registered-models/create'

        body = dict()
        body['name'] = name
        body['description'] = description

        try:
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        regmod = response.json()['registered_model']
        ct = None
        dscr = None
        lu = None
        if ('creation_timestamp' in regmod):
            ct = regmod['creation_timestamp']
        if ('description' in regmod):
            dscr = regmod['description']
        if ('last_updated_timestamp' in regmod):
            lu = regmod['last_updated_timestamp']
        return RegisteredModel(regmod['name'], creation_timestamp=ct,
                last_updated_timestamp=lu, description=dscr,
                latest_versions=None, tags=None)

    def update_registered_model(self, name, description):
        """
        Update description of the registered model.

        :param name: Registered model name.
        :param description: New description.
        :return: A single updated :py:class:`mlflow.entities.model_registry.RegisteredModel` object.
        """
        headers = self.get_headers()
        url = 'https://mlflow.' + self.get_service() + '/api/2.0/mlflow/registered-models/update'

        body = dict()
        body['name'] = name
        if (description):
            body['description'] = description

        try:
            response = requests.patch(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        regmod = response.json()['registered_model']
        ct = None
        dscr = None
        lu = None
        if ('creation_timestamp' in regmod):
            ct = regmod['creation_timestamp']
        if ('description' in regmod):
            dscr = regmod['description']
        if ('last_updated_timestamp' in regmod):
            lu = regmod['last_updated_timestamp']
        return RegisteredModel(regmod['name'], creation_timestamp=ct,
                last_updated_timestamp=lu, description=dscr,
                latest_versions=None, tags=None)

    def list_registered_models(self, max_results, page_token):
        """
        List of all registered models.

        :param max_results: Maximum number of registered models desired.
        :param page_token: Token specifying the next page of results. It should be obtained from
                            a ``list_registered_models`` call.
        :return: A PagedList of :py:class:`mlflow.entities.model_registry.RegisteredModel` objects
                that satisfy the search expressions. The pagination token for the next page can be
                obtained via the ``token`` attribute of the object.
        """
        headers = self.get_headers()
        url = 'https://mlflow.' + self.get_service() + '/api/2.0/mlflow/registered-models/list'

        try:
            response = requests.get(url,
                    params={'max_results':max_results, 'page_token':page_token},
                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        respjson = json.loads(response.text)
        registered_models = respjson['registered_models']
        next_page_token = None
        if ('next_page_token' in respjson):
            next_page_token = respjson['next_page_token']
        return PagedList(registered_models, next_page_token)

    def __init__(self, store_uri=None, artifact_uri=None):
        super().__init__(self.cognito_host_creds)


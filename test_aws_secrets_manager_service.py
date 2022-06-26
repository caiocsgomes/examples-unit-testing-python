from unittest import TestCase
from unittest.mock import MagicMock, patch
import pytest
from aws_secrets_manager_service import SecretsManagerService


def secrets_manager_response():
    return {'ARN': 'arn:aws:secretsmanager:us-east-1:322620855520:secret:test-secret-E4eZVd',
            'Name': 'test-secret',
            'VersionId': 'ef70fce6-d14c-452b-9951-fc7b138cd535',
            'SecretString': '{"test-key":"test-value"}',
            'VersionStages': ['AWSCURRENT']}


class TestSecretsManagerService(TestCase):
    mock_boto: MagicMock
    secrets_manager_service: SecretsManagerService

    @classmethod
    def setUp(cls):
        cls.secrets_manager_service = SecretsManagerService()

    @patch('aws_secrets_manager_service.boto3')
    def test_get_secret(self, mock_boto):
        mock_session = mock_boto.session.Session()
        mock_client = mock_session.client()
        mock_client.get_secret_value.return_value = secrets_manager_response()
        secret_response = self.secrets_manager_service.get_secret("test")
        assert 'SecretString' in secret_response

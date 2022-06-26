from unittest import TestCase
from unittest.mock import MagicMock, patch
from aws_secrets_manager_service import SecretsManagerService
import os
import boto3
from moto import mock_secretsmanager


def secrets_manager_correct_response():
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
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    @patch('aws_secrets_manager_service.boto3')
    def test_get_secret(self, mock_boto):
        mock_session = mock_boto.session.Session()
        mock_client = mock_session.client()
        mock_client.get_secret_value.return_value = secrets_manager_correct_response()
        secret_response = self.secrets_manager_service.get_secret("test")
        assert 'SecretString' in secret_response

    @mock_secretsmanager
    def test_get_secret_with_moto(self):
        conn = boto3.client("secretsmanager", region_name="us-east-1")
        conn.create_secret(Name="test-secret", SecretString="test-password")
        response = self.secrets_manager_service.get_secret("test-secret")
        assert response['SecretString'] == "test-password"

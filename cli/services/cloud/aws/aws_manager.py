import textwrap

from cli.common.utils.os_utils import detect_command_presence
from cli.services.cloud.aws.aws_sdk import AwsSdk
from cli.services.cloud.aws.iam_permissions import vpc_permissions, eks_permissions, s3_permissions, \
    own_iam_permissions, iam_permissions
from cli.services.cloud.cloud_provider_manager import CloudProviderManager

CLI = 'aws'


class AWSManager(CloudProviderManager):
    """AWS wrapper."""

    def __init__(self, region, profile, key, secret):
        self.__aws_sdk = AwsSdk(region, profile, key, secret)

    @property
    def region(self):
        return self.__aws_sdk.region

    @property
    def account_id(self):
        return self.__aws_sdk.account_id

    def detect_cli_presence(self) -> bool:
        """Check whether `name` is on PATH and marked as executable."""
        return detect_command_presence(CLI)

    def create_iac_state_storage(self, bucket: str):
        """
        Creates cloud native terraform remote state storage
        :return: Resource identifier, Region
        """
        return self.__aws_sdk.create_bucket(bucket)

    def destroy_iac_state_storage(self, bucket: str):
        """
        Destroy cloud native terraform remote state storage
        """
        return self.__aws_sdk.delete_bucket(bucket)

    def create_iac_backend_snippet(self, location: str, region: str, service="default"):
        if region is None:
            region = self.region
        # TODO: consider replacing with file template
        return textwrap.dedent('''\
        backend "s3" {{
          bucket = "{bucket}"
          key    = "terraform/{service}/terraform.tfstate"
          region  = "{region}"
          encrypt = true
        }}'''.format(bucket=location, region=region, service=service))

    def create_hosting_provider_snippet(self):
        # TODO: consider replacing with file template
        return textwrap.dedent('''\
        provider "aws" {
          default_tags {
            tags = {
              ClusterName   = local.name
              ProvisionedBy = local.ProvisionedBy
            }
          }
        }''')

    def create_k8s_role_binding_snippet(self):
        # TODO: consider replacing with file template
        return "serviceAccountName"

    def get_k8s_auth_command(self) -> str:
        args = [
            '--region',
            '<CLUSTER_REGION>',
            'eks',
            'get-token',
            '--cluster-name',
            "<CLUSTER_NAME>",
            "--output",
            "json"
        ]
        return "aws", args

    def get_k8s_token(self, cluster_name: str) -> str:
        token = self.__aws_sdk.get_token(cluster_name=cluster_name)
        return token['status']['token']

    def evaluate_permissions(self) -> bool:
        """
        Check if provided credentials have required permissions
        :return: True or False
        """
        missing_permissions = []
        missing_permissions.extend(self.__aws_sdk.blocked(vpc_permissions))
        missing_permissions.extend(self.__aws_sdk.blocked(eks_permissions))
        missing_permissions.extend(self.__aws_sdk.blocked(iam_permissions))
        missing_permissions.extend(self.__aws_sdk.blocked(s3_permissions))
        missing_permissions.extend(self.__aws_sdk.blocked(own_iam_permissions, [self.__aws_sdk.current_user_arn()]))
        if len(missing_permissions) == 0:
            return True
        else:
            return False

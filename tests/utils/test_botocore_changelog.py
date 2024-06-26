from pathlib import Path
from unittest.mock import patch

import pytest

from mypy_boto3_builder.utils.botocore_changelog import BotocoreChangelog


class TestBotocoreChangelogChangelog:
    @pytest.fixture(autouse=True)
    def patch_urlopen(self):
        with patch("mypy_boto3_builder.utils.botocore_changelog.urlopen") as urlopen_mock:
            urlopen_mock.return_value.__enter__().read.return_value = (
                Path(__file__).parent / "fake_changelog.rst"
            ).read_bytes()
            yield

    def test_existing(self):
        botocore_changelog = BotocoreChangelog()
        assert botocore_changelog.fetch_updated("1.22.5") == [
            "autoscaling",
            "ec2",
            "eks",
            "sagemaker",
            "textract",
        ]
        assert botocore_changelog.fetch_updated("1.22.4") == [
            "emr-containers",
            "chime-sdk-messaging",
            "chime-sdk-identity",
        ]

    def test_non_existing(self):
        botocore_changelog = BotocoreChangelog()
        assert botocore_changelog.fetch_updated("4.0.0") == []

"""Fetch a SecureString parameter from AWS SSM Parameter Store and print it.

Used by `entrypoint.sh` at container startup on EC2 to populate
OPENAI_API_KEY from the SSM parameter named in OPENAI_PARAM_NAME. The
EC2's instance profile (granted via Terraform — see infra/main.tf)
provides the IAM permission `ssm:GetParameter` on that one parameter
ARN; boto3 picks up the credentials automatically via the EC2 metadata
service.

Locally we never invoke this script: docker-compose passes the
developer's own OPENAI_API_KEY directly, the entrypoint sees it set,
and skips the SSM lookup.

Exit codes:
    0  printed the parameter value to stdout (no trailing newline)
    1  OPENAI_PARAM_NAME is not set
    2  the SSM call failed (network, IAM, or parameter does not exist)
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    param_name = os.environ.get("OPENAI_PARAM_NAME")
    if not param_name:
        print("OPENAI_PARAM_NAME is not set", file=sys.stderr)
        return 1

    # boto3 reads region from the first source it finds:
    # AWS_REGION env var, AWS_DEFAULT_REGION env var, ~/.aws/config.
    # It does NOT auto-discover region from EC2 IMDS (it does for
    # credentials, not for region), so we pass it explicitly and fail
    # loudly with a clearer message than boto3's NoRegionError.
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if not region:
        print(
            "AWS_REGION is not set. On EC2, add `AWS_REGION=<region>` to "
            "/home/ubuntu/food-tier-app/.env and `docker compose restart backend`.",
            file=sys.stderr,
        )
        return 3

    # Imported lazily so the (small) boto3 import cost is only paid on
    # the EC2 path, not on every local container start.
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    ssm = boto3.client("ssm", region_name=region)
    try:
        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    except (BotoCoreError, ClientError) as exc:
        print(f"failed to fetch SSM parameter {param_name!r}: {exc}", file=sys.stderr)
        return 2

    # `end=""` so the value pipes cleanly into a shell variable.
    print(response["Parameter"]["Value"], end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())

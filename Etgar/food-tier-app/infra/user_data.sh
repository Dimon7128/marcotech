#!/bin/bash
# =============================================================================
#  EC2 bootstrap — runs once at first boot via cloud-init.
#
#  Installs:
#    * Docker Engine + Compose plugin (official Docker apt repo)
#    * git, unzip, curl
#    * AWS CLI v2
#
#  Prepares:
#    * /home/ubuntu/food-tier-app/backend/data  (compose's bind-mount target)
#    * `ubuntu` user added to the `docker` group
#    * SSM Agent enabled (pre-installed via snap on Ubuntu 22.04 AMIs)
#
#  Does NOT:
#    * Deploy the app — that is the CD workflow's job (via SSM Run Command).
#    * Place docker-compose.yml on the box — copy it once with the README.
# =============================================================================

set -euxo pipefail

# All cloud-init output ends up in /var/log/cloud-init-output.log — handy
# for debugging from the AWS console if first boot misbehaves.

# --- 1. base packages -------------------------------------------------------
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg git unzip

# --- 2. Docker Engine + Compose plugin (official repo) ---------------------
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

. /etc/os-release
cat >/etc/apt/sources.list.d/docker.list <<EOF
deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu ${VERSION_CODENAME} stable
EOF

apt-get update -y
apt-get install -y --no-install-recommends \
    docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable --now docker
usermod -aG docker ubuntu

# --- 3. AWS CLI v2 ---------------------------------------------------------
# The Ubuntu apt package is v1; we install v2 from Amazon directly.
curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip
unzip -q /tmp/awscliv2.zip -d /tmp
/tmp/aws/install
rm -rf /tmp/aws /tmp/awscliv2.zip

# --- 4. SSM Agent ----------------------------------------------------------
# Pre-installed on Ubuntu 22.04 LTS AMIs via snap. The unit name reflects
# that. We restart it so the new instance profile is picked up on a fresh
# boot (the agent reads its credentials lazily).
systemctl restart snap.amazon-ssm-agent.amazon-ssm-agent.service || true

# --- 5. Project skeleton ---------------------------------------------------
# The CD workflow expects this folder to exist and to be owned by ubuntu.
# It will NOT deploy the docker-compose.yml — copy it once per the README
# (curl from the GitHub raw URL).
install -d -o ubuntu -g ubuntu /home/ubuntu/food-tier-app
install -d -o ubuntu -g ubuntu /home/ubuntu/food-tier-app/backend
install -d -o ubuntu -g ubuntu /home/ubuntu/food-tier-app/backend/data

# Helpful breadcrumb file so a future operator knows this box was set up
# by Terraform and what to expect.
cat >/home/ubuntu/food-tier-app/README.bootstrap <<'EOF'
This EC2 was provisioned by Terraform (food-tier-app/infra).
Next steps (one-time, done by a human or by an SSM command):
  1. Place docker-compose.yml at /home/ubuntu/food-tier-app/docker-compose.yml
  2. Place .env at /home/ubuntu/food-tier-app/.env with:
       DOCKERHUB_USERNAME=<your-dockerhub-user>
       IMAGE_TAG=staging   (or "prod" on the prod EC2)
       OPENAI_API_KEY=<your-openai-key>
After that, the CD workflow (food-tier-cd-deploy.yml) takes over.
EOF
chown ubuntu:ubuntu /home/ubuntu/food-tier-app/README.bootstrap

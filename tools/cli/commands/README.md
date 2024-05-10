# CG DevX CLI Commands

Below is a list of commands supported by the CG DevX CLI tool.

## Setup

Creates and configures the reference implementation of the CG DevX K8s Internal Developer Platform (IDP) kit. The CLI tool saves the intermediate state to a local file (checkpoints) when running through multiple setup steps and can be re-run.

### What the `setup` command checks:
- Presence of Cloud CLI tools
- Cloud account permissions using the provided profile or access keys
- DNS provider permissions using the provided token or access keys
- Domain ownership

### What the `setup` command creates:
- SSH key pairs
- Remote backend storage (e.g., AWS S3) for Infrastructure as Code (IaC)
- GitOps repository under the Git provider of your choice
- K8s cluster and supporting cloud resources provisioned by the CG DevX CLI

The `setup` command can be executed using arguments, environment variables, or an input file.

**Arguments**:

| Name (short, full)             | Type                                    | Description                                       |
|--------------------------------|-----------------------------------------|---------------------------------------------------|
| -e, --email                    | TEXT                                    | Email address used for alerts                     |
| -c, --cloud-provider           | [aws]                                   | Cloud provider type                               |
| -cp, --cloud-profile           | TEXT                                    | Cloud account profile                             |
| -cc, --cloud-account-key       | TEXT                                    | Cloud account access key                          |
| -cs, --cloud-account-secret    | TEXT                                    | Cloud account access secret                       |
| -r, --cloud-region             | TEXT                                    | Cloud regions                                     |
| -n, --cluster-name             | TEXT                                    | Cluster name                                      |
| -d, --dns-registrar            | [route53]                               | DNS registrar                                     |
| -dt, --dns-registrar-token     | TEXT                                    | DNS registrar token                               |
| -dk, --dns-registrar-key       | TEXT                                    | DNS registrar key                                 |
| -ds, --dns-registrar-secret    | TEXT                                    | DNS registrar secret                              |
| -dn, --domain-name             | TEXT                                    | Domain name used by the K8s cluster               |
| -g, --git-provider             | [github]                                | Git provider                                      |
| -go, --git-org                 | TEXT                                    | Git organization name                             |
| -gt, --git-access-token        | TEXT                                    | Git access token                                  |
| -grn, --gitops-repo-name       | TEXT                                    | GitOps repository name                            |
| -gtu, --gitops-template-url    | TEXT                                    | GitOps repository template URL                    |
| -gtb, --gitops-template-branch | TEXT                                    | GitOps repository template branch                 |
| -dw, --setup-demo-workload     | Flag                                    | Setup demo workload                               |
| -f, --config-file              | FILENAME                                | Load parameters from a file                       |
| --verbosity                    | [DEBUG, INFO, WARNING, ERROR, CRITICAL] | Set the logging verbosity level, default CRITICAL |

> **Note:** Use kebab-case for all names.

**parameters.yaml** file example:
```yaml
email: user@cgdevx.io
cloud-provider: aws
cloud-profile: profile-name
cloud-region: eu-west-1
cluster-name: cluster-name
dns-registrar: route53
domain-name: demo.cgdevx.io
git-provider: github
git-org: CGDevX
git-access-token: ghp_xxx
gitops-repo-name: cgdevx-gitops

Command Snippets:
Using command arguments:

cgdevxcli setup --email user@cgdevx.io \ 
                --cloud-provider aws \ 
                --cloud-profile your-profile-name \ 
                --cluster-name cluster-name \ 
                --dns-registrar route53 \
                --domain-name example.com \ 
                --git-provider github \
                --git-org acmeinc \
                --git-access-token ghp_xxx \
                --gitops-repo-name gitops-repo-name

Using a parameter file:
cgdevxcli setup -f path/to/your/parameters.yaml

Troubleshooting
The installation of a reference architecture is a complex process that depends on multiple factors, such as cloud resource availability, connection speed, and image registry rate limits. While we do our best to handle common problems and provide an uninterrupted experience, the setup process may still fail. If you encounter connectivity or resource availability errors, please try restarting the setup process. It should resume from the step where it previously failed.

Destroy

This command destroys all resources created during the setup process, effectively reversing the setup. It uses local state data created during the setup.

What the destroy command deletes:
K8s cluster and supporting cloud resources provisioned by the CG DevX CLI
GitOps repository created under the Git provider of your choice
Remote backend storage (e.g., AWS S3) used for IaC
All local files created by the CG DevX CLI
NOTE: This process is irreversible.
NOTE: This operation will delete all workload repositories. If workloads have any out-of-cluster (cloud provider) resources, they will become orphaned and should be manually deleted. It is highly recommended to delete all active workloads and associated resources before destroying your installation. See more on the workload delete command with the --destroy-resources flag here.
Arguments:

Name (short, full)	Type	Description
--verbosity	[DEBUG, INFO, WARNING, ERROR, CRITICAL]	Set the logging verbosity level, default CRITICAL

Command Snippet:
cgdevxcli destroy

Troubleshooting
Some resources used by the reference architecture are created dynamically at runtime. During cleanup, we attempt to destroy these temporary resources and then all other resources created by our automation. The cleanup process may still fail. If you encounter issues, please try restarting the process. If it fails to delete your K8s cluster, consider manually deleting any associated Load Balancers and restarting the process. For GitHub, external action runners should be removed prior to repository deletion. If it fails to delete your GitOps repo, please check and remove runners and restart the process.

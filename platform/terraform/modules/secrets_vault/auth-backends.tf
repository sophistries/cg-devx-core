###AWS specific data sources begin
data "aws_eks_cluster" "cluster" {
  name = var.cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}
###AWS specific data sources end

resource "vault_auth_backend" "k8s" {
  type = "kubernetes"
  path = "kubernetes/cgdevx"
}

resource "vault_kubernetes_auth_backend_config" "k8s" {
  backend         = vault_auth_backend.k8s.path
  kubernetes_host = data.aws_eks_cluster.cluster.endpoint
##uncomment this string only for local dev server vault installation
#  kubernetes_ca_cert     = "-----BEGIN CERTIFICATE-----\nexample\n-----END CERTIFICATE-----"
}

resource "vault_kubernetes_auth_backend_role" "k8s_atlantis" {
  backend                          = vault_auth_backend.k8s.path
  role_name                        = "atlantis"
  bound_service_account_names      = ["atlantis"]
  bound_service_account_namespaces = ["atlantis"]
  token_ttl                        = 86400
  token_policies                   = ["admin", "default"]
}

resource "vault_kubernetes_auth_backend_role" "k8s_external_secrets" {
  backend                          = vault_auth_backend.k8s.path
  role_name                        = "external-secrets"
  bound_service_account_names      = ["external-secrets"]
  bound_service_account_namespaces = ["external-secrets-operator"]
  token_ttl                        = 86400
  #is it necessary to have admin for external secrets?
  token_policies = ["admin", "default"]
}

resource "vault_auth_backend" "userpass" {
  type = "userpass"
  path = "userpass"
}
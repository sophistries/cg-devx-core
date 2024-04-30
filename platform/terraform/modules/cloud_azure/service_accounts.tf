module "iac_pr_automation_sa" {
  source = "./modules/aks_rbac"

  oidc_issuer_url         = azurerm_kubernetes_cluster.aks_cluster.oidc_issuer_url
  resource_group_name     = azurerm_resource_group.rg.name
  resource_group_location = azurerm_resource_group.rg.location
  name                    = "atlantis"
  service_account_name    = "atlantis"
  role_definitions        = [
    { "name" = "Contributor", "scope" = "" },
    { "name" = "User Access Administrator", "scope" = "" },
    { "name" = "Key Vault Administrator", "scope" = "" }
  ]
  namespace = "atlantis"
  tags      = merge(local.tags, {
    "cg-devx.metadata.service" : "iac-pr-automation"
  })


  depends_on = [azurerm_kubernetes_cluster.aks_cluster]
}

module "ci_sa" {
  source = "./modules/aks_rbac"

  oidc_issuer_url         = azurerm_kubernetes_cluster.aks_cluster.oidc_issuer_url
  resource_group_name     = azurerm_resource_group.rg.name
  resource_group_location = azurerm_resource_group.rg.location
  name                    = "argo-workflow"
  service_account_name    = "argo-server"
  role_definitions        = [{ "name" = "Contributor", "scope" = "" }]
  namespace               = "argo"
  tags                    = merge(local.tags, {
    "cg-devx.metadata.service" : "continuous-integration"
  })

  depends_on = [azurerm_kubernetes_cluster.aks_cluster]
}

module "cert_manager_sa" {
  source = "./modules/aks_rbac"

  oidc_issuer_url         = azurerm_kubernetes_cluster.aks_cluster.oidc_issuer_url
  resource_group_name     = azurerm_resource_group.rg.name
  resource_group_location = azurerm_resource_group.rg.location
  name                    = "cert-manager"
  service_account_name    = "cert-manager"
  role_definitions        = [{ "name" = "Contributor", "scope" = "" }]
  namespace               = "cert-manager"
  tags                    = merge(local.tags, {
    "cg-devx.metadata.service" : "cert-manager"
  })

  depends_on = [azurerm_kubernetes_cluster.aks_cluster]
}

module "external_dns_sa" {
  source = "./modules/aks_rbac"

  oidc_issuer_url         = azurerm_kubernetes_cluster.aks_cluster.oidc_issuer_url
  resource_group_name     = azurerm_resource_group.rg.name
  resource_group_location = azurerm_resource_group.rg.location
  name                    = "external-dns"
  service_account_name    = "external-dns"
  role_definitions        = [{ "name" = "Contributor", "scope" = "" }]
  namespace               = "external-dns"
  tags                    = merge(local.tags, {
    "cg-devx.metadata.service" : "external-dns"
  })

  depends_on = [azurerm_kubernetes_cluster.aks_cluster]
}

module "secret_manager_sa" {
  source = "./modules/aks_rbac"

  oidc_issuer_url         = azurerm_kubernetes_cluster.aks_cluster.oidc_issuer_url
  resource_group_name     = azurerm_resource_group.rg.name
  resource_group_location = azurerm_resource_group.rg.location
  name                    = "vault"
  service_account_name    = "vault"
  role_definitions        = [{ "name" = "Key Vault Administrator", "scope" = "" }]
  namespace               = "vault"
  tags                    = merge(local.tags, {
    "cg-devx.metadata.service" : "secret-manager"
  })

  depends_on = [azurerm_kubernetes_cluster.aks_cluster]
}

# Cluster Autoscaler
module "cluster_autoscaler_sa" {
  source = "./modules/aks_rbac"

  oidc_issuer_url         = azurerm_kubernetes_cluster.aks_cluster.oidc_issuer_url
  resource_group_name     = azurerm_resource_group.rg.name
  resource_group_location = azurerm_resource_group.rg.location
  name                    = "cluster-autoscaler"
  service_account_name    = "cluster-autoscaler"
  role_definitions        = [{ "name" = "Contributor", "scope" = "" }]
  namespace               = "cluster-autoscaler"
  tags                    = merge(local.tags, {
    "cg-devx.metadata.service" : "cluster-autoscaler"
  })

  depends_on = [azurerm_kubernetes_cluster.aks_cluster]
}

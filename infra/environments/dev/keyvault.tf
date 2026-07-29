resource "azurerm_key_vault" "kv" {
  name = "kv-retail-prado09"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  tenant_id = data.azurerm_client_config.current.tenant_id

  sku_name = "standard"

  rbac_authorization_enabled = false

  soft_delete_retention_days = 7
  purge_protection_enabled   = false

  tags = {
    environment = "dev"
  }

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

  secret_permissions = [
  "Get",
  "List",
  "Set",
  "Delete",
  "Recover",
  "Purge"
  ]
  }
}

resource "azurerm_key_vault_secret" "postgres_user" {
  name         = "postgres-user"
  value        = var.postgres_username
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "postgres_password" {
  name         = "postgres-password"
  value        = var.postgres_password
  key_vault_id = azurerm_key_vault.kv.id
}
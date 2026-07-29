# Outputs del entorno dev

output "resource_group_name" {
  description = "Nombre del Resource Group"
  value       = azurerm_resource_group.rg.name
}

output "resource_group_location" {
  description = "Ubicación del Resource Group"
  value       = azurerm_resource_group.rg.location
}

output "storage_account_name" {
  description = "Nombre de la Storage Account"
  value       = azurerm_storage_account.storage.name
}

output "storage_account_id" {
  description = "ID de la Storage Account"
  value       = azurerm_storage_account.storage.id
}

output "storage_primary_dfs_endpoint" {
  description = "Primary DFS Endpoint de la Storage Account"
  value       = azurerm_storage_account.storage.primary_dfs_endpoint
}

output "data_factory_name" {
  description = "Nombre del Data Factory"
  value       = azurerm_data_factory.adf.name
}

output "data_factory_id" {
  description = "ID del Data Factory"
  value       = azurerm_data_factory.adf.id
}

output "key_vault_name" {
  description = "Nombre del Key Vault"
  value       = azurerm_key_vault.kv.name
}

output "key_vault_uri" {
  description = "URI del Key Vault"
  value       = azurerm_key_vault.kv.vault_uri
}

output "log_analytics_workspace_id" {
  description = "ID del Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.law.id
}

output "action_group_id" {
  description = "ID del Action Group"
  value       = module.action_group.action_group_id
}

output "action_group_name" {
  description = "Nombre del Action Group"
  value       = module.action_group.action_group_name
}

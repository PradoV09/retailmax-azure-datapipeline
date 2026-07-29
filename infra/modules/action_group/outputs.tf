output "action_group_id" {
  description = "ID del Action Group"
  value       = azurerm_monitor_action_group.this.id
}

output "action_group_name" {
  description = "Nombre del Action Group"
  value       = azurerm_monitor_action_group.this.name
}

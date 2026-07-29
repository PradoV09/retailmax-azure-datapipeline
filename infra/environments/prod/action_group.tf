# Action Group para notificaciones
module "action_group" {
  source = "../../modules/action_group"

  action_group_name        = "ag-retailmax-prod"
  action_group_short_name  = "ag-rmx-prod"
  resource_group_name     = azurerm_resource_group.rg.name
  location                = azurerm_resource_group.rg.location
  email_address           = var.notification_email
  environment              = var.environment
}

# Módulo Action Group para Azure Monitor

resource "azurerm_monitor_action_group" "this" {
  name                = var.action_group_name
  resource_group_name = var.resource_group_name
  location            = var.location
  short_name          = var.action_group_short_name

  email_receiver {
    name                    = "email_receiver"
    email_address           = var.email_address
    use_common_alert_schema = true
  }

  tags = {
    environment = var.environment
  }
}

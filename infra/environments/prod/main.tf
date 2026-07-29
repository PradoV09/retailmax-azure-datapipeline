# Crear un grupo de recursos
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# Crear cuenta de almacenamiento
resource "azurerm_storage_account" "storage" {
  name                = var.storage_account_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true

  tags = {
    environment = var.environment
  }
}

resource "azurerm_storage_data_lake_gen2_filesystem" "bronze" {
  name               = "bronze"
  storage_account_id = azurerm_storage_account.storage.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "silver" {
  name               = "silver"
  storage_account_id = azurerm_storage_account.storage.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "gold" {
  name               = "gold"
  storage_account_id = azurerm_storage_account.storage.id
}

resource "azurerm_data_factory" "adf" {
  name                = "adf-retailmax-pradov09-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# Módulo SQL comentado temporalmente debido a restricciones de aprovisionamiento en la suscripción
# module "azure_sql" {
#
#   source = "../../modules/azure_sql"
#
#   sql_server_name = "sql-retailmax-prod-northeurope"
#
#   database_name = "retailmax"
#
#   resource_group_name = azurerm_resource_group.rg.name
#
#   location = "northeurope"
#
#   admin_username = "sqladmin"
#
#   admin_password = var.sql_admin_password
#
# }

data "azurerm_client_config" "current" {}

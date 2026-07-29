# Crear un grupo de recursos
resource "azurerm_resource_group" "rg" {
  name     = "rg-retailmax-dev"
  location = "East US"
}

# Crear cuenta de almacenamiento
resource "azurerm_storage_account" "storage" {
  name                     = "stretailmaxdev01"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location

  account_tier             = "Standard"
  account_replication_type = "LRS"

  is_hns_enabled = true

  tags = {
    environment = "dev"
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
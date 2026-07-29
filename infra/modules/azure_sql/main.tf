resource "azurerm_mssql_server" "sql_server" {

  name = var.sql_server_name

  resource_group_name = var.resource_group_name
  location            = var.location

  version = "12.0"

  administrator_login = var.admin_username

  administrator_login_password = var.admin_password

  minimum_tls_version = "1.2"

}


resource "azurerm_mssql_database" "database" {

  name = var.database_name

  server_id = azurerm_mssql_server.sql_server.id

  sku_name = "Basic"

  max_size_gb = 2

  tags = {
    environment = var.environment
    project     = "RetailMax"
  }

}
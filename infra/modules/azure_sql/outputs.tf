output "sql_server_id" {

  description = "ID del servidor SQL"

  value = azurerm_mssql_server.sql_server.id

}


output "sql_server_fqdn" {

  description = "Endpoint del servidor SQL"

  value = azurerm_mssql_server.sql_server.fully_qualified_domain_name

}


output "database_id" {

  description = "ID de la base de datos"

  value = azurerm_mssql_database.database.id

}
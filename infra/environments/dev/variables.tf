variable "postgres_username" {
  description = "Usuario de PostgreSQL"
  type        = string
  sensitive   = true
}

variable "postgres_password" {
  description = "Contraseña de PostgreSQL"
  type        = string
  sensitive   = true
}

variable "environment" {
  type = string
}

variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "storage_account_name" {
  type = string
}

variable "sql_admin_password" {

  description = "Password administrador Azure SQL"

  type = string

  sensitive = true

}
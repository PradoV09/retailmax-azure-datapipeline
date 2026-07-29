variable "sql_server_name" {

  description = "Nombre del servidor Azure SQL"

  type = string

}


variable "database_name" {

  description = "Nombre de la base de datos"

  type = string

}


variable "resource_group_name" {

  description = "Resource group donde se crea"

  type = string

}


variable "admin_username" {

  description = "Usuario administrador SQL"

  type = string

}

variable "admin_password" {

  description = "Password administrador SQL"

  type = string

  sensitive = true

}


variable "environment" {

  description = "Ambiente"

  type = string

  default = "dev"

}

variable "location" {

  description = "Region Azure"

  type = string

}
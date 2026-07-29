variable "action_group_name" {
  description = "Nombre del Action Group"
  type        = string
}

variable "action_group_short_name" {
  description = "Nombre corto del Action Group (máximo 12 caracteres)"
  type        = string
}

variable "resource_group_name" {
  description = "Nombre del Resource Group"
  type        = string
}

variable "location" {
  description = "Región de Azure"
  type        = string
}

variable "email_address" {
  description = "Correo electrónico para notificaciones"
  type        = string
}

variable "environment" {
  description = "Entorno (dev/prod)"
  type        = string
}

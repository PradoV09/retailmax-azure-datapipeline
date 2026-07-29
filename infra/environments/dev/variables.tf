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
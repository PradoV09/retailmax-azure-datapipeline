# Recomendamos encarecidamente usar el bloque required_providers para configurar el origen y la versión del proveedor de Azure que se está utilizando.
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 5.0"
    }
  }
}

# Configurar el proveedor de Microsoft Azure
provider "azurerm" {
  features {}
}
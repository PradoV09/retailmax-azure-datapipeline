terraform {
  backend "azurerm" {
    resource_group_name  = "rg-retailmax-dev"
    storage_account_name = "stretailmaxpv092026"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

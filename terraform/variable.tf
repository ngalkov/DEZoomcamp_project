variable "token" {
  description = "OAuth token from Yandex.OAuth"
  type        = string
  sensitive   = true
}

variable "cloud_id" {
  description = "cloud_id"
  type        = string
  sensitive   = true
}

variable "folder_id" {
  description = "folder_id"
  type        = string
  sensitive   = true
}

variable "network_id" {
  description = "network_id"
  type        = string
  sensitive   = true
}

variable "service_account_id" {
  description = "service_account_id"
  type        = string
  sensitive   = true
}

variable "access_key" {
  description = "Key ID"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Private key"
  type        = string
  sensitive   = true
}

variable "db_username" {
  description = "Database administrator username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}

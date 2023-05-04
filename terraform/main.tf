terraform {
  required_version = ">= 0.13"
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token     = var.token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  # zone = "ru-central1-a"
}

resource "yandex_storage_bucket" "bucket" {
  access_key = var.access_key
  secret_key = var.secret_key
  bucket = "uk-property"
}

resource "yandex_mdb_clickhouse_cluster" "cluster" {
  name               = "uk-property-cluster"
  environment        = "PRESTABLE"
  network_id         = var.network_id

  clickhouse {
    resources {
      resource_preset_id = "b2.nano"
      disk_type_id       = "network-hdd"
      disk_size          = 10
    }
  }

  host {
    type             = "CLICKHOUSE"
    zone             = "ru-central1-a"
    assign_public_ip = true
  }

  database {
    name = "uk_property"
  }

  user {
    name     = var.db_username
    password = var.db_password
    permission {
      database_name = "uk_property"
    }
  }

  service_account_id = var.service_account_id

  access {
     data_lens  = true
     web_sql    = true
  }
}

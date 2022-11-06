variable "cluster_version" {
  type = string
}

variable "worker_count" {
  type    = number
  default = 2
}

variable "worker_size" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "cluster_region" {
  type    = string
  default = "fra1"
}


variable "cluster_version" {
  type    = string
  default = "1.22"
}

variable "cluster_region" {
  type    = string
  default = "fra1"
}

variable "worker_count" {
  type    = number
  default = 2
}

variable "worker_size" {
  type    = string
  default = "s-2vcpu-4gb"
}

variable "write_kubeconfig" {
  type    = bool
  default = false
}

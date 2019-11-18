variable "key_name" {
  default = "private-passwd"
}

variable "pvt_key" {
  default = "/Users/titan/.ssh/id_rsa"
}

variable "sg-id" {
  default = ""
}

variable "vpc" {
  default = {}
}

variable "number_instances" {
  default = "1"
}

variable "region" {
  default = "eu-central-1"
}

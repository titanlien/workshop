variable "bucket_name" {
  type        = string
  description = "The name of S3 bucket"
}

variable "env" {
  type        = string
  description = "The name of environment, e.g: dev, stage and prod"
}

variable "namespace" {
  type        = string
  description = "The name of function, e.g: web, backend, db"
}

variable "username" {
  type        = string
  description = "The name of end user to upload file to s3"
}

variable "whitelistIPs" {
  type        = list(string)
  default     = []
  description = "Whitelist IP address allow uploader to access backup bucket, e.g: 127.0.0.1/32"
}

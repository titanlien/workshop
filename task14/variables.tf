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

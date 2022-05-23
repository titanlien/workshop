variable "env" {
  description = "The environment name to which this project will be applied against (e.g.: dev, prod, stage)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "The name of this project"
  type        = string
  default     = "task16"
}

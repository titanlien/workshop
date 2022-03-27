module "s3-bucket" {
  source  = "cloudposse/s3-bucket/aws"
  version = "0.49.0"
  enabled = true

  acl                           = "private"
  block_public_policy           = false
  block_public_acls             = false
  user_enabled                  = false
  versioning_enabled            = false
  lifecycle_configuration_rules = local.lifecycle_configuration_rules

  name      = var.bucket_name
  namespace = var.namespace
  stage     = var.env
}

module "iam-s3-user" {
  source  = "cloudposse/iam-s3-user/aws"
  version = "0.15.9"

  s3_resources = [
    local.s3-arn-with-star,
    module.s3-bucket.bucket_arn
  ]

  s3_actions = [
    "s3:PutObject",
    "s3:PutObjectAcl",
    "s3:GetObject",
    "s3:GetObjectAcl",
    "s3:DeleteObject",
    "s3:ListBucket",
  ]

  name      = var.username
  namespace = var.namespace
  stage     = var.env
}

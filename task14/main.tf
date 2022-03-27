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

resource "aws_iam_policy" "whitelist-policy" {
  name        = "whitelist-policy"
  description = "Reject all incoming request but excludes IPs in whitelistIPs and IPs of deployed host"
  policy      = templatefile("${path.module}/whitelist-ip.json.tmpl", { whitelistIPs = local.whitelistIPs })
}

resource "aws_iam_user_policy_attachment" "whitelist-attach" {
  user       = module.iam-s3-user.user_name
  policy_arn = aws_iam_policy.whitelist-policy.arn
}

data "http" "admin_ip" {
  url = "https://ipinfo.io/ip"
}

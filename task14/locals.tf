locals {
  lifecycle_configuration_rules = [{
    enabled = true # bool
    id      = "v2rule"

    abort_incomplete_multipart_upload_days = 1 # number

    filter_and = null
    expiration = {
      days = 120 # integer > 0
    }
    noncurrent_version_expiration = {
      newer_noncurrent_versions = 3  # integer > 0
      noncurrent_days           = 60 # integer >= 0
    }
    transition = [{
      days          = 30            # integer >= 0
      storage_class = "STANDARD_IA" # string/enum, one of GLACIER, STANDARD_IA, ONEZONE_IA, INTELLIGENT_TIERING, DEEP_ARCHIVE, GLACIER_IR.
      },
      {
        days          = 60           # integer >= 0
        storage_class = "ONEZONE_IA" # string/enum, one of GLACIER, STANDARD_IA, ONEZONE_IA, INTELLIGENT_TIERING, DEEP_ARCHIVE, GLACIER_IR.
    }]
    noncurrent_version_transition = [{
      newer_noncurrent_versions = 3            # integer >= 0
      noncurrent_days           = 30           # integer >= 0
      storage_class             = "ONEZONE_IA" # string/enum, one of GLACIER, STANDARD_IA, ONEZONE_IA, INTELLIGENT_TIERING, DEEP_ARCHIVE, GLACIER_IR.
    }]
  }]
}

locals {
  s3-arn-with-star = length(module.s3-bucket.bucket_arn) > 0 ? format("%s/%s", module.s3-bucket.bucket_arn, "*") : ""
}

locals {
  admin_ip_list = [format("%s/%s", data.http.admin_ip.body, "32")]
  whitelistIPs  = length(var.whitelistIPs) == 0 ? local.admin_ip_list : concat(local.admin_ip_list, var.whitelistIPs)
}

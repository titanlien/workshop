# -------------------------------------------------------------------------------------------------
# Remote State settings
# -------------------------------------------------------------------------------------------------

terraform {
  backend "s3" {
    bucket         = "tfstate-demo-workshop"
    key            = "task16/dev"
    region         = "eu-central-1"
    dynamodb_table = "tfstate-demo-state-backend"
    encrypt        = true
    kms_key_id     = "alias/tfstate-demo-default"
  }
}

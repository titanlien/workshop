terraform {
  backend "s3" {
    bucket = "tfstate-demo-workshop"
    key    = "upload-s3"
    region = "eu-central-1"
  }
}

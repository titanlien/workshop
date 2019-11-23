terraform {
  backend "s3" {
    bucket = "tf-poc-dev"
    key    = "navVis/terraform.tfstate"
    region = "eu-central-1"
  }
}

locals {
  regions = {
    dev        = "eu-central-1"
    staging    = "eu-central-1"
  }

  worker_instance_count = {
    dev        = "1"
    staging    = "2"
  }
}

module "worker" {
  source           = "./worker"
  region           = local.regions[terraform.workspace]
  number_instances = local.worker_instance_count[terraform.workspace]
  vpc              = module.vpc
  sg-id            = aws_security_group.allow_ssh.id
}

resource "null_resource" "ansible-worker" {
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ./ansible/inventory --limit nodes ./ansible/java.yml -u ubuntu"
  }

  depends_on = [module.worker]
}

provider "aws" {
  region = local.regions[terraform.workspace]
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow port 22 inbound traffic"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["217.86.133.43/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "java-BE"

  cidr = "172.16.0.0/16"

  azs             = ["${local.regions[terraform.workspace]}a"]
  public_subnets  = ["172.16.1.0/24", "172.16.2.0/24"]

  enable_nat_gateway = false

  tags = {
    Project     = "backend"
    Environment = "${terraform.workspace}"
    Name        = "teffaform vpc"
  }
}


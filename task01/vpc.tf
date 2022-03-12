provider "aws" {
  region = local.regions[terraform.workspace]
}

resource "aws_security_group" "allow_task1" {
  name        = "sg_task1"
  description = "Allow port 22 and 80 inbound traffic"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["217.86.133.43/32"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
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

  azs             = ["${local.regions[terraform.workspace]}a",
                     "${local.regions[terraform.workspace]}b"]
  public_subnets  = ["172.16.1.0/24", "172.16.2.0/24"]

  enable_nat_gateway = false

  tags = {
    Project     = "task1"
    Environment = "terraform.workspace"
    Name        = "teffaform vpc"
  }
}

resource "aws_security_group_rule" "allow_internal" {
  type            = "ingress"
  from_port       = 0
  to_port         = 65535
  protocol        = "all"
  self            = true
  security_group_id = aws_security_group.allow_task1.id
}

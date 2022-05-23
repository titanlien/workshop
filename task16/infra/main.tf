provider "aws" {
  region = local.region
}

data "aws_caller_identity" "current" {}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

################################################################################
# EKS Module
################################################################################

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.19.0"

  cluster_name                    = local.name
  cluster_version                 = local.cluster_version
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Self Managed Node Group(s)
  self_managed_node_group_defaults = {
    max_size      = 3
    desired_size  = 1
    instance_type = "t3a.large"
    tags          = { "aws-node-termination-handler/managed" = "true" }
  }
  self_managed_node_groups = {
    refresh = {
      instance_refresh = {
        strategy = "Rolling"
        preferences = {
          checkpoint_delay       = 600
          checkpoint_percentages = [35, 70, 100]
          instance_warmup        = 300
          min_healthy_percentage = 50
        }
        triggers = ["tag"]
      }

      bootstrap_extra_args = "--kubelet-extra-args '--node-labels=node.kubernetes.io/lifecycle=refresh'"
    }

    mixed_instance = {
      use_mixed_instances_policy = true
      mixed_instances_policy = {
        instances_distribution = {
          on_demand_base_capacity                  = 0
          on_demand_percentage_above_base_capacity = 50
          spot_allocation_strategy                 = "capacity-optimized"
        }
        override = [
          {
            instance_type     = "t3a.medium"
            weighted_capacity = "4"
          },
          {
            instance_type     = "m6a.large"
            weighted_capacity = "1"
          },
        ]
      }

      bootstrap_extra_args = "--kubelet-extra-args '--node-labels=node.kubernetes.io/lifecycle=mix'"
    }

    spot = {
      desired_size = 2
      instance_market_options = {
        market_type = "spot"
      }

      bootstrap_extra_args = "--kubelet-extra-args '--node-labels=node.kubernetes.io/lifecycle=spot'"
    }
  }

  tags = local.tags
}

################################################################################
# aws-auth configmap
# Only EKS managed node groups automatically add roles to aws-auth configmap
# so we need to ensure fargate profiles and self-managed node roles are added
################################################################################

data "aws_eks_cluster_auth" "this" {
  name = module.eks.cluster_id
}


resource "null_resource" "apply" {
  triggers = {
    kubeconfig = base64encode(local.kubeconfig)
    cmd_patch  = <<-EOT
      kubectl create configmap aws-auth -n kube-system --kubeconfig <(echo $KUBECONFIG | base64 --decode)
      kubectl patch configmap/aws-auth --patch "${module.eks.aws_auth_configmap_yaml}" -n kube-system --kubeconfig <(echo $KUBECONFIG | base64 --decode)
    EOT
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    environment = {
      KUBECONFIG = self.triggers.kubeconfig
    }
    command = self.triggers.cmd_patch
  }
}

################################################################################
# Supporting Resources
################################################################################

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = local.name
  cidr = "10.0.0.0/16"

  azs             = ["${local.region}a", "${local.region}b", "${local.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.name}" = "shared"
    "kubernetes.io/role/elb"              = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.name}" = "shared"
    "kubernetes.io/role/internal-elb"     = 1
  }

  tags = local.tags
}

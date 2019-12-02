data "aws_ami" "work" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["ubuntu-bionic-18.04-amd64-server-*"]
  }

}

data "aws_availability_zones" "this" {}

resource "aws_spot_instance_request" "worker" {
  count                  = var.number_instances
  availability_zone      = data.aws_availability_zones.this.names[count.index % 2]
  ami                    = data.aws_ami.work.id
  instance_type          = "t3a.micro"
  key_name               = var.key_name
  vpc_security_group_ids = [var.sg-id]
  spot_price             = "0.01"
  spot_type              = "one-time"
  wait_for_fulfillment   = true
  subnet_id              = var.vpc.public_subnets[count.index % 2]

  tags = {
    index = count.index
  }

  # force Terraform to wait until a connection can be made, so that Ansible doesn't fail when trying to provision
  provisioner "remote-exec" {
    # The connection will use the local SSH agent for authentication
    inline = ["echo Successfully connected",
              "wget ${var.java-app-url} -P ~/"]

    connection {
      user        = "ubuntu"
      type        = "ssh"
      private_key = file(var.pvt_key)
      host        = self.public_ip
    }
  }
}

data "template_file" "inventory" {
  template = file("templates/inventory.tpl")

  depends_on = [
    aws_spot_instance_request.worker,
  ]

  vars = {
    nodes = join(
      "\n",
      aws_spot_instance_request.worker.*.public_ip,
    )
  }
}

resource "null_resource" "export" {
  triggers = {
    template_rendered = data.template_file.inventory.rendered
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.inventory.rendered}' > ./ansible/inventory"
  }
}

output spot_instance_ids_worker {
  description = "List of spot instance IDs of worker"
  value = aws_spot_instance_request.worker.*.spot_instance_id
}

output spot_instance_private_ip {
  value = aws_spot_instance_request.worker.*.private_ip
}

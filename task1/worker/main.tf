data "aws_availability_zones" "this" {}

resource "aws_spot_instance_request" "worker" {
  count                  = var.number_instances
  availability_zone      = data.aws_availability_zones.this.names[count.index]
  ami                    = "ami-07af7368ebacbf345"
  instance_type          = "t3a.micro"
  key_name               = var.key_name
  vpc_security_group_ids = ["${var.sg-id}"]
  spot_price             = "0.01"
  spot_type              = "one-time"
  wait_for_fulfillment   = true
  subnet_id              = var.vpc.public_subnets[0]

  # force Terraform to wait until a connection can be made, so that Ansible doesn't fail when trying to provision
  provisioner "remote-exec" {
    # The connection will use the local SSH agent for authentication
    inline = ["echo Successfully connected"]

    connection {
      user        = "ubuntu"
      type        = "ssh"
      private_key = file(var.pvt_key)
      host        = aws_spot_instance_request.worker[count.index].public_ip
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

resource "null_resource" "cmd" {
  triggers = {
    template_rendered = data.template_file.inventory.rendered
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.inventory.rendered}' > ./ansible/inventory"
  }
}

resource "null_resource" "ansible-worker" {
  count     = var.number_instances
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i '${aws_spot_instance_request.worker[count.index].public_ip},' ./ansible/site.yaml -u ubuntu"
  }

  depends_on = [null_resource.cmd]
}

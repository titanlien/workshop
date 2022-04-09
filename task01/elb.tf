resource "aws_elb" "task1" {
  name = "elb-taks1"

  subnets = module.vpc.public_subnets
  listener {
    instance_port     = 8080
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    target              = "HTTP:8080/"
    interval            = 30
  }

  instances                   = module.worker.spot_instance_ids_worker
  cross_zone_load_balancing   = true
  idle_timeout                = 400
  connection_draining         = true
  connection_draining_timeout = 400

  security_groups = [aws_security_group.allow_task1.id]

  depends_on = [module.worker]

  tags = {
    Name = "terraform-elb-task1"
  }
}

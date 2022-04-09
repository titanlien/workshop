data "aws_route53_zone" "mhlien" {
  name = "mhlien.de."
}

resource "aws_route53_record" "task1" {
  zone_id = data.aws_route53_zone.mhlien.zone_id
  name    = "task1"
  type    = "CNAME"
  ttl     = "30"
  records = [aws_elb.task1.dns_name]
}

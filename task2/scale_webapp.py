#!/usr/bin/env python3
import argparse

from jinja2 import Template, Environment, FileSystemLoader


def render_compose(count: int):
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("docker-compose.yml.j2")
    compose_ouput = template.render(count=list(range(1,count+1)))
    #print(compose_ouput)
    with open("./docker-compose.yml", "w") as f:
        f.write(compose_ouput)

def render_nginx(count: int):
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("nginx.conf.j2")
    nginx_ouput = template.render(count=list(range(1,count+1)))
    #print(nginx_ouput)
    with open("./nginx/nginx.conf", "w") as f:
        f.write(nginx_ouput)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scale up webapp by input number')
    parser.add_argument('web_count', metavar='N', type=int, choices=range(1, 200),
                        help='an natural number for webapp size, [1-200]')
    args = parser.parse_args()
    render_compose(args.web_count)
    render_nginx(args.web_count)

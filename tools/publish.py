# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/4/9
#

import urllib2
import base64
import json
import click

api_url = 'http://127.0.0.1:5000/api'
api_version = 'v1.0'
api_name = 'publish'
meta_fields = ['title', 'summary', 'tags', 'categories']


def publish(user, passwd, post):
    auth = 'Basic ' + base64.urlsafe_b64encode('%s:%s' % (user, passwd))
    req = urllib2.Request(
        '%s/%s/%s' % (api_url, api_version, api_name),
        data=post,
        headers={'Authorization': auth, 'Content-Type': 'application/json'})

    resp = urllib2.urlopen(req)
    print(resp.read())


def parse_post(filename, encoding):
    """Parse post data from source file."""
    has_meta, meta, body_index = False, {}, 0
    lines = click.open_file(filename, 'r', encoding=encoding).readlines()
    for idx, line in enumerate(lines):
        if line.startswith('---'):
            has_meta = True
            continue
        if line.startswith('...'):
            body_index = idx + 1
            break
        if has_meta and line.strip():
            key, value = (x.strip(' []') for x in line.strip().split(':', 1))
            meta[key] = value
    body = ''.join(lines[body_index:])

    post = {'body': body}
    for m in (set(meta_fields) & set(meta)):
        post[m] = meta[m]

    return json.dumps(post)


@click.command()
@click.option('-u', '--user', help='your username')
@click.option('-p', '--passwd', help='your password')
@click.option('-f', '--filename', type=click.Path(exists=True),
              help='your article filename')
@click.option('-e', '--encoding', help='input file encoding, default utf-8')
def cli(user, passwd, filename, encoding='utf8'):
    if not all([user, passwd, filename]):
        print('Error: rguments not enough.\n'
              'See publish --help for usage information.')
        exit()
    post = parse_post(filename, encoding)
    publish(user, passwd, post)


if __name__ == '__main__':
    cli()

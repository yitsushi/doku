import click
import os
import re
import tempfile
from datetime import datetime
from subprocess import Popen
from textwrap import indent

from doku.context import Context

pass_ctx = click.make_pass_decorator(Context)

"""
Potential:
    - dokuwiki.appendPage -> Diary
"""

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = Context()

@cli.command()
@click.option('--namespace', default='')
@pass_ctx
def list(ctx, namespace):
    pages = ctx.client.call('dokuwiki.getPagelist', namespace, [])
    for p in pages:
        t = datetime.utcfromtimestamp(p['rev']).strftime('%Y-%m-%d %H:%M:%S')
        print('[{date}] {page}'.format(page=p['id'], date=t))

@cli.command()
@click.argument('name')
@pass_ctx
def cat(ctx, name):
    print(ctx.client.call('wiki.getPage', name))

@cli.command()
@click.argument('query')
@pass_ctx
def search(ctx, query):
    results = ctx.client.call('dokuwiki.search', query)
    for hit in results:
        print('> {}'.format(hit['id']))
        if 'snippet' in hit:
            content = re.sub(
                r'</strong>|<strong class="search_hit">',
                '',
                hit['snippet']
            )
            print(indent(content, ' ' * 4, lambda line: True))
        print()

@cli.command()
@click.argument('name')
@pass_ctx
def edit(ctx, name):
    data = ctx.client.call('wiki.getPage', name)

    fp, path = tempfile.mkstemp(prefix='doku', suffix='.wiki', text=True)
    os.write(fp, data.encode())
    os.close(fp)

    with Popen([ctx.editor, path]) as proc:
        proc.wait()

    with open(path, 'r') as fp:
        ret = ctx.client.call(
            'wiki.putPage',
            name,
            fp.read(),
            {'sum': 'Updated with DokuSync'}
        )

        if ret:
            print('Document saved.')
        else:
            print('Something went wrong. :(')

    os.remove(path)


if __name__ == '__main__':
    cli()


import sys
import click
from cver.scraper import search as cve_search, lookup_cve

@click.group()
@click.version_option("1.0.0")
def main():
    """A CVE Search and Lookup CLI"""
    pass


@main.command()
@click.argument('keyword', required=False)
def search(**kwargs):
    """Search through CVE Database for vulnerabilities"""
    results = cve_search(kwargs.get("keyword"))
    for res in results:

        click.echo(f'{res["name"]} - {res["url"]} \n{res["description"]}')

@main.command()
@click.argument('name', required=False)
def look_up(**kwargs):
    """Get vulnerability details using its CVE-ID on CVE Database"""
    details = lookup_cve(kwargs.get("name"))
    click.echo(f'CVE-ID \n\n{details["cve-id"]}\n')
    click.echo(f'Description \n\n{details["description"]}\n')
    click.echo(f'References \n\n{details["references"]}\n')
    click.echo(f'Assigning CNA \n\n{details["assigning cna"]}\n')
    click.echo(f'Date Entry \n\n{details["date entry created"]}')


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    main()
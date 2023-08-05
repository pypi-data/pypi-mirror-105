import asyncio
import click
from merakitools.main import run
from merakitools import const

@click.group()
def cli():
    """ Tasks to start sync auto Sycn of Meraki Networks """
    pass


@click.command(name="port-config",help='Meraki Switch')
@click.option('-f','--configfile', help='Config File')
def port_config(configfile=None,):
    if configfile is not None:
        asyncio.run(run(configfile, 'device_config'))
        

cli.add_command(port_config)

import click
from yucebio_wdladaptor.backend import SUPPORTTED_BACKENDS, create_adaptor, PLACEHOLDER_SIMG_PATH, PLACEHOLDER_GLOBAL_PATH


@click.group()
def cli():
    pass


@cli.command()
@click.option("--input", "-i", required=False, help="input json file include project information")
@click.option("--platform", "-p", required=True, type=click.Choice(list(SUPPORTTED_BACKENDS)), help="platform")
@click.option("--submit", "-s", is_flag=True, default=False, help="auto submit to cromwell server")
@click.argument("wdl")
def convert(**kw):
    """根据不同平台具有的基础设施转换通用WDL，并自动适配json和task
    """
    adaptor = create_adaptor(kw['platform'])
    adaptor.parse(wdl_path=kw['wdl'], input_path=kw['input'])

    adaptor.convert()

    if not kw['submit']:
        adaptor.generate_file()
    else:
        jobid = adaptor.submit()
        click.secho(f"submit success: {jobid}", fg="green")



@cli.command()
@click.option("--platform", "-p", type=click.Choice(list(SUPPORTTED_BACKENDS)), help="platform")
@click.option('--host', '-h', help="cromwell server 地址")
@click.option('--global_path', '-g', help=f"公共文件路径，用于自动替换json中的[{PLACEHOLDER_GLOBAL_PATH}]", type=str)
@click.option('--simg_path', '-s', help=f"singulartiy镜像路径，用于自动替换json中的[{PLACEHOLDER_SIMG_PATH}]", type=str)
def config(**kw):
    """查看或更新计算平台配置"""
    platform = kw['platform']
    adaptor = create_adaptor(platform)
    
    cfg = {k: kw[k] for k in kw if k != 'platform' and kw[k]}
    if cfg:
        adaptor.config(platform, cfg)
    adaptor.pp(adaptor.config())



if __name__ == "__main__":
    cli()

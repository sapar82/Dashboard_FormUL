import click
from numpy import size
import pandas
import sys

from pprint import pprint

from canda.decoding_funcs import *
from canda.parsing_funcs import *


@click.group()
def app():
    """
    Human readable can bus data.
    """


@click.command()
@click.argument("database", type=click.Path(exists=True))
@click.argument("filename", type=click.Path(exists=True))
def decode_file(filename, database):
    """
    Decode a delimited text file produced by candump.
    """
    data: pandas.DataFrame = load_file(filename)
    database: cantools.db.can.Database = cantools.db.load_file(database)
    decoded_data: pandas.DataFrame = decode_can_binary(data, database)
    
    print(decoded_data.to_markdown())

@click.command()
@click.argument("database", type=click.Path(exists=True))
@click.argument("filename", type=click.Path(exists=True))
@click.argument("col", type=str)
def plot_file(filename, database, col):
    """Decode and plot the delimited text file.
    """
    data: pandas.DataFrame = load_file(filename)
    database: cantools.db.can.Database = cantools.db.load_file(database)
    decoded_data: pandas.DataFrame = decode_can_binary(data, database)

    from matplotlib import pyplot as plt
    plt.scatter(decoded_data.index, decoded_data[col], marker=".")
    plt.show()

@click.command()
@click.argument("database", type=click.Path(exists=True))
@click.argument("filename", type=click.Path(exists=True))
def missing_ids(filename, database):
    """
    Finds missing ids in a dbc file.
    """

    can_db = cantools.db.load_file(database)
    data: pandas.DataFrame = load_file(filename)

    missing_ids = find_unknown_ids(data, can_db)

    for id in missing_ids:
        sys.stdout.write(f"{id:#0{10}x}\n")


app.add_command(decode_file)
app.add_command(plot_file)
app.add_command(missing_ids)

if __name__ == "__main__":
    app()

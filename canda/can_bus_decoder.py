import pandas as pd
import copy
import matplotlib.pyplot as plt
import cantools
import pathlib
from typing import Union
from datetime import datetime


class CanDecoder:
    # TODO Revamp importing (see test.py)

    # TODO Add a way to define encoding, timeColumnName and other variables speicif to datatypes
    # TODO Define different ways to transform id data to significant name (ex: motor speed) and assigns ids by list to differents methods
    def __init__(self):

        self.raw = pd.DataFrame()
        self.decoded = {}
        self.availableIDs = []
        self.date = None

    def import_delimited_text(self, path: Union[str, pathlib.Path]):
        """Import CAN Data stored in a delimited text format.

        Args:
            path (str): path to data
        """

        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)

        if not path.exists():
            raise ValueError(f"Could not find {path.resolve()}.")

        self.raw = pd.read_csv(path, header=None, sep="  ", engine="python")

        # name columns
        self.raw.set_axis(["time", "can", "id", "size", "bytes"], axis=1, inplace=True)

        # remove useless columns
        self.raw.drop(["can", "size"], axis=1, inplace=True)

        # change id from str to hex
        self.raw["id"] = [hex(int(idd, 16)) for idd in self.raw["id"].tolist()]

        # change time format and save date
        self.raw["time"] = [float(time[1:-1]) for time in self.raw["time"].tolist()]

        # store date
        self.date = datetime.utcfromtimestamp(self.raw["time"][0]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # time starts at 0
        self.raw["time"] = self.raw["time"] - self.raw["time"][0]

        # combine bytes
        self.raw["bytes"] = [
            byte.replace(" ", "") for byte in self.raw["bytes"].to_list()
        ]

        # remove duplicate ids using dict (can be done using set?)
        self.availableIDs = list(dict.fromkeys(self.raw["id"]))

    def decode(self, path: str):
        """Decode CAN Bus data via dbc file using cantools

        Args:
            path (string): path to dbc file

        Returns:
            list: CAN bus ids not in dbc/failed to decode
        """
        # https://www.youtube.com/watch?v=CAy9Ji8bnqw

        if self.raw.empty:
            raise ValueError("No data to decode. Consider importing data first.")

        can_database = cantools.database.load_file(path)

        # transform to dict to remove duplicates
        decodable_ids = list(
            dict.fromkeys([hex(message.frame_id) for message in can_database.messages])
        )

        for row in self.raw.iterrows():
            # iterrows yields (index, Series)
            # Series object can be indexed as df
            serie = row[1]
            if serie["id"] in decodable_ids:
                # if id of row can be decoded
                # decode message and decompose into signals
                message = serie["bytes"]
                # turn id from hex to dec
                # decode message into bytes
                signals = can_database.decode_message(
                    int(serie["id"], 16), bytes.fromhex(message)
                )
                for key in signals:
                    # iterate over keys in dict (usually 1 but some messages (id) have multiple signals (different data))
                    if not self.decoded.get(key, False):
                        # create signal if not already created
                        self.decoded[key] = {"data": [], "time": []}

                    self.decoded[key]["data"].append(signals[key])
                    self.decoded[key]["time"].append(serie["time"])

        return [ID for ID in self.availableIDs if ID not in decodable_ids]

    def copy_data(self):
        """Creates copy of data

        Returns:
            dataframe: CAN bus data
        """
        return copy.deepcopy(self.raw)

    def read_id(self, id):
        """Read data of a specific id on CAN bus

        Args:
            id (str): CAN bus id to read data from

        Returns:
            DataFrame: CAN bus data on id
        """
        return self.raw.loc[self.raw["id"] == id]

    def create_figures(self):
        """Plots decoded data

        Returns:
            List: List of fig objects produced
        """
        # TODO Add plot instructions

        if not self.decoded:
            raise ValueError("No data to decode.")

        figures = []

        for key in self.decoded:
            fig = plt.figure()
            plt.plot(self.decoded[key]["time"], self.decoded[key]["data"])
            figures.append(fig)

        return figures

    def display_raw(self):
        # TODO https://stackoverflow.com/questions/12638408/decorating-hex-function-to-pad-zeros
        pass

    def export_raw(self, path: Union[str, pathlib.Path], export_to: str):
        if export_to == "excel":
            self.raw.to_excel(path, index=False)
        if export_to == "csv":
            self.raw.to_csv(path, index=False)

    def export_decoded(self, path: str):
        # TODO
        pass

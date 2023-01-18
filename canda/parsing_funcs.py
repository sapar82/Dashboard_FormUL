import pathlib
import pandas
from datetime import datetime

# Update this variable for each new supported file type.
SUPPORTED_FILE_TYPES = ["delimited"]

def load_file(
    file_path, file_type: str ="delimited"
) -> pandas.DataFrame:
    """Loads a file into a pandas dataframe.

    Args:
            file_path (Union[pathlib.Path, str]): The path towards the file to load.
            file_type (str, optional): The type of the file to parse. Defaults to
            `delimited`, which corresponds to `candump`'s output. Defaults to "delimited".

    Raises:
            ValueError: If the provided file path is not a valid path.
            FileNotFoundError: If the provided file_path does not exist.
            ValueError: If the provided file type is not supported. Supported file types
                                    are defined in the `SUPPORTED_FILE_TYPES` variable.

    Returns:
            pandas.DataFrame: The loaded file as a pandas dataframe.
    """

    if not isinstance(file_path, pathlib.Path):

        try:
            file_path = pathlib.Path(file_path)

        except TypeError as error:
            raise ValueError(f"{file_path} could not be converted to a file path.") from error

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    if file_type not in SUPPORTED_FILE_TYPES:

        err_msg = (
            f"{file_type} is not a supported file type. Supported file types are:\n"
        )
        for supported_file_type in SUPPORTED_FILE_TYPES:
            err_msg += supported_file_type + "\n"

        raise ValueError(err_msg)

    if file_type == "delimited":

        # Python engine used to avoid warning about regex. Two spaces are seen
        # as a regex and the c parser does not support it.
        # on_bad_lines="skip" used to avoid errors when a line is not well formatted.
        # Some ids are not well formatted and are not decoded. Eg: 00000
        df = pandas.read_csv(
            file_path, header=None, sep="  ", engine="python", dtype=object, on_bad_lines="skip"
        )

    df.set_axis(["time", "can", "id", "size", "bytes"], axis=1, inplace=True)
    df["time"] = df["time"].apply(lambda str_timestamp: datetime.fromtimestamp(float(str_timestamp.strip(")").strip("("))))

    return df

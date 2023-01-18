
from numpy import size
import pandas
from datetime import datetime

from pprint import pprint

from canda.decoding_funcs import *
from canda.parsing_funcs import *
def test_decode_file(data, database):
    data = pandas.read_csv(data,header=None, sep="  ", engine="python", dtype=object, on_bad_lines="skip")
    data.set_axis(["time", "can", "id", "size", "bytes"], axis=1, inplace=True)
    data["time"] = data["time"].apply(lambda str_timestamp: datetime.fromtimestamp(float(str_timestamp.strip(")").strip("("))))

    database: cantools.db.can.Database = cantools.db.load_file(database)
    decoded_data: pandas.DataFrame = decode_can_binary(data, database)


    #Export to csv
    #decoded_data.to_csv("decoded_data_7_aout.csv")
    return decoded_data

def test_decode_file_2(filename, database):
    data: pandas.DataFrame = load_file(filename)
    
    database: cantools.db.can.Database = cantools.db.load_file(database)
    decoded_data: pandas.DataFrame = decode_can_binary(data, database)

    #Export to csv
    #decoded_data.to_csv("decoded_data_7_aout.csv")
    return decoded_data


def plot_file(filename, database, col):
    """Decode and plot the delimited text file.
    """
    data: pandas.DataFrame = load_file(filename)
    database: cantools.db.can.Database = cantools.db.load_file(database)
    decoded_data: pandas.DataFrame = decode_can_binary(data, database)

    from matplotlib import pyplot as plt
    #Drop decoded_data[col] containing NaN
    graph_data = decoded_data[col].dropna()
    plt.plot(graph_data.index, graph_data.values, linewidth=0.5)
    plt.xlabel("Time (s)")
    plt.ylabel(col)

    plt.show()


#test_decode_file("test_txt/7aout2022-sortie2-1.txt", "dbc/formul_16_jan.dbc")

#plot_file("test_txt/7aout2022-sortie2-1.txt", "dbc/formul_16_jan.dbc", "Segment_5_scaled_20")

decoded_ids = ['0x8000080', '0x8010080', '0x8020080', '0x1800000', '0x99', '0x9a', '0x4440000', '0x4430000', 
                '0x4420000', '0x4410000', '0x4450000', '0x4110000', '0x4120000', '0x4130000', '0x4140000',
                '0x4150000', '0x2030000', '0x2030100', '0x2030200', '0x2030300', '0x2030400', '0x2030500', 
                '0x2030600', '0x2030700', '0x2030800', '0x2030900', '0x2030a00', '0x2030b00', '0x2030c00', 
                '0x2030d00', '0x2030e00', '0x2030f00', '0x2031000', '0x2031100', '0x2031200', '0x2031300', 
                '0x2020000', '0x2020100', '0x2020200', '0x2020300', '0x2020400', '0x2020500', '0x2020600', 
                '0x2020700', '0x2020800', '0x2020900', '0x2020a00', '0x2020b00', '0x2020c00']

int_decoded_ids = [int(id, 16) for id in decoded_ids]

all_ids = ['0000000A', '00000004', '04130000', '04140000', '04120000', '04010000'
            '04020000', '04030000', '04040000', '04110000', '08000080', '01800000'
            '01310000', '00000099', '0000009A', '08010080', '04840000', '04940000'
            '04740000', '04640000', '04540000', '04440000', '04930000', '04730000'
            '04630000', '04530000', '04830000', '04430000', '08020080', '0000000D'
            '0000000C', '00000008', '0000000B', '02020000', '02030000', '02070000'
            '02020100', '02030100', '02020200', '02030200', '02020300', '02030300'
            '02020400', '02030400', '02020500', '02030500', '02020600', '02030600'
            '02020700', '02030700', '02020800', '02030800', '02020900', '02030900'
            '02020A00', '02030A00', '02020B00', '02030B00', '02020C00', '02030C00'
            '02030D00', '02030E00', '02030F00', '02031000','02031100', '02031200'
            '02031300']

int_all_ids = [int(id, 16) for id in all_ids]


# Find the ids that are not decoded
not_decoded_int = []
for id in int_all_ids:
    if id not in int_decoded_ids:
        not_decoded_int.append(id)

not_decoded = [hex(id) for id in not_decoded_int]


not_decoded = ['0x180000001310000', '0x203030002020400', '0x203060002020700', '0x203090002020a00', 
                '0x2030c0002030d00', '0x203120002031300', '0x207000002020100', '0x4', '0x401000004020000',
                '0x4030000', '0x4040000', '0x4530000', '0x4540000', '0x4640000', '0x473000004630000', 
                '0x4830000', '0x4840000', '0x4930000', '0x494000004740000', '0x8', '0xa', '0xb', '0xd0000000c']
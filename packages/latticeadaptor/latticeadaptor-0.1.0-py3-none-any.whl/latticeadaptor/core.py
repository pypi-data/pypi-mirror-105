# -*- coding: utf-8 -*-

"""
Module latticeadaptor.core 
=================================================================

A module containing the main class to operate on accelerator lattices.

"""

# your imports here ...
import queue
from copy import deepcopy

from .parsers import (
    _parse_table_to_madx_definitions,
    parse_from_madx_sequence_file,
    parse_from_madx_sequence_string,
    parse_table_to_elegant_file,
    parse_table_to_elegant_string,
    parse_table_to_madx_install_str,
    parse_table_to_madx_remove_str,
    parse_table_to_madx_sequence_file,
    parse_table_to_madx_sequence_string,
    parse_table_to_tracy_file,
    parse_table_to_tracy_string,
)


class LatticeAdaptor:
    """Class to convert lattices."""

    def __init__(self, **kwargs):
        # roll back
        self.history = queue.LifoQueue()
        self.name = kwargs.get("name", None)
        self.len = kwargs.get("len", 0.0)
        self._table = None
        self.table = kwargs.get("table", None)
        self.filename = kwargs.get("file", None)
        self.inputstr = kwargs.get("string", None)

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        # roll back
        self.history.put((deepcopy(self.name), deepcopy(self.len), deepcopy(self.table)))

        self._table = value

    def load_from_madx_sequence_string(self, string: str) -> None:
        """Load lattice from sequence as string

        :param str string: string to load from.
        """

        # roll back
        self.history.put((deepcopy(self.name), deepcopy(self.len), deepcopy(self.table)))

        self.name, self.len, self.table = parse_from_madx_sequence_string(string)

    def load_from_madx_sequence_file(self, filename: str) -> None:
        """Load lattice from sequence in file

        :param str filename: file to load from
        """
        # roll back
        self.history.put((deepcopy(self.name), deepcopy(self.len), deepcopy(self.table)))

        self.name, self.len, self.table = parse_from_madx_sequence_file(filename)

    def parse_table_to_madx_sequence_string(self):
        """Parse table to madx sequence and return it as a string"""
        return parse_table_to_madx_sequence_string(self.name, self.len, self.table)

    def parse_table_to_madx_sequence_file(self, filename):
        """Parse table to madx sequence and write to file

        :param str filename: file to parse to
        """
        parse_table_to_madx_sequence_file(self.name, self.len, self.table, filename)

    def parse_table_to_elegant_string(self):
        """Parse table to elegant lattice file and return as string."""
        return parse_table_to_elegant_string(self.name, self.table)

    def parse_table_to_elegant_file(self, filename):
        """Parse table to elegant lattice and write to file

        :param str filename: file to parse to
        """
        parse_table_to_elegant_file(self.name, self.table, filename)

    def parse_table_to_tracy_string(self):
        """Parse table to tracy lattice file and return as string."""
        return parse_table_to_tracy_string(self.name, self.table)

    def parse_table_to_tracy_file(self, filename):
        """Parse table to tracy lattice and write to file

        :param str filename: file to parse to
        """
        parse_table_to_tracy_file(self.name, self.table, filename)

    def madx_sequence_add_start_end_marker_string(self):
        """Return madx string to install marker at start and at end of lattice"""
        return install_start_end_marker(self.name, self.len)

    def madx_sequence_save_string(self, filename):
        """
        Method to generate string input for madx
        to save the sequence.

                                                                                                                                        :param str filename: file to parse to
        """
        return "SAVE, SEQUENCE={}, file='{}';".format(self.name, filename)

    def add_drifts(self):
        """Method to add back drifts to sequence."""
        self.history.put((deepcopy(self.name), deepcopy(self.len), deepcopy(self.table)))

        df = self.table.copy()
        df.reset_index(inplace=True, drop=True)
        name = "D"
        family = "DRIFT"

        df.loc[df.L.isna(), "L"] = 0
        newrows = []
        ndrift = 0
        for i, row in df.iterrows():
            # add the row
            newrows.append(pd.DataFrame(row).T)

            # check if next row
            if i < len(df) - 1:
                # check if next row pos is not equal to the current
                nextrow = df.loc[i + 1]
                if nextrow["pos"] > row.pos:
                    ndrift += 1
                    newrow = {}
                    newrow["name"] = name + str(ndrift)
                    newrow["family"] = family
                    newrow["L"] = np.round(
                        (nextrow["pos"] - nextrow["L"] / 2.0) - (row["pos"] + row["L"] / 2.0), 6
                    )
                    newrow["pos"] = (row["pos"] + row["L"] / 2.0) + (newrow["L"] / 2.0)
                    newrows.append(pd.Series(newrow).to_frame().T)
        if nextrow["pos"] < self.len:
            newrow = {}
            newrow["name"] = name + str(ndrift)
            newrow["family"] = family
            newrow["L"] = np.round(self.len - nextrow["pos"], 6)
            newrow["pos"] = (row["pos"] + row["L"] / 2.0) + (newrow["L"] / 2.0)
            newrows.append(pd.Series(newrow).to_frame().T)

        self.table = (pd.concat(newrows)).reset_index(drop=True)

    def parse_table_to_madx_line_string(self):
        """Method to convert table to madx line def lattice file string."""
        add_drifts(self.table, self.len)
        defstr = _parse_table_to_madx_definitions(self.table)
        linestr = "{}: LINE=({});".format(
            name,
            ",\n\t\t".join(
                [",".join(c) for c in list(self.chunks(self.table.name.to_list(), 20))]
            ),
        )
        return defstr + "\n\n" + linestr

    @staticmethod
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst.

        :param list lst: list to chunk up
        :param int n: chunk size
        :returns: list of chunks of size n of the original list
        """
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    def parse_table_madx_line_file(self, filename: str):
        """Method to convert table to madx line def lattice file string and write to file.

        :param str filename: file to write to
        """
        save_string(self.parse_table_to_madx_line_string(), filename)

    def get_quad_strengths(self):
        """Method to return quadrupole strengths as a dict."""
        return (
            self.table.loc[self.table.family == "QUADRUPOLE", ["name", "K1"]]
            .set_index("name", drop=True)
            .to_dict()["K1"]
        )

    def get_sext_strengths(self):
        """Method to return sextupole strengths as a dict"""
        return (
            self.table.loc[self.table.family == "SEXTUPOLE", ["name", "K2"]]
            .set_index("name", drop=True)
            .to_dict()["K2"]
        )

    def load_strengths_to_table(self, strdc, col):
        """
        Method to load as strength dict to the table, col is the attribute where
        the strengths will be loaded to.

        :param dict strdc: dictionary with strength settings
        :param str col: column where the strengths need to be written to
        """
        self.history.put((deepcopy(self.name), deepcopy(self.len), deepcopy(self.table)))

        for k, v in strdc.items():
            self.table.loc[self.table["name"] == k, col] = v

    def compare_seq_center_positions(self, seqfile2):
        """
        Method to compare locations of elements in two
        MADX sequence files.

                                                                        :param str seqfile2: filename of second sequence
                                                                        :returns: equal and diff dataframes
        """
        # assert os.path.isfile(seqfile1)
        assert os.path.isfile(seqfile2)

        # name1, len1, df1 = parse_from_madx_sequence_file(seqfile1)
        name2, len2, df2 = parse_from_madx_sequence_file(seqfile2)

        table1 = self.table[["name", "pos"]]
        table2 = df2[["name", "pos"]]

        eq = pd.merge(table1, table2, on=["pos"], how="inner")
        diff = table1[~table1["pos"].isin(table2["pos"])]

        return eq, diff

    def undo(self):
        """Undo previous change."""
        if not self.history.empty():
            old = self.history.get()
            self.name, self.length, self.table = old
        else:
            print("No previous states available")

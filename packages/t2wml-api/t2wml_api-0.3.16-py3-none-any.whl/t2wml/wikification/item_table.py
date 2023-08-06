import json
from t2wml.utils.debug_logging import basic_debug, with_args_debug, t2wml_log
import pandas as pd
from pandas import DataFrame
from collections import defaultdict
from t2wml.utils.t2wml_exceptions import ItemNotFoundException
from t2wml.utils.bindings import bindings


class ItemTable:
    def __init__(self, lookup_table={}):
        self.lookup_table = defaultdict(dict, lookup_table)
    
    def __repr__(self):
        return "<Item Table>"

    @with_args_debug
    def lookup_func(self, context, file, sheet, column, row, value):
        lookup = self.lookup_table.get(context)
        if not lookup:
            raise ItemNotFoundException(
                "Search for cell item failed. (No values defined for context: {})".format(context))

        # order of priority: cell+value> cell> col+value> col> row+value> row> value
        column = int(column)
        row = int(row)
        tuples = [
            (file, sheet, column, row, value),
            ('', '', column, row, value),
            ('', '', column, row, ''),
            ('', '', column, '', value),
            ('', '', column, '', ''),
            ('', '', '', row, value),
            ('', '', '', row, ''),
            ('', '', '', '', value)
        ]

        for tup in tuples:
            item = lookup.get(str(tup))
            if item:
                return item
        raise ValueError("Not found")

    def get_item(self, column:int, row:int, context:str='', sheet=None, value=None):
        if not sheet:
            sheet = bindings.excel_sheet
        file=sheet.data_file_name
        sheet_name=sheet.name
        if value is None:
            value = str(sheet[row, column])
        try:
            item = self.lookup_func(context, file, sheet_name, column, row, value)
            return item
        except ValueError:
            return None  # currently this is what the rest of the API expects. could change later
        #   raise ItemNotFoundException("Item for cell "+to_excel(column, row)+"("+value+")"+"with context "+context+" not found")

    def get_item_by_string(self, value: str, context:str=''):
        lookup = self.lookup_table.get(context)
        if not lookup:
            raise ItemNotFoundException(
                "Search for cell item failed. (No values defined for context: {})".format(context))

        item = lookup.get(str(('', '', '', '', value)))
        if item:
            return item
        raise ItemNotFoundException("Could not find item for value: "+value)

    def get_cell_info(self, column, row, sheet):
        # used to serialize table
        bindings.excel_sheet = sheet
        for context in self.lookup_table:
            value= bindings.excel_sheet[row, column]
            item = self.get_item(column, row, context, sheet=sheet, value=value)
            if item:
                return item, context, value
        return None, None, None

    @with_args_debug
    def update_table_from_dataframe(self, df: DataFrame):
        try:
            t2wml_log.debug("replace na with empty string")
            df = df.fillna('')
            t2wml_log.debug("replace regex in dataframe")
            df = df.replace(r'^\s+$', '', regex=True)
            overwritten = {}
            
            t2wml_log.debug("gathering all tuples")
            tuples = list(df.itertuples())
            t2wml_log.debug(f"gathered {len(tuples)} tuples")

            t2wml_log.debug('Iterating over gathered tupled')
            for (idx, entry) in enumerate(tuples):
                t2wml_log.debug(f"entry index {idx}")
                t2wml_log.debug("fetching fields from entry:")
                column = entry.column
                row = entry.row
                value = str(entry.value)
                context = entry.context
                item = entry.item
                t2wml_log.debug(f"column {column} row {row} value {value} context {context} item {item}")
                try:
                    file = entry.file
                    sheet= entry.sheet
                except:
                    file=sheet="" #backwards compatible for now
                t2wml_log.debug(f" adding fields for: file {file} sheet {sheet}")

                if not item:
                    raise ValueError("Item definition missing")

                if column=="" and row=="" and value=="":
                    raise ValueError(
                        "at least one of column, row, or value must be defined")

                if column != "":
                    t2wml_log.debug("convert column to int")
                    column = int(column)
                if row != "":
                    t2wml_log.debug("convert row to int")
                    row = int(row)
                t2wml_log.debug("create tuple key")
                key = str((file, sheet, column, row, value))
                t2wml_log.debug(f"key: {str(key)}")
                t2wml_log.debug("check if already exists in lookup table")
                if self.lookup_table[context].get(key):
                    t2wml_log.debug("it does already exist")
                    overwritten[key] = self.lookup_table[context][key]
                else:
                    t2wml_log.debug("it doesn't already exist")
                t2wml_log.debug("add/overwrite in lookup table")
                self.lookup_table[context][key] = item
                t2wml_log.debug(f"Done with iteration {idx}")

            t2wml_log.debug('Exited loop')
            if len(overwritten):
                t2wml_log.debug("print count for overwritten")
                ##print("Wikifier update overwrote existing values: "+str(overwritten))
            t2wml_log.debug('returning from function')
            return overwritten
        except Exception as e:
            #print(e)
            raise e


class Wikifier:
    def __init__(self):
        self.wiki_files = []
        self._data_frames = []
        self._item_table = ItemTable()

    def print_data(self):
        """prints a little summary of the contents of the wikifier
        """
        print("The wikifier contains {} wiki files, and a total of {} dataframes".format(
            len(self.wiki_files), len(self._data_frames)))
        if len(self.wiki_files):
            print("The files are:")
            for filename in self.wiki_files:
                print(filename)

    @property
    def item_table(self):
        return self._item_table

    @with_args_debug
    def add_file(self, file_path: str):
        """add a wikifier file to the wikifier. loads the file and adds it to the item table.
        file must be a csv file, and must contain the columns 'row', 'column', 'value', 'context', 'item'
        (columns may be empty)

        Args:
            file_path (str): location of the wikifier file

        Raises:
            ValueError: if the wikifier file fails to apply

        Returns:
            dict: a dictionary describing which item definitions were already present and overwritten
        """
        df = pd.read_csv(file_path)
        try:
            overwritten = self.item_table.update_table_from_dataframe(df)
        except Exception as e:
            raise ValueError(
                "Could not apply {} : {}".format(file_path, str(e)))
        self.wiki_files.append(file_path)
        self._data_frames.append(df)
        return overwritten

    @with_args_debug
    def add_dataframe(self, df: DataFrame):
        """Add a wikifier dataframe to the Wikifier item table

        Args:
            df (DataFrame): a dataframe with columns 'row', 'column', 'value', 'context', 'item'        
            (columns may be empty)

        Raises:
            ValueError: not all columns defined
            ValueError: could not apply dataframe

        Returns:
            dict: a dictionary describing which item definitions were already present and overwritten
        """
        expected_columns = set(['row', 'column', 'value', 'context', 'item'])
        columns = set(df.columns)
        missing_columns = expected_columns.difference(columns)
        if len(missing_columns):
            raise ValueError(
                "Dataframe for wikifier must contain all 5 expected columns")
        try:
            overwritten = self.item_table.update_table_from_dataframe(df)
        except Exception as e:
            raise ValueError("Could not apply dataframe: "+str(e))
        self._data_frames.append(df)
        return overwritten

    @basic_debug
    def save(self, filename: str):
        """save Wikifier to a json file

        Args:
            filename (str): location of save file
        """
        output = json.dumps({
            "wiki_files": self.wiki_files,
            "lookup_table": self.item_table.lookup_table,
            "dataframes": [df.to_json() for df in self._data_frames]
        })
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(output)

    @classmethod
    @basic_debug
    def load(cls, filename:str):
        """load Wikifier from saved json file (created by the wikifier save method)

        Args:
            filename (str): location of save file

        Returns:
            Wikifier: initialized wikifier
        """
        with open(filename, 'r', encoding="utf-8") as f:
            wiki_args = json.load(f)
        wikifier = Wikifier()
        wikifier.wiki_files = wiki_args["wiki_files"]
        wikifier._item_table = ItemTable(
            lookup_table=wiki_args["lookup_table"])
        wikifier._data_frames = [pd.read_json(
            json_string) for json_string in wiki_args["dataframes"]]
        return wikifier

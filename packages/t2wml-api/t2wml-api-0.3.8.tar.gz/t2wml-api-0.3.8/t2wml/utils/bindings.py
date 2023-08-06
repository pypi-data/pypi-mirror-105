# bindings represents information used by classes/functions available in the t2wml parser
from t2wml.utils.debug_logging import basic_debug
class BindingsClass:
    def __init__(self):
        self.item_table = None
        self.excel_sheet = None


bindings = BindingsClass()

@basic_debug
def update_bindings(sheet=None, item_table=None) -> None:
    """
    This function updates the bindings dictionary with the excel_file, item_table, and sparql endpoint
    """
    if sheet:
        bindings.excel_sheet = sheet
    if item_table:
        bindings.item_table = item_table
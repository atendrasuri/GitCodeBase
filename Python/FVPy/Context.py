class Context:
  def __init__(self):
    self.data = []
    self.arguments = {}

    # PartialMode
    self.arguments['cfg_partialMode'] = "True"

    # Header 1_1 > <Row>_<Column>
    self.arguments['cfg_hdr_info'] = "{\"1_1\":\"FileName\",\"1_2\":\"GeneratedTime\"}"
    self.arguments['cfg_header_rows'] = "1"
    self.arguments['cfg_column_header_row'] = "2"
    self.arguments['cfg_hdr_delimiter'] = ","
    self.arguments["cfg_hdr_columns"] = "label_set, name, week_start, geo, indexed_queries"

    # Footer
    self.arguments['cfg_ftr_delimiter'] = ","
    self.arguments['cfg_ftr_info'] = "{\"1_1\":\"RowCount\"}"
    self.arguments['cfg_ftr_rows'] = 1

    # FileName Configurations
    self.arguments['cfg_fn_delimiter'] = "_"
    self.arguments['cfg_fn_info_str'] = "{\"FileName\":\"1,20\",\"GeneratedTime\":\"4,6\"}"

    # Section Zero KB
    self.arguments['cfg_chk_zero_kb'] = "True"
    self.arguments['cfg_chk_zero_kb_bytes'] = "0"

    # Section Duplicate File Check
    self.arguments["cfg_chk_duplicate_file"] = "True"

    # Section for Row Count Check
    self.arguments["cfg_chk_rowcount"] = "True"

    # Column Header Checks
    self.arguments["chk_col_headers"] = "True"

    # FileName Check
    self.arguments["cfg_chk_filename"] = "True"
    self.arguments["cfg_chk_filename_base"] = "Header"
    self.arguments["cfg_chk_filename_target"] = "Filename"

    # Datetime Check
    self.arguments["cfg_chk_datetime"] = "True"
    self.arguments["cfg_chk_datetime_base"] = "Header"
    self.arguments["cfg_chk_datetime_target"] = "Filename"
    self.arguments["cfg_chk_datetime_name"] = "GeneratedTime"

    # Control File Validation

  def getArguments(self):
    return self.arguments

from Context import Context
from emitter import Emitter

import ast
def transform(record, emitter, context):
  # Cask Bug
  record["fileSize"] = long(record["fileSize"])
  record["modificationTime"] = long(record["modificationTime"])

  class Config:
    "Parses configuration"
    def __init__(self, config_name, is_num=False, is_dic=False):
      self.name = config_name
      self.empty = False
      self.err = ""
      self.value = context.getArguments().get(config_name)
      if self.value is None:
        self.empty = True
      elif len(self.value.strip()) == 0:
        self.empty = True
      else:
        try:
          if is_num:
            self.value = long(self.value)
          elif is_dic:
            self.value = ast.literal_eval(self.value)
        except Exception, ex:
          self.err = str(ex)

  def convert(dict):
    txt = "{"
    for key in (dict.keys()):
      txt += "\"" + key + "\": \"" + dict[key] + "\","
    txt = txt[:len(txt)-1] + "}"
    return txt


  def parseByMap(file_txt, delimiter, parse_map, namedInfo, fillRowNum=0, fillRow=None):
    if file_txt is None:
      return
    rows = file_txt.splitlines()
    for ln_idx in range(0, len(rows)):
      row_str = rows[ln_idx]
      row_num = ln_idx + 1

      if row_num == fillRowNum:
        record[fillRow] = row_str
      else:
        row_arr = row_str.split(delimiter)
        for i in range(0, len(row_arr)):
          xy_coordinates = str(row_num) + '_' + str(i + 1)
          col_name = parse_map.get(xy_coordinates, xy_coordinates)
          if len(row_arr[i]) > 0:
            if col_name != xy_coordinates:
              namedInfo[col_name] = row_arr[i].strip()

  # Parse Header
  record['hdr_NamedInfo'] = "{}"
  record['hdr_column_headers'] = ""
  cfg_hdr_delimiter = Config('cfg_hdr_delimiter')
  cfg_column_header_row = Config('cfg_column_header_row', True)
  cfg_hdr_info = Config('cfg_hdr_info', False, True)
  if not cfg_hdr_info.empty:
    hdr_NamedInfo = {}
    parseByMap(record['header'], cfg_hdr_delimiter.value, cfg_hdr_info.value, hdr_NamedInfo,
               cfg_column_header_row.value, 'hdr_column_headers')
    record['hdr_NamedInfo'] = convert(hdr_NamedInfo)

  # Parse Footer
  record["ftr_NamedInfo"] = "{}"
  cfg_ftr_delimiter = Config('cfg_ftr_delimiter')
  cfg_ftr_info = Config('cfg_ftr_info', False, True)
  if not cfg_ftr_info.empty:
    ftr_NamedInfo = {}
    parseByMap(record['footer'], cfg_ftr_delimiter.value, cfg_ftr_info.value, ftr_NamedInfo)
    record['ftr_NamedInfo'] = convert(ftr_NamedInfo)

  # Parse FileName
  record["fn_NamedInfo"] = "{}"
  fileName = record["fileName"]
  fn_delimiter = Config('cfg_fn_delimiter')
  cfg_fn_info = Config('cfg_fn_info_str', False, True)
  if not cfg_fn_info.empty:
    fn_info_dic = cfg_fn_info.value
    fn_NamedInfo = {}
    if fileName.rfind(".") > 0:
      fileName = fileName[:fileName.rfind(".")]
      fn_NamedInfo["ext"] = record["fileName"].replace(fileName, "")
    fn_parts = fileName.split(fn_delimiter.value)
    for key in fn_info_dic.keys():
      cfg_fn_info = str(key)
      if key == "FileName":
        fn_NamedInfo[cfg_fn_info] = record["fileName"]
      else:
        lbound = int(fn_info_dic[key].split(",")[0])
        uboud = min(int(fn_info_dic[key].split(",")[1]), len(fn_parts))
        fn_info = ""
        for j in range(lbound - 1, uboud):
          fn_info += fn_parts[j] + fn_delimiter.value
        if len(fn_info) > 1:
          if fn_info[len(fn_info) - 1:] == "_":
            fn_info = fn_info[:len(fn_info) - 1]
        fn_NamedInfo[cfg_fn_info] = fn_info
    record["fn_NamedInfo"] = convert(fn_NamedInfo)
  emitter.emit(record)


context = Context()
emitter = Emitter()
record = {}
record["fileSize"] = "422"
record["modificationTime"] = "1524553674000"
record[
  'header'] = "google_brandindexedqueries_demo1_20180217_20180218_0629.txt, 20180217_20180218_0629" + "\n" + "label_set,name,week_start,geo,indexed_queries"
record['footer'] = None
record['fileName'] = "google_brandindexedqueries_noquotes_20180217_20180218_0629.txt"

transform(record, emitter, context)

from emitter import Emitter
from Context import Context

#import ast

def transform(record, emitter, context):
  class Config:
    "Parses configuration"
    def __init__(self, config_name, return_type=""):
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
          if return_type == "long":
            self.value = long(self.value)
          elif return_type == "dic":
            self.value = dict(x.split(':') for x in self.value[:-1][1:].split(','))
          elif return_type == "bool":
            self.value = bool(self.value)
        except Exception, ex:
          self.err = str(ex)

  # Get information from Header, Footer and Filename
  def getSectionInfos(cfg_section, info):
    def getInfoForSection(cfg_section, info):
      section = cfg_section.lower() + "_NamedInfo"
      if record[section] is not None and len(record[section]) > 0:
        section_dic = dict(x.split(':') for x in record[section][:-1][1:].split(','))
        return section_dic.get(info, "")
      return ""

    if len(cfg_section) > 0:
      cfg_section = cfg_section.replace("Header", "hdr").replace("Footer", "ftr").replace("Filename", "fn")
      return getInfoForSection(cfg_section, info)
    else:
      info_str = getInfoForSection("hdr", info)
      if len(info_str) == 0:
        info_str = getInfoForSection("ftr", info)
      if len(info_str) == 0:
        info_str = getInfoForSection("fn", info)
      return info_str

  # Zero KB Check Section
  cfg_chk_zero_kb = Config("cfg_chk_zero_kb", "bool")
  cfg_chk_zero_kb_bytes = Config("cfg_chk_zero_kb_bytes", "long")
  if cfg_chk_zero_kb.empty or cfg_chk_zero_kb_bytes.empty or cfg_chk_zero_kb.value == False:
    record["chk_zero_kb"] = "NOT_CONFIGURED - chk_zero_kb " + cfg_chk_zero_kb.err + cfg_chk_zero_kb_bytes.err
  else:
    fileSize = record["fileSize"]
    if fileSize <= cfg_chk_zero_kb_bytes.value:
      record["chk_zero_kb"] = "FAILED: File size is " + str(fileSize) + "bytes, Expected over " + str(
        cfg_chk_zero_kb_bytes.value) + " bytes."
    else:
      record["chk_zero_kb"] = "PASSED"

  # Duplicate file check Section
  cfg_chk_duplicate_file = Config("cfg_chk_duplicate_file", "bool")
  if cfg_chk_duplicate_file.empty or cfg_chk_duplicate_file.value == False:
    record["chk_duplicate_file"] = "NOT_CONFIGURED - chk_duplicate_file " + cfg_chk_duplicate_file.err
  else:
    if record["VfFileName"] is not None:
      if len(record["VfFileName"].strip()) > 0:
        record["chk_duplicate_file"] = "FAILED: File received before in JobID = " + record["VfJobId"] + " TivoliId = " + \
                                       record["VfTivoliId"]
      else:
        record["chk_duplicate_file"] = "PASSED"
    else:
      record["chk_duplicate_file"] = "PASSED"

  # Rowcount Check
  cfg_chk_rowcount = Config("cfg_chk_rowcount", "bool")
  if cfg_chk_rowcount.empty or cfg_chk_rowcount.value == False:
    record["chk_rowcount"] = "NOT_CONFIGURED - chk_rowcount " + cfg_chk_rowcount.err
  else:
    expected_count = getSectionInfos("", "RowCount")
    if len(expected_count.strip()) > 0:
      try:
        expected_count = long(expected_count)
        rows_found = record['rowNum']
        if expected_count == rows_found:
          record["chk_rowcount"] = "PASSED: record count matched, " + str(expected_count) + " records found"
        else:
          record["chk_rowcount"] = "FAILED: record count expected - " + str(
            expected_count) + " but found - " + str(rows_found)
      except Exception, ex:
        record["chk_rowcount"] = "FAILED: Failed to find expected record count " + str(ex)

  # Filename Check
  cfg_chk_filename = Config("cfg_chk_filename", "bool")
  base_section = Config("cfg_chk_filename_base")
  tgt_section = Config("cfg_chk_filename_target")

  if cfg_chk_filename.empty or base_section.empty or tgt_section.empty or cfg_chk_filename.value == False or \
      base_section.value not in ["Header", "Footer", "Filename"] or \
      tgt_section.value not in ["Header", "Footer", "Filename"]:
    record[
      "chk_filename"] = "NOT_CONFIGURED - chk_filename " + cfg_chk_filename.err + base_section.err + tgt_section.err
  else:
    base_str = getSectionInfos(base_section.value, "FileName")
    if len(base_str) > 0:
      tgt_str = getSectionInfos(tgt_section.value, "FileName")
      if len(tgt_str) > 0:
        if base_str == tgt_str:
          record["chk_filename"] = "PASSED: filename matched - " + base_str
        else:
          record["chk_filename"] = "FAILED: filename do not match - " + base_str + " - " + tgt_str
      else:
        record["chk_filename"] = "FAILED: target filename not found"
    else:
      record["chk_filename"] = "FAILED: base filename not found"

  # Generated Datetime Check
  cfg_chk_datetime = Config("cfg_chk_datetime", "bool")
  dt_base_section = Config("cfg_chk_datetime_base")
  dt_tgt_section = Config("cfg_chk_datetime_target")
  dt_var_name = Config("cfg_chk_datetime_name")

  if cfg_chk_datetime.empty or cfg_chk_datetime.value == False or \
      dt_base_section.empty or dt_tgt_section.empty or dt_var_name.empty or \
      dt_base_section.value not in ["Header", "Footer", "Filename"] or \
      dt_tgt_section.value not in ["Header", "Footer", "Filename"]:
    record[
      "chk_datetime"] = "NOT_CONFIGURED - chk_datetime " + cfg_chk_datetime.err + dt_base_section.err + dt_tgt_section.err + dt_var_name.err
  else:
    base_str = getSectionInfos(base_section.value, dt_var_name.value)
    if len(base_str) > 0:
      tgt_str = getSectionInfos(tgt_section.value, dt_var_name.value)
      if len(tgt_str) > 0:
        if base_str == tgt_str:
          record["chk_datetime"] = "PASSED: datetime matched - " + base_str
        else:
          record["chk_datetime"] = "FAILED: datetime do not match - " + base_str + " - " + tgt_str
      else:
        record["chk_datetime"] = "FAILED: target datetime not found"
    else:
      record["chk_datetime"] = "FAILED: base datetime not found"

  # Column Headers chk
  chk_col_headers = Config("chk_col_headers", "bool")
  cfg_hdr_columns = Config("cfg_hdr_columns")
  cfg_hdr_delimiter = Config('cfg_hdr_delimiter')

  if chk_col_headers.empty or chk_col_headers.value == False or cfg_hdr_columns.empty or cfg_hdr_delimiter.empty:
    record[
      "chk_col_headers"] = "NOT_CONFIGURED - chk_col_headers " + chk_col_headers.err + cfg_hdr_columns.err + cfg_hdr_delimiter.err
  else:
    record["chk_col_headers"] = ""
    cfg_hdr_columns = (cfg_hdr_columns.value).replace("\"", "").replace("\'", "")
    cfg_hdr_col_list = cfg_hdr_columns.split(cfg_hdr_delimiter.value)

    hdr_column_headers = record["hdr_column_headers"]
    if hdr_column_headers is not None and len(hdr_column_headers.strip()) > 1:
      hdr_column_headers = str(hdr_column_headers.replace("\"", "").replace("\'", ""))
      hdr_col_list = hdr_column_headers.split(cfg_hdr_delimiter.value)
      cfg_hdr_col_list = map(str.lower, map(str.strip, cfg_hdr_col_list))
      hdr_col_list = map(str.lower, map(str.strip, hdr_col_list))
      if set(cfg_hdr_col_list) == set(hdr_col_list):
        record["chk_col_headers"] = "PASSED: Found Expected Columns " + str(hdr_col_list)
      else:
        record["chk_col_headers"] = "FAILED: Config expects " + str(cfg_hdr_col_list) + " columns but found " + str(
          hdr_col_list)
    else:
      record["chk_col_headers"] = "FAILED: Failed to find columns in source "

  emitter.emit(record)


emitter = Emitter()
context = Context()
record = {}
record["fileName"] = "google_brandindexedqueries_demo3_20180217_20180218_0629.txt"
record["fileSize"] = long("321")
record["modificationTime"] = long("1524553662000")
record[
  "hdr_NamedInfo"] = "{\"FileName\":\"google_brandindexedqueries_demo3_20180217_20180218_0629.txt\", \"GeneratedTime\":\"20180217_20180218_0628\"}"
record[
  "fn_NamedInfo"] = "{\"FileName\":\"google_brandindexedqueries_demo3_20180217_20180218_0629\", \"GeneratedTime\":\"20180217_20180218_0629\"}"
record["ftr_NamedInfo"] = "{\"RowCount\":\"4\"}"
record["rowNum"] = long("4")
record["VfFileName"] = "google_brandindexedqueries_noquotes_20180217_20180218_0629"
record["VfJobId"] = "Job_201804231912000"
record["VfTivoliId"] = "TivoliID233"
record["hdr_column_headers"] = 'label_set,name,week_start,geo,indexed_queries'
transform(record, emitter, context)

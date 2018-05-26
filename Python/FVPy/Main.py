import unittest
import ast
from HeaderFooterFileNameParser import transform
from Context import Context
from emitter import Emitter

class HeaderFooterTest(unittest.TestCase):

  def test_transform(self):
    context = Context()
    emitter = Emitter()

    def getResult(dicx, column_name, info_name):
      output = ""
      # Example "hdr_NamedInfo"
      if dicx.has_key(column_name):
        # "hdr_NamedInfo"
        infos = ast.literal_eval(dicx[column_name])
        # "FileName"
        output = infos.get(info_name)
      return output

    #set Config
    context.arguments['cfg_hdr_info'] = "{\"1_1\":\"FileName\",\"1_2\":\"GeneratedTime\"}"
    context.arguments['cfg_header_rows'] = "1"
    context.arguments['cfg_column_header_row'] = "2"
    context.arguments['cfg_hdr_delimiter'] = ","
    context.arguments["cfg_hdr_columns"] = "label_set, name, week_start, geo, indexed_queries"

    #Header to Test
    record = {}
    record["fileSize"] = "422"
    record["modificationTime"] = "1524553674000"
    record['header'] = "google_brandindexedqueries_demo1_20180217_20180218_0629.txt, 20180217_20180218_0629" \
                  + "\n" + "label_set,name,week_start,geo,indexed_queries"
    record['footer'] = None
    record['fileName'] = "google_brandindexedqueries_noquotes_20180217_20180218_0629.txt"
    transform(record, emitter, context)

    runtime_result = ""
    expected_result = "google_brandindexedqueries_demo1_20180217_20180218_0629.txt"
    runtime_result = getResult(emitter.record, "hdr_NamedInfo", "FileName")
    self.assertEqual(runtime_result,expected_result,"FileName Parsing from Header")

    expected_result = "20180217_20180218_0629"
    runtime_result = ""
    runtime_result = getResult(emitter.record, "hdr_NamedInfo", "GeneratedTime")
    self.assertEqual(runtime_result,expected_result,"GeneratedTime Parsing from Header")

if __name__ == '__main__':
  unittest.main()


# var_str = "{\"FileName\":\"1,20\",\"GeneratedTime\":\"4,6\"}"
# var_str = var_str[1:-1]
# var_str = var_str.replace('\'','\"').replace('\",\"','\";\"')
# dic = dict(x.replace('\"','').split(':') for x in var_str.split(';'))
# pl = dic.keys()
# print(dic.keys())
class Emitter:
  def __init__(self):
    self.data = []
    self.record = {}

  kwrags = {}

  def emit(self, kwarg):
    self.record = kwarg
    kwargs = locals()
    keys = sorted(kwargs.keys())
    for kw in keys:
      print kw, ":", kwargs[kw]

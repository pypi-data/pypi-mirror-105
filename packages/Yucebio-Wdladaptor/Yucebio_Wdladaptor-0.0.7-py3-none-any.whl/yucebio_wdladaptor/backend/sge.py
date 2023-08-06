import re
from yucebio_wdladaptor.backend.base import BaseAdaptor
import yucebio_wdladaptor.util.wdl_v1_parser as WDL


class Adaptor(BaseAdaptor):
    """转换WORKFLOW到泰州SGE平台

    不需要额外处理，Cromwell的SGE backend中可以支持singularity适配
    """
    PLATFORM = "SGE"

    def convert(self):
        pass

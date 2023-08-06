#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging
import os

import pandas as pd
from scutils import Singleton
from scutils.file_utils import ensure_dir

from excel.utils import config


class Splitter(metaclass=Singleton):

    def __init__(self):
        pass

    def split(self):
        # 源路径
        source_file_path = config.get("excel.source_file_path")
        logging.getLogger(__name__).info("源文件路径：{}".format(source_file_path))
        # 输出目标路径
        target_directory = config.get("excel.target_directory")
        logging.getLogger(__name__).info("目标路径：{}".format(target_directory))
        # 确保目标路径存在
        ensure_dir(target_directory)

        source_filename = os.path.basename(source_file_path)
        (filename, ext) = os.path.splitext(source_filename)

        branch_list = config.get("excel.branch_list")
        logging.getLogger(__name__).info("机构列表配置：{}".format(branch_list))
        if type(branch_list) is not list:
            logging.getLogger(__name__).info("配置项 'excel.branch_list' 配置错误")
            return 1

        sheet_config_dict = config.get("excel.sheet_config")
        logging.getLogger(__name__).info("Sheet配置：{}".format(sheet_config_dict))
        if type(sheet_config_dict) is not dict:
            logging.getLogger(__name__).info("配置项 'excel.sheet_config' 配置错误")
            return 1
        if len(sheet_config_dict) <= 1:
            logging.getLogger(__name__).info("配置项 'excel.sheet_config' 配置错误，缺少导出Sheet的配置")
            return 1

        for branch in branch_list:
            logging.getLogger(__name__).info("开始处理机构：{}".format(branch))
            target_filename = os.path.join(target_directory, filename + "-" + branch + ext)
            first = True
            if first:
                # 如果是第一个Sheet，首先删除已有文件
                if os.path.exists(target_filename):
                    os.remove(target_filename)
                first = False
            with pd.ExcelWriter(target_filename) as writer:
                for sheet_name, sheet_config in sheet_config_dict.items():
                    if "other_sheets" == sheet_name and type(sheet_config) == list:
                        # 其他Sheet直接读取按原样输出
                        for other_sheet in sheet_config:
                            df = pd.read_excel(source_file_path, sheet_name=other_sheet)
                            df.to_excel(writer, sheet_name=other_sheet, index=False)
                        continue
                    # 如果是需要拆分的Sheet
                    logging.getLogger(__name__).info("开始处理Sheet：{}".format(sheet_name))
                    df = pd.read_excel(source_file_path, sheet_name=sheet_name, header=sheet_config["header"])
                    column_index = sheet_config["branch_column"]
                    column_name = df.columns[column_index]
                    sub_df = df[df[column_name] == branch]
                    sub_df.to_excel(writer, sheet_name=sheet_name, index=False)
        return 0

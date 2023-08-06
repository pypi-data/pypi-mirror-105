.. image:: https://badge.fury.io/py/sc-excel-splitter.svg
    :target: https://badge.fury.io/py/sc-excel-splitter
.. image:: https://img.shields.io/pypi/pyversions/sc-excel-splitter
    :alt: PyPI - Python Version

A simple Python project sample structure
========================================

This project provides a sample structure for creating python project.


Installation
------------

It is possible to install the tool with `pip`::

    pip install sc-excel-splitter

Configuration
-------------

First, make sure /var/opt/sc directory exists, if not create this directory and make sure current user has the right
to create files in this directory.

You can copy `default.yml <https://github.com/Scott-Lau/sc-excel-splitter/blob/master/excel/tests/sample_config/default.yml>`_
to /var/opt/sc/.sc-excel-splitter/production.yml to initialize the production configuration.

The default configuration file looks like this::

    dev:
      # whether this program is running is development mode
      dev_mode: False

    excel:
      # 源文件路径
      source_file_path: "/path/to/source_excel_file.xlsx"
      # 导出文件的保存路径
      target_directory: "/path/to/target/"
      # 网点名称列表
      branch_list:
        - "A支行"
        - "B支行"
      # 需要按列拆分的Sheet以及拆分所在列
      sheet_config:
        # 需要拆分的Sheet名称，用双引号包围
        "Sheet1":
          # 机构列所在列的索引（从0开始计数，第一列为0，依此类推）
          branch_column: 3
          # 表头所在行的索引（从0开始计数，第一列为0，依此类推）
          header: 2
        # 需要拆分的Sheet名称，用双引号包围
        "Sheet2":
          # 机构列所在列的索引（从0开始计数，第一列为0，依此类推）
          branch_column: 17
          # 表头所在行的索引（从0开始计数，第一列为0，依此类推）
          header: 0
        # 其他需要导出的Sheet名称列表
        other_sheets:
          # Sheet名称
          - "Sheet3"
          # Sheet名称
          - "Sheet4"

License
-------

The script is released under the MIT License.  The MIT License is registered
with and approved by the Open Source Initiative [1]_.

.. [1] https://opensource.org/licenses/MIT

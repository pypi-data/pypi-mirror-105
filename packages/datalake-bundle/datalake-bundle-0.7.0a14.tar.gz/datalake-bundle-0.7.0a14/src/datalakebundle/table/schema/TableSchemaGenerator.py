from pyspark.sql.types import StructType


class TableSchemaGenerator:
    def generate(self, schema: StructType) -> str:
        table_schema = ""

        table_schema += "table_schema = TableSchema(\n"
        table_schema += "    [\n"

        for field in schema:
            table_schema += f'        t.StructField("{field.name}", t.{field.dataType}()),\n'

        table_schema += "    ],\n"
        table_schema += '    #  primary_key="",  # INSERT PRIMARY KEY COLUMN(s) HERE (OPTIONAL)\n'
        table_schema += '    #  partition_by="",  # INSERT PARTITION KEY COLUMN(s) HERE (OPTIONAL)\n'
        table_schema += ")\n"

        return table_schema

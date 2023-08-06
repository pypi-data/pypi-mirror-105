from pyspark.sql import DataFrame


class SchemaClassGenerator:
    def generate(self, table_identifier: str, df: DataFrame) -> str:
        db = table_identifier.split(".")[0]
        table = table_identifier.split(".")[1]
        schema_class = ""

        schema_class += f"class {table}:\n"
        schema_class += f'    db = "{db}"\n'
        schema_class += "    fields = [\n"

        for field in df.schema:
            schema_class += f'        t.StructField("{field.name}", t.{field.dataType}()),\n'

        schema_class += "    ]\n"
        schema_class += '    primary_key = "" # INSERT PRIMARY KEY(s) HERE (MANDATORY)\n'
        schema_class += '    # partition_by = "" # INSERT PARTITIONS KEY(s) HERE (OPTIONAL)\n'

        return schema_class

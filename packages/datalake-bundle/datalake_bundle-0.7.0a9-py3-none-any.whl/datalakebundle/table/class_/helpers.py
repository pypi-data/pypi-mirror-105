def field_names(table_class) -> [str]:
    return [field.name for field in table_class.fields]

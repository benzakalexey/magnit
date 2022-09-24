from magnit.adapters.database import metadata

SCHEMA_HEADER = 'MAGNIT'
TITLE = 'Схема БД'

# Standards
UNIQUE_MARK = '[u]'
NULLABLE_MARK = '*'
ONE_TO_MANY_RELATION_MARK = '}o--||'


def _render_table_description(table, show_comment=True):
    def format_col_type(col_):
        if col_.foreign_keys:
            fk = next(iter(col_.foreign_keys))
            return f'ForeignKey({fk.column.table.name})'
        return str(col_.type).lower()

    def format_col_str(col):
        unique_mark = f'{UNIQUE_MARK} ' if col.unique else ''
        nullable_mark = f'{NULLABLE_MARK} ' if col.nullable else ''

        if show_comment:
            comment = f' - {col.comment}' if col.comment else ''
        else:
            comment = ''

        return f'{nullable_mark}' \
               f'**{unique_mark}{col.name}**  :  ' \
               f'{format_col_type(col)}{comment}'

    table_description = f'entity {table.name} {"{"}\n'
    delimiter_count = 0
    for col_ in table.columns:
        delimiter_count += 1
        table_description += f'\t {format_col_str(col_)}'
        if delimiter_count == 1:
            table_description += '\n\t__\n'
        if 1 < delimiter_count != len(table.columns):
            table_description += '\n\t--\n'

    table_description += '\n}\n\n'
    return table_description


def _render_tables_relations(tables=None):
    tables_relations = ''
    for table in tables:
        for fk in table.foreign_keys:
            if fk.column.table not in tables:
                continue
            table_relation = f'{table.name} ' \
                             f'{ONE_TO_MANY_RELATION_MARK} ' \
                             f'{fk.column.table.name}\n'
            tables_relations += table_relation
    return tables_relations


def _create_db_schema_body(metadata_=None):
    if metadata is not None:
        if not len(metadata.tables):
            metadata.reflect()
        tables = metadata.tables.values()
    else:
        raise ValueError("You need to specify metadata")

    db_schema_body = ''
    for table in tables:
        table_description = _render_table_description(table)
        db_schema_body += table_description

    db_schema_body += '\n'
    tables_relations = _render_tables_relations(tables)
    db_schema_body += tables_relations
    return db_schema_body


def create_db_schema(metadata_=None):
    db_schema_body = _create_db_schema_body(metadata_)
    db_schema = f'@startuml DB_MODEL\n\n' \
                f'header {SCHEMA_HEADER}\n' \
                f'title {TITLE}\n\n' \
                f'hide circle\n' \
                f'skinparam linetype ortho\n\n' \
                f'{db_schema_body}\n' \
                f'@enduml'
    return db_schema


if __name__ == '__main__':
    db_schema = create_db_schema(metadata)
    print(db_schema)

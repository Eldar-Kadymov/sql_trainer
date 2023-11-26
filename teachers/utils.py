import io
from django.core.files.base import ContentFile
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import csv

def convert_to_csv(query_result):
    csv_result = ""
    if query_result:
        headers = [desc for desc in query_result[0].keys()]
        csv_result += ','.join(headers) + '\n'

        for row in query_result:
            values = [str(value) for value in row]
            csv_result += ','.join(values) + '\n'

    return csv_result


DB_URL = "postgresql://postgres:root@127.0.0.1:5432/test"


def execute_sql_query(sql_query, params=None):
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            result = session.execute(text(sql_query), params)

            csv_string = io.StringIO()
            csv_writer = csv.writer(csv_string)

            column_headers = result.keys()
            csv_writer.writerow(column_headers)


            for row in result:
                csv_writer.writerow(row)

            csv_data = csv_string.getvalue()
            csv_string.close()
            return csv_data
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return ""

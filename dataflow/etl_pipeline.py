import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions
from datetime import datetime
import csv
import argparse
import logging
import os
import pandas as pd


class CleanTransform(beam.DoFn):
    def process(self, element):
        try:
            row = next(csv.reader([element]))
            (sale_id, sale_date, customer_id, product_id, product_name,
             category, quantity, unit_price, total_price, region) = row

            # Convert date
            try:
                parsed_date = datetime.strptime(sale_date.strip(), "%d-%m-%Y")
                formatted_date = parsed_date.strftime("%Y-%m-%d")
            except Exception:
                formatted_date = None

            # Titlecase & sanitize
            product_name = product_name.strip().title()
            category = category.strip().title()
            region = region.strip().title()

            # Numeric cleanup
            unit_price = abs(round(float(unit_price)))
            quantity = int(quantity)
            total_price = float(quantity * unit_price)

            yield {
                "sale_id": sale_id,
                "sale_date": formatted_date,
                "customer_id": customer_id,
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_price": total_price,
                "region": region
            }

        except Exception as e:
            logging.warning(f"Skipping bad record: {element} — Error: {e}")


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--temp_location', required=True)
    parser.add_argument('--staging_location', required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--region', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--table', required=True)
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Beam pipeline options
    options = PipelineOptions(pipeline_args)
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = known_args.project
    google_cloud_options.region = known_args.region
    google_cloud_options.temp_location = known_args.temp_location

    options.view_as(StandardOptions).runner = "DataflowRunner"

    table_spec = f"{known_args.project}:{known_args.dataset}.{known_args.table}"

    with beam.Pipeline(options=options) as p:
        (p
         | "Read CSV" >> beam.io.ReadFromText(known_args.input, skip_header_lines=1)
         | "Transform" >> beam.ParDo(CleanTransform())
         | "Write BQ" >> beam.io.WriteToBigQuery(
                table=table_spec,
                schema="""
                    sale_id:STRING,
                    sale_date:DATE,
                    customer_id:STRING,
                    product_id:STRING,
                    product_name:STRING,
                    category:STRING,
                    quantity:INTEGER,
                    unit_price:FLOAT,
                    total_price:FLOAT,
                    region:STRING
                """,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
          )
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()

#!/usr/bin/env python3
from subprocess import Popen, PIPE
import csv
import os
import re
import shutil
import sys


if len(sys.argv) != 3:
    print("USAGE: govstack_csv_to_openapi.py <path_to_endpoint_spec.csv> <path_to_schema_spec.csv>")
    sys.exit(1)


class SafeDict(dict):
    """
    https://stackoverflow.com/a/17215533/405682
    """
    def __missing__(self, key):
        return '{' + key + '}'

template = """
openapi: 3.0.0
servers:
  # Added by API Auto Mocking Plugin
  - description: SwaggerHub API Auto Mocking
    url: https://virtserver.swaggerhub.com/GovStack/consent_bb/0.7.0
info:
  description: A basic API reflecting requirements of the Consent BB (WIP)
  version: 0.7.0
  title: Consent Management BB API (WIP)
  contact:
    email: you@your-company.com
  license:
    name: Apache 2.0
    url: 'http://www.apache.org/licenses/LICENSE-2.0.html'
tags:
  - name: admin
    description: Secured Admin-only calls
  - name: org
    description: Secured operations available to organization API integration
  - name: individual
    description: Individual operations
paths:
{paths}

components:
  schemas:
{schemas}
"""

path_spec_template = """
    {method}:
      tags:
        - {tag}
      summary: "{summary}"
      operationId: "{operationId}"
      description: "{description}"
      parameters: {url_parameters}
      responses:
        '200':
          description: "{responseOK}"
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Policy'
        '400':
          description: bad input parameter
"""

path_spec_template_post = path_spec_template + """
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/{request_parameter}'
        description: Insert manually
"""


# See: https://swagger.io/docs/specification/describing-parameters/
parameter_template = """
        - in: {where}
          name: "{name}"
          description: "{description}"
          required: {required}
          schema:
            type: {schema_type}
"""

# See: https://swagger.io/docs/specification/describing-parameters/
parameter_template_schema = """
        - in: {where}
          name: {name}
          description: "{description}"
          required: {required}
          schema:
            $ref: '#/components/schemas/{schema_model}'
"""

schema_template = """
    {schema}:
      type: {schema_type}
      required:
{required}
      properties:
{properties}
"""

schema_property_template = """
        {name}:
          type: {property_type}
          format: "{format}"
          example: "{example}"
          description: "{description}"
"""

schema_property_fk_template = """
        {name}:
          $ref: '#/components/schemas/{fk_model}'
          example: "{example}"
          description: "{description}"
"""


def get_api_spec_from_row(row, current_tag):

    url = row[0]
    method = row[1].lower()
    
    # YAML quotation friendlyness: Use \n as newline characters
    # See: https://stackoverflow.com/questions/3790454/how-do-i-break-a-string-in-yaml-over-multiple-lines
    summary = row[8].replace("\n", "\\n").replace("\"", "\\\"")
    parameters = ""

    pattern_url_parameters = re.compile("{(\w+)}")

    for parameter in pattern_url_parameters.findall(url):
        parameters += parameter_template.format(
            where="path",
            name=parameter,
            required="true",
            schema_type="string",
            description="Unique ID of an object",
        )
    
    for query_parameter in filter(lambda x: bool(x), row[4].split(", ")):
        parameters += parameter_template_schema.format(
            where="query",
            name=query_parameter,
            required="true",
            schema_model=query_parameter,
            description="An object of type {}".format(query_parameter),
        )

    return {
        "url": url,
        "tag": current_tag,
        "method": method,
        "summary": "",
        "operationId": "",
        "description": "",
        "url_parameters": parameters or "[]",
        "request_parameter": "",
        "responseOK": "",
    }


endpoint_csv_file = sys.argv[1]
schema_csv_file = sys.argv[2]

if not os.path.exists(endpoint_csv_file):
    print("File not found: {}".format(endpoint_csv_file))

if not os.path.exists(schema_csv_file):
    print("File not found: {}".format(schema_csv_file))


def is_row_with_api_url(row):
    return "/" in row[0] and row[1]


def is_row_with_api_tag(row):
    return "API tag:" in row[0]

def is_row_with_model_name(row):
    return "Model:" in row[0]

def is_row_with_schema_property(row):
    return not is_row_with_model_name(row) and row[0] and not row[2]

def is_row_with_schema_fk(row):
    return not is_row_with_model_name(row) and row[0] and row[2]


# Build output in this variable
output = ""


#####################################
# PROCESS ENDPOINT CSV              #
#####################################

path_specs = {}

current_tag = None
with open(endpoint_csv_file, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if is_row_with_api_tag(row):
            current_tag = row[0].split(": ")[-1]
        if is_row_with_api_url(row):
        
            api_path = get_api_spec_from_row(row, current_tag)
        
            path = path_spec_template.format(
                **api_path
            )
            if not api_path["url"] in path_specs:
                path_specs[api_path["url"]] = []
            path_specs[api_path["url"]].append(path)

paths_template = """
  {url}:
{path_spec}
"""

paths = {}

for url, path_spec in path_specs.items():
    if not url in paths:
        paths[url] = ""
    paths[url] += ("\n".join(path_spec))

output_paths = ""
for url, path_spec_rendered in paths.items():
    output_paths += paths_template.format(url=url, path_spec=path_spec_rendered)


#####################################
# PROCESS SCHEMA CSV                #
#####################################
models = {}

current_model = None
output_schemas = ""
schema_fields = {}
schema_field_names = {}

with open(schema_csv_file, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if is_row_with_model_name(row):
            current_model = row[0].split(": ")[-1]

        if current_model:
            schema_fields.setdefault(current_model, "")
            schema_field_names.setdefault(current_model, [])

        if current_model and is_row_with_schema_property(row):
            schema_field_names[current_model].append(row[0])
            schema_fields[current_model] += schema_property_template.format(
                name=row[0],
                property_type=row[1],
                format="",
                example="",
                description=row[3],
            )
        elif current_model and is_row_with_schema_fk(row):
            schema_field_names[current_model].append(row[0])
            schema_fields[current_model] += schema_property_fk_template.format(
                name=row[0],
                fk_model=row[2],
                example="",
                description=row[3],
            )
        

for schema_name, properties in schema_fields.items():
    output_schemas += schema_template.format(
        schema=schema_name,
        schema_type="object",
        properties=properties,
        required="\n".join("           - {}".format(name) for name in schema_field_names[schema_name])
    )
    

output = template.format(paths=output_paths, schemas=output_schemas)


print(output)

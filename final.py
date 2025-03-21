import yaml
import json
import argparse
import sys
import os
import jsonschema
from jsonschema import validate, FormatChecker
from jinja2 import Environment, FileSystemLoader


def load_yaml(file_path):
    """Load YAML from a file."""
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def load_json(file_path):
    """Load JSON schema from a file."""
    with open(file_path, "r") as f:
        return json.load(f)

def validate_yaml(yaml_file, schema_file):
    """Validate YAML against JSON Schema."""
    data = load_yaml(yaml_file)
    schema = load_json(schema_file)

    try:
        validate(instance=data, schema=schema, format_checker=FormatChecker())
        print("✅ Validation Passed!")
    except jsonschema.exceptions.ValidationError as e:
        print("🚨 Validation Error!")
        print(f"🔹 Message: {e.message}")
        print(f"🔹 Failed Validator: {e.validator}")
        print(f"🔹 Expected: {e.validator_value}")
        print(f"🔹 Data Path: {list(e.path)}")
        print(f"🔹 Schema Path: {list(e.schema_path)}")
        print("------------------------------------------")
        sys.exit(1)  # Exit the script on validation failure

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a YAML file against a JSON Schema and render Jinja2 template.")
    parser.add_argument("yaml_file", help="Path to the YAML file")
    
    args = parser.parse_args()

    # Check if input YAML file exists
    if not os.path.exists(args.yaml_file):
        print(f"Error: YAML file '{args.yaml_file}' not found.")
        sys.exit(1)

    # Load YAML config
    with open(args.yaml_file, "r") as file:
        config = yaml.safe_load(file)


    # Extract the "name" key for output filename
    service_name = config.get("name")  
    template_name = config.get("template")  

    # Construct filenames based on "template" key
    schema_file = f"schema-{template_name}.json"
    jinja_file = f"template-{template_name}.j2"
    nginx_conf = f"{template_name}-{service_name}.conf"
 
    # Check if required files exist
    if not os.path.exists(schema_file):
        print(f"Error: JSON Schema file '{schema_file}' not found.")
        sys.exit(1)

    if not os.path.exists(jinja_file):
        print(f"Error: Jinja2 template file '{jinja_file}' not found.")
        sys.exit(1)

    # Validate YAML against schema
    validate_yaml(args.yaml_file, schema_file)

    # Load Jinja2 template
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(os.path.abspath(jinja_file))),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(os.path.basename(jinja_file))

    # Render the template
    nginx_config = template.render(nginx=config)

    # Save to output conf file
    with open(nginx_conf, "w") as output_file:
        output_file.write(nginx_config)

    print(f"✅ NGINX configuration successfully generated: {nginx_conf}")

from google import genai
from google.genai import types
from llm_client import get_genai_client
from pydantic import BaseModel, Field
from typing import List, Optional
import dotenv
import json
import os

dotenv.load_dotenv()
class ProductInfo(BaseModel):
    model: Optional[str] = Field(None, description="Product model name")
    manufacturer: Optional[str] = Field(None, description="Manufacturer name")
    address: Optional[str] = Field(None, description="Manufacturer address")
    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    dimensions_mm: Optional[str] = Field(None, description="Dimensions in millimeters (L x W x H)")
    max_efficiency_percent: Optional[float] = Field(None, description="Maximum efficiency percentage")
    max_input_voltage_v: Optional[float] = Field(None, description="Maximum input voltage in volts")
    startup_voltage_v: Optional[float] = Field(None, description="Start-up voltage in volts")
    mppt_trackers: Optional[int] = Field(None, description="Number of MPPT trackers")
    warranty_years: Optional[int] = Field(None, description="Warranty period in years")
    ip_rating: Optional[str] = Field(None, description="IP rating for protection")
    insulation_resistance_protection: Optional[bool] = Field(None, description="Indicates if insulation resistance protection is present")
    Temperature_protection: Optional[bool] = Field(None, description="Indicates if temperature protection is present")
    earth_fault_detection: Optional[bool] = Field(None, description="Indicates if earth fault detection is present")
    remote_software_upload: Optional[bool] = Field(None, description="Indicates if remote software upload is supported")
    cooling_concept: Optional[str] = Field(None, description="Cooling concept used in the product")
    permissible_altitude_m: Optional[float] = Field(None, description="Permissible altitude in meters")
    grid_connection_standards: Optional[List[str]] = Field(None, description="List of grid connection standards the product complies with")
    safety_standards: Optional[List[str]] = Field(None, description="List of safety standards the product complies with")
    rated_output_power_KW: Optional[List[str]] = Field(None, description="List of rated output powers")

def extract_product_info(input_file: str) -> dict:
    """
    Extracts product information from a text file using the Gemini API.

    Args:
        input_file (str): The path to the input text file.
    """
    client = get_genai_client()

    with open(input_file, 'r', encoding='utf-8') as f:
        file_content = f.read()

    prompt = f"""
    Extract all available product specifications from this document in json format.
    If a value is not present, return null.

    Document:

    {file_content}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ProductInfo,
        ),
    )


    return response.parsed.model_dump(exclude_none=True, mode="json") # Return the parsed response as a dictionary, excluding None values.


def save_product_info_to_json(product_info: dict, output_file: str):
    """
    Saves the extracted product information to a JSON file.

    Args:
        product_info (dict): The extracted product information.
        output_file (str): The path to the output JSON file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(product_info, f, indent=4, ensure_ascii=False)


def extract_and_save_product_info(input_file: str, output_file: str):
    """
    Extracts product information from a text file and saves it to a JSON file.

    Args:
        input_file (str): The path to the input text file.
        output_file (str): The path to the output JSON file.
    """
    product_info = extract_product_info(input_file)
    save_product_info_to_json(product_info, output_file)
    print(f"Extracted product information from {input_file} saved to {output_file}")

def extract_fields(text_paths: List[str], output_dir: str) -> List[str]:
    """
    Loops through all text paths, extracts product information, and saves it to the output directory.

    Args:
        text_paths (str): The list of text paths.
        output_dir (str): The directory where extracted JSON files will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extracted_paths = []
    for i, txt_path in enumerate(text_paths, start=1):
        output_path = os.path.join(output_dir, f"product_info_{i}.json")
        extract_and_save_product_info(txt_path, output_path)
        extracted_paths.append(output_path)

    return extracted_paths

if __name__ == "__main__":
    extract_fields(["data/processed/parsed_text_1.txt","data/processed/parsed_text_2.txt"], "outputs/extracted")






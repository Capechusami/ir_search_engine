import os
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_clinical_study(xml_path, txt_output_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing {xml_path}: {e}")
        return

    def get_text(tag):
        elem = root.find(tag)
        return elem.text.strip() if elem is not None and elem.text else "N/A"

    def get_nested_text(parent, tag):
        elem = parent.find(tag)
        return elem.text.strip() if elem is not None and elem.text else "N/A"

    data = []

    # Basic Info
    data.append(f"Brief Title: {get_text('brief_title')}")
    data.append(f"Official Title: {get_text('official_title')}")
    data.append(f"Study Type: {get_text('study_type')}")
    data.append(f"Status: {get_text('overall_status')}")
    data.append(f"Start Date: {get_text('start_date')}")
    data.append(f"Completion Date: {get_text('completion_date')}")

    # Sponsor
    sponsor = root.find("sponsors/lead_sponsor")
    if sponsor is not None:
        agency = get_nested_text(sponsor, "agency")
        data.append(f"Sponsor: {agency}")

    # Summary & Description
    summary = root.find("brief_summary/textblock")
    if summary is not None:
        data.append(f"\nSummary:\n{summary.text.strip()}")

    description = root.find("detailed_description/textblock")
    if description is not None:
        data.append(f"\nDetailed Description:\n{description.text.strip()}")

    # Outcomes
    def extract_outcome(tag):
        outcomes = root.findall(tag)
        for i, outcome in enumerate(outcomes, 1):
            measure = get_nested_text(outcome, "measure")
            timeframe = get_nested_text(outcome, "time_frame")
            description = get_nested_text(outcome, "description")
            data.append(f"\n{tag.replace('_', ' ').title()} {i}:")
            data.append(f"  Measure: {measure}")
            data.append(f"  Time Frame: {timeframe}")
            data.append(f"  Description: {description}")

    extract_outcome("primary_outcome")
    extract_outcome("secondary_outcome")

    # Eligibility
    eligibility = root.find("eligibility/criteria/textblock")
    if eligibility is not None:
        data.append(f"\nEligibility Criteria:\n{eligibility.text.strip()}")

    min_age = get_text("eligibility/minimum_age")
    max_age = get_text("eligibility/maximum_age")
    gender = get_text("eligibility/gender")
    data.append(f"Age Range: {min_age} to {max_age}")
    data.append(f"Gender: {gender}")

    # Contacts
    contact = root.find("overall_contact")
    if contact is not None:
        name = get_nested_text(contact, "last_name")
        phone = get_nested_text(contact, "phone")
        email = get_nested_text(contact, "email")
        data.append(f"\nContact:\n  Name: {name}\n  Phone: {phone}\n  Email: {email}")

    # Write to file
    try:
        with open(txt_output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(data))
        print(f"Saved: {txt_output_path}")
    except Exception as e:
        print(f"Error writing to {txt_output_path}: {e}")

# === Main script: Process all XMLs in documents ===
def process_all_documents_xml():
    documents_folder = Path.home() / "documents"
    output_folder = documents_folder / "Parsed_Clinical_Trials"
    output_folder.mkdir(exist_ok=True)

    xml_files = list(documents_folder.glob("*.xml"))

    if not xml_files:
        print("No XML files found in documents folder.")
        return

    for xml_file in xml_files:
        output_file = output_folder / f"{xml_file.stem}_parsed.txt"
        try:
            parse_clinical_study(xml_file, output_file)
        except Exception as e:
            print(f"Error processing {xml_file.name}: {e}")

# Run it
if __name__ == "__main__":
    process_all_documents_xml()

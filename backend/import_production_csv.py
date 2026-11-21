"""Import production metadata from a CSV file into the database.

Expected CSV columns:
qid,name,kind,year,end_year,years,relation,source_work,source_work_wikipedia,
series,sitelinks,located_places,place_slugs,wiki_places,wiki_place_slugs,
wiki_evidence_url,wiki_evidence_source,countries_only,countries_only_per_wikipedia,
description,wikipedia,wikidata,url,verified_places,verified_place_slugs,verified_source_urls

The qid in this CSV matches the qid of an existing Location. The name column
is the production name, which matches an existing Production's name.
The year, end_year, relation, and wikipedia fields are stored in a new
ProductionInfo table linked to the Production.

Uses the same mojibake fix and encoding detection as import_csv.py.
"""
import csv
import os
import sys
from app import create_app
from database import db
from models.location import Location, Production, ProductionInfo

# Reuse the mojibake fix and encoding detection from import_csv.py
from import_csv import fix_cp1252_mojibake, detect_encoding


def safe_int(value):
    """Convert a value to int, returning None if empty or invalid."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def safe_str(value):
    """Return a stripped string with mojibake fixed, or None if empty."""
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    s = fix_cp1252_mojibake(s)
    return s


def import_production_csv(csv_path):
    """Import production metadata from a CSV file into the database.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        Tuple of (imported_count, skipped_count, error_count).
    """
    app = create_app()

    with app.app_context():
        if not os.path.exists(csv_path):
            print(f"Error: CSV file not found: {csv_path}")
            return 0, 0, 0

        imported = 0
        skipped = 0
        errors = 0

        # Auto-detect file encoding
        file_encoding = detect_encoding(csv_path)
        print(f"Detected CSV encoding: {file_encoding}")

        with open(csv_path, "r", encoding=file_encoding) as f:
            reader = csv.DictReader(f)

            # Validate required columns
            required = ["qid", "name"]
            missing = [col for col in required if col not in (reader.fieldnames or [])]
            if missing:
                print(f"Error: Missing required columns: {missing}")
                return 0, 0, 0

            for row_num, row in enumerate(reader, start=2):
                try:
                    qid = safe_str(row.get("qid"))
                    prod_name = safe_str(row.get("name"))

                    # Skip rows without essential data
                    if not qid or not prod_name:
                        skipped += 1
                        continue

                    # Find the location by qid
                    location = Location.query.filter_by(qid=qid).first()
                    if not location:
                        skipped += 1
                        print(f"  Row {row_num}: No location found for qid={qid}, skipping.")
                        continue

                    # Find or create the production by name
                    production = Production.query.filter_by(name=prod_name).first()
                    if not production:
                        production = Production(name=prod_name)
                        db.session.add(production)
                        db.session.flush()

                    # Check if production_info already exists for this production with the same year
                    year = safe_int(row.get("year"))
                    end_year = safe_int(row.get("end_year"))
                    relation = safe_str(row.get("relation"))
                    wikipedia = safe_str(row.get("wikipedia"))

                    # Skip if all fields are empty
                    if year is None and end_year is None and relation is None and wikipedia is None:
                        skipped += 1
                        continue

                    # Check for duplicate: same production + same year
                    existing_info = ProductionInfo.query.filter_by(
                        production_id=production.id, year=year
                    ).first()
                    if existing_info:
                        skipped += 1
                        continue

                    # Create the production info record
                    prod_info = ProductionInfo(
                        production_id=production.id,
                        year=year,
                        end_year=end_year,
                        relation=relation,
                        wikipedia=wikipedia,
                    )
                    db.session.add(prod_info)

                    # Also ensure the production is linked to the location if not already
                    existing_link = db.session.query(LocationProduction).filter_by(
                        location_id=location.id, production_id=production.id
                    ).first()
                    if not existing_link:
                        from models.location import LocationProduction
                        lp = LocationProduction(
                            location_id=location.id,
                            production_id=production.id,
                            production_source="production_csv",
                        )
                        db.session.add(lp)

                    db.session.commit()
                    imported += 1

                except Exception as e:
                    errors += 1
                    print(f"  Error on row {row_num}: {e}")
                    db.session.rollback()

        print(f"Import complete: {imported} imported, {skipped} skipped, {errors} errors.")
        return imported, skipped, errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_production_csv.py <path_to_csv>")
        print("")
        print("Imports production metadata (year, end_year, relation, wikipedia)")
        print("from a CSV file into the database, linking to existing productions by qid.")
        sys.exit(1)

    csv_path = sys.argv[1]

    print(f"Importing production metadata from: {csv_path}")
    imported, skipped, errors = import_production_csv(csv_path)
    print(f"Summary: {imported} production info records imported, {skipped} skipped, {errors} errors.")

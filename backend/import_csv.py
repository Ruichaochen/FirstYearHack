"""Import locations from a CSV file into the database.

Expected CSV columns:
qid,name,category,category_label,resolution,latitude,longitude,country,iso,
fame_rank,fame_tier,productions,wiki_productions,modelled_for,top_modelled,
set_only,top_productions,description,wikipedia,wikidata,image,image_page,url,
image_by,image_licence,image_licence_url,verified_productions,top_verified

The semi-colon separated fields (top_modelled, top_productions, verified_productions,
top_verified, productions) are split into individual Production records linked via
a many-to-many relationship table.
"""
import csv
import os
import sys
from app import create_app
from database import db
from models.location import Location, Production, LocationProduction


# Reverse mapping for CP1252 mojibake: when UTF-8 bytes are misread as CP1252,
# specific byte values (0x80-0x9F) map to specific Unicode code points.
# This map reverses that so we can recover the original UTF-8 bytes.
_CP1252_MOJIBAKE_MAP = {
    0x20AC: 0x80,  # Euro sign
    0x201A: 0x82,  # Single low-9 quotation mark
    0x0192: 0x83,  # Latin small f with hook
    0x201E: 0x84,  # Double low-9 quotation mark
    0x2026: 0x85,  # Horizontal ellipsis
    0x2020: 0x86,  # Dagger
    0x2021: 0x87,  # Double dagger
    0x02C6: 0x88,  # Modifier letter circumflex
    0x2039: 0x89,  # Single left-pointing angle quotation
    0x0160: 0x8A,  # Latin capital S with caron
    0x203A: 0x8B,  # Single right-pointing angle quotation
    0x0152: 0x8C,  # Latin capital OE
    0x017D: 0x8E,  # Latin capital Z with caron
    0x2018: 0x91,  # Left single quotation mark
    0x2019: 0x92,  # Right single quotation mark
    0x201C: 0x93,  # Left double quotation mark
    0x201D: 0x94,  # Right double quotation mark
    0x2022: 0x95,  # Bullet
    0x2013: 0x96,  # En dash
    0x2014: 0x97,  # Em dash
    0x02DC: 0x98,  # Small tilde
    0x2122: 0x99,  # Trade mark sign
    0x0161: 0x9A,  # Latin small s with caron
    0x0153: 0x9C,  # Latin small oe
    0x017E: 0x9E,  # Latin small z with caron
    0x0178: 0x9F,  # Latin capital y with diaeresis
}


def fix_cp1252_mojibake(text):
    """Fix text corrupted by reading UTF-8 bytes as CP1252.

    When a UTF-8 file is opened with CP1252 encoding, bytes in the 0x80-0x9F range
    are mapped to special Unicode code points (e.g., 0x96 becomes U+2013 en-dash,
    but 0x80 becomes U+20AC euro sign). This function detects and reverses that
    corruption by mapping those code points back to their original byte values,
    then decoding the recovered bytes as UTF-8.

    Returns the original text unchanged if no mojibake pattern is found.
    """
    if not text:
        return text

    bytes_list = []
    has_mojibake = False
    for char in text:
        code = ord(char)
        if code in _CP1252_MOJIBAKE_MAP:
            bytes_list.append(_CP1252_MOJIBAKE_MAP[code])
            has_mojibake = True
        elif code < 128:
            bytes_list.append(code)
        elif code < 256:
            # Regular Latin-1 character, keep as single byte
            bytes_list.append(code)
        else:
            # Character outside the CP1252 range — not a mojibake pattern
            return text

    if not has_mojibake:
        return text

    # Try to decode the recovered bytes as UTF-8
    try:
        fixed = bytes(bytes_list).decode("utf-8")
        # Only return the fixed version if it's different (i.e., we actually fixed something)
        return fixed if fixed != text else text
    except UnicodeDecodeError:
        return text


def detect_encoding(file_path):
    """Detect the encoding of a CSV file by trying common encodings.

    Returns the first encoding that successfully reads the file without errors.
    Prioritizes UTF-8, then falls back to Windows-1252 (common for Windows-created CSVs).
    """
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                f.read()
            return encoding
        except (UnicodeDecodeError, LookupError):
            continue
    return "utf-8"  # Final fallback


def parse_semicolon_field(value):
    """Split a semi-colon separated field into a list of non-empty, stripped strings.

    Filters out numeric-only values (e.g., "0" from verified_productions counts)
    that should not be treated as production names. Also fixes CP1252 mojibake
    in each production name.
    """
    if not value or not value.strip():
        return []
    return [
        fix_cp1252_mojibake(item.strip())
        for item in value.split(";")
        if item.strip() and not item.strip().isdigit()
    ]


def safe_int(value):
    """Convert a value to int, returning None if empty or invalid."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def safe_float(value):
    """Convert a value to float, returning None if empty or invalid."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def safe_str(value):
    """Return a stripped string with mojibake fixed, or None if empty."""
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    # Fix CP1252 mojibake that may have been introduced during CSV reading
    s = fix_cp1252_mojibake(s)
    return s


def import_csv(csv_path, clear_existing=False):
    """Import locations from a CSV file into the database.

    Args:
        csv_path: Path to the CSV file.
        clear_existing: If True, delete all existing locations and productions first.

    Returns:
        Tuple of (imported_count, skipped_count, error_count).
    """
    app = create_app()

    with app.app_context():
        if clear_existing:
            # Clear in correct order to respect foreign keys
            LocationProduction.query.delete()
            Production.query.delete()
            Location.query.delete()
            db.session.commit()
            print("Cleared existing data.")

        if not os.path.exists(csv_path):
            print(f"Error: CSV file not found: {csv_path}")
            return 0, 0, 0

        imported = 0
        skipped = 0
        errors = 0

        # Auto-detect file encoding to handle Windows-1252, UTF-8, etc.
        file_encoding = detect_encoding(csv_path)
        print(f"Detected CSV encoding: {file_encoding}")

        with open(csv_path, "r", encoding=file_encoding) as f:
            reader = csv.DictReader(f)

            # Validate required columns
            required = ["name", "latitude", "longitude"]
            missing = [col for col in required if col not in (reader.fieldnames or [])]
            if missing:
                print(f"Error: Missing required columns: {missing}")
                return 0, 0, 0

            for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                try:
                    name = safe_str(row.get("name"))
                    latitude = safe_float(row.get("latitude"))
                    longitude = safe_float(row.get("longitude"))

                    # Skip rows without essential data
                    if not name or latitude is None or longitude is None:
                        skipped += 1
                        continue

                    # Check if location already exists (by qid or name + coords)
                    qid = safe_str(row.get("qid"))
                    existing = None
                    if qid:
                        existing = Location.query.filter_by(qid=qid).first()
                    if not existing:
                        existing = Location.query.filter_by(
                            name=name, latitude=latitude, longitude=longitude
                        ).first()

                    if existing:
                        skipped += 1
                        continue

                    # Create the location
                    location = Location(
                        qid=qid,
                        name=name,
                        category=safe_str(row.get("category")) or "film",
                        category_label=safe_str(row.get("category_label")),
                        description=safe_str(row.get("description")),
                        latitude=latitude,
                        longitude=longitude,
                        country=safe_str(row.get("country")),
                        iso=safe_str(row.get("iso")),
                        resolution=safe_str(row.get("resolution")),
                        fame_rank=safe_int(row.get("fame_rank")),
                        fame_tier=safe_str(row.get("fame_tier")),
                        wiki_productions=safe_int(row.get("wiki_productions")),
                        modelled_for=safe_int(row.get("modelled_for")),
                        wikipedia=safe_str(row.get("wikipedia")),
                        wikidata=safe_str(row.get("wikidata")),
                        image=safe_str(row.get("image")),
                        image_page=safe_str(row.get("image_page")),
                        image_by=safe_str(row.get("image_by")),
                        image_licence=safe_str(row.get("image_licence")),
                        image_licence_url=safe_str(row.get("image_licence_url")),
                        url=safe_str(row.get("url")),
                        media_url=safe_str(row.get("image")),  # Map image to legacy media_url
                    )

                    db.session.add(location)
                    db.session.flush()  # Get the location ID

                    # Parse and create Production records for semi-colon separated fields
                    production_fields = [
                        "top_modelled",
                        "top_productions",
                        "verified_productions",
                        "top_verified",
                    ]

                    production_names_added = set()
                    for field in production_fields:
                        raw_value = row.get(field)
                        items = parse_semicolon_field(raw_value)
                        for item in items:
                            # Normalize name to avoid duplicates within this location
                            normalized = item.strip().lower()
                            if normalized in production_names_added:
                                continue
                            production_names_added.add(normalized)

                            # Check if production already exists
                            production = Production.query.filter_by(name=item).first()
                            if not production:
                                production = Production(name=item)
                                db.session.add(production)
                                db.session.flush()

                            # Link production to location via the association object
                            lp = LocationProduction(
                                location_id=location.id,
                                production_id=production.id,
                                production_source=field,
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


def fix_database_mojibake():
    """Scan and fix all corrupted strings in the database.

    Fixes CP1252 mojibake in both the locations and productions tables.
    """
    app = create_app()

    with app.app_context():
        fixed_count = 0

        # Fix locations
        for location in Location.query.all():
            fields_to_fix = [
                "name", "description", "category", "category_label",
                "country", "iso", "resolution", "fame_tier",
                "wikipedia", "wikidata", "image", "image_page",
                "image_by", "image_licence", "image_licence_url", "url", "media_url"
            ]
            for field in fields_to_fix:
                old_value = getattr(location, field)
                if old_value:
                    new_value = fix_cp1252_mojibake(old_value)
                    if new_value != old_value:
                        setattr(location, field, new_value)
                        fixed_count += 1
                        print(f"  Fixed Location {location.id} ({field}): {repr(old_value[:50])} -> {repr(new_value[:50])}")

        # Fix productions
        for production in Production.query.all():
            old_name = production.name
            if old_name:
                new_name = fix_cp1252_mojibake(old_name)
                if new_name != old_name:
                    production.name = new_name
                    fixed_count += 1
                    print(f"  Fixed Production {production.id}: {repr(old_name[:50])} -> {repr(new_name[:50])}")

        if fixed_count:
            db.session.commit()
            print(f"Fixed {fixed_count} corrupted strings in the database.")
        else:
            print("No corrupted strings found.")

        return fixed_count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_csv.py <path_to_csv> [--clear]")
        print("       python import_csv.py --fix-mojibake")
        print("")
        print("Imports locations from a CSV file into the database.")
        print("Add --clear to delete existing data before importing.")
        print("Use --fix-mojibake to fix corrupted UTF-8 characters in the database.")
        sys.exit(1)

    if sys.argv[1] == "--fix-mojibake":
        print("Fixing CP1252 mojibake in the database...")
        fixed = fix_database_mojibake()
        print(f"Summary: {fixed} strings fixed.")
        sys.exit(0)

    csv_path = sys.argv[1]
    clear = "--clear" in sys.argv

    print(f"Importing from: {csv_path}")
    if clear:
        print("Clearing existing data...")


    imported, skipped, errors = import_csv(csv_path, clear_existing=clear)
    print(f"Summary: {imported} locations imported, {skipped} skipped, {errors} errors.")

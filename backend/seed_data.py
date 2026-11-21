# -*- coding: utf-8 -*-
"""Seed the database with curated London cultural locations."""
import json
import os
from app import create_app
from database import db
from models.location import Location, Production, LocationProduction

LOCATIONS_DATA = [
    # FILM locations
    {
        "name": "Tower Bridge",
        "description": "Iconic London bridge featured in numerous films including James Bond's 'Die Another Day' (2002) and 'The Mummy Returns' (2001). One of London's most recognizable landmarks spanning the River Thames.",
        "category": "film",
        "latitude": 51.5055,
        "longitude": -0.0873,
        "address": "Tower Bridge Rd, London SE1 2UP",
        "media_url": None,
        "year": 2002,
    },
    {
        "name": "Leadenhall Market",
        "description": "Victorian covered market that served as a filming location for Diagon Alley in the Harry Potter films. Its ornate iron and glass roof creates a magical atmosphere.",
        "category": "film",
        "latitude": 51.5134,
        "longitude": -0.0860,
        "address": "Gracechurch St, City of London, London EC3V 0LR",
        "media_url": None,
        "year": 2001,
    },
    {
        "name": "Paddington Station",
        "description": "Featured in the Paddington film series (2014, 2017), this grand Victorian railway station is where the beloved bear arrives in London. Also appears in 'The Imitation Game' and 'Skyfall'.",
        "category": "film",
        "latitude": 51.5167,
        "longitude": -0.1752,
        "address": "Paddington Stn, London W2 1HW",
        "media_url": None,
        "year": 2014,
    },
    {
        "name": "The London Eye",
        "description": "Featured prominently in 'Die Another Day' (2002) during the climactic spinning beds scene. This giant observation wheel on the South Bank has since appeared in many films set in London.",
        "category": "film",
        "latitude": 51.5033,
        "longitude": -0.1195,
        "address": "Riverside Building, County Hall, London SE1 7PB",
        "media_url": None,
        "year": 2002,
    },
    {
        "name": "Buckingham Palace",
        "description": "The official residence of the British monarch, featured in 'The Queen' (2006), 'The King's Speech' (2010), and 'Dunkirk' (2017). The Changing of the Guard ceremony is a iconic London scene.",
        "category": "film",
        "latitude": 51.5014,
        "longitude": -0.1419,
        "address": "London SW1A 1AA",
        "media_url": None,
        "year": 2006,
    },
    {
        "name": "Piccadilly Circus",
        "description": "Famous traffic junction and entertainment hub featured in 'Notting Hill' (1999), 'Skyfall' (2012), and 'Quantum of Solace' (2008). The bright digital billboards make it instantly recognizable.",
        "category": "film",
        "latitude": 51.5100,
        "longitude": -0.1342,
        "address": "Piccadilly Circus, London W1J 9HS",
        "media_url": None,
        "year": 1999,
    },
    {
        "name": "Covent Garden",
        "description": "Historic market area featured in 'Notting Hill' (1999) and 'The Avengers' (1998). The Piazza and surrounding streets provide a quintessential London backdrop for street performers and shops.",
        "category": "film",
        "latitude": 51.5118,
        "longitude": -0.1226,
        "address": "Covent Garden, London WC2E 8RF",
        "media_url": None,
        "year": 1999,
    },
    {
        "name": "Southwark Bridge",
        "description": "Filming location for the opening scene of 'V for Vendetta' (2005) where Evey Hammond is arrested. The bridge connects the South Bank with the City of London.",
        "category": "film",
        "latitude": 51.5068,
        "longitude": -0.0902,
        "address": "Southwark Bridge, London SE1 9PP",
        "media_url": None,
        "year": 2005,
    },
    {
        "name": "Millennium Bridge",
        "description": "The wobbly pedestrian bridge made famous by 'Harry Potter and the Order of the Phoenix' (2007) where the Dementor attack scene was filmed. Connects the Tate Modern with St Paul's Cathedral.",
        "category": "film",
        "latitude": 51.5098,
        "longitude": -0.0985,
        "address": "Millennium Bridge, London SE1 9AG",
        "media_url": None,
        "year": 2007,
    },
    {
        "name": "The Shard",
        "description": "London's tallest building, featured in 'Mission: Impossible – Ghost Protocol' (2011) and 'Fantastic Beasts: The Crimes of Grindelwald' (2018). Offers panoramic views of the city.",
        "category": "film",
        "latitude": 51.5045,
        "longitude": -0.0865,
        "address": "32 London Bridge St, London SE1 9SG",
        "media_url": None,
        "year": 2011,
    },
    # MUSIC locations
    {
        "name": "Royal Albert Hall",
        "description": "Iconic circular concert hall that hosts the annual Proms classical music series. Home to countless legendary performances from The Rolling Stones to Andrea Bocelli.",
        "category": "music",
        "latitude": 51.5009,
        "longitude": -0.1773,
        "address": "Kensington Gore, London SW7 2AP",
        "media_url": None,
        "year": 1871,
    },
    {
        "name": "Wembley Stadium",
        "description": "One of the world's most famous stadiums, hosting legendary concerts by The Beatles, Queen, Coldplay, and Ed Sheeran. The iconic arch is a London landmark visible from miles away.",
        "category": "music",
        "latitude": 51.5560,
        "longitude": -0.2795,
        "address": "Wembley, London HA9 0WS",
        "media_url": None,
        "year": 2007,
    },
    {
        "name": "Hammersmith Apollo (O2 Shepherds Bush Empire)",
        "description": "Legendary music venue where The Beatles, Pink Floyd, and Nirvana all performed. David Bowie's final tour ended here in 2006. A cornerstone of London's live music scene.",
        "category": "music",
        "latitude": 51.4966,
        "longitude": -0.2228,
        "address": "Shepherds Bush Green, London W12 7DJ",
        "media_url": None,
        "year": 1931,
    },
    {
        "name": "Roundhouse",
        "description": "Former railway engine house turned iconic music venue in Camden. Hosted The Who, Jimi Hendrix, and David Bowie. Known for its unique circular stage and avant-garde performances.",
        "category": "music",
        "latitude": 51.5432,
        "longitude": -0.1518,
        "address": "Chalk Farm Rd, London NW1 8EH",
        "media_url": None,
        "year": 1964,
    },
    {
        "name": "Kilburn Studio (Abbey Road Studios)",
        "description": "The world-famous recording studio where The Beatles recorded most of their albums. 'Abbey Road' remains one of the best-selling albums of all time. Open to visitors by tour.",
        "category": "music",
        "latitude": 51.5318,
        "longitude": -0.1780,
        "address": "3 Abbey Rd, St John's Wood, London NW8 9AY",
        "media_url": None,
        "year": 1962,
    },
    {
        "name": "Brixton Academy (O2 Academy Brixton)",
        "description": "Historic music venue in South London that has hosted Arctic Monkeys, Adele, and The 1975. Known for its intimate atmosphere and vibrant South London music culture.",
        "category": "music",
        "latitude": 51.4613,
        "longitude": -0.1150,
        "address": "211 Stockwell Rd, London SW9 9SL",
        "media_url": None,
        "year": 1872,
    },
    {
        "name": "Camden Market",
        "description": "Birthplace of the punk movement and home to the legendary Camden Palace where The Sex Pistols performed. Now a vibrant market area that remains central to London's alternative music scene.",
        "category": "music",
        "latitude": 51.5423,
        "longitude": -0.1440,
        "address": "Camden Lock Pl, London NW1 8AF",
        "media_url": None,
        "year": 1976,
    },
    {
        "name": "Royal Festival Hall",
        "description": "South Bank venue that hosted the first Monty Python live show and countless jazz, classical, and pop concerts. Part of the Southbank Centre, it was built for the 1951 Festival of Britain.",
        "category": "music",
        "latitude": 51.5010,
        "longitude": -0.1165,
        "address": "Belvedere Rd, London SE1 8XX",
        "media_url": None,
        "year": 1951,
    },
    # LITERATURE locations
    {
        "name": "The British Library",
        "description": "Home to the Magna Carta, Darwin's original notebooks, and Shakespeare's First Folio. The largest library in the world, containing over 150 million items from across human history.",
        "category": "literature",
        "latitude": 51.5299,
        "longitude": -0.1274,
        "address": "96 Euston Rd, London NW1 2DB",
        "media_url": None,
        "year": 1973,
    },
    {
        "name": "Charles Dickens Museum",
        "description": "The former home of Charles Dickens at Doughty Street where he wrote 'Oliver Twist' and 'Nicholas Nickleby'. The museum preserves his writing desk and personal belongings.",
        "category": "literature",
        "latitude": 51.5235,
        "longitude": -0.1366,
        "address": "48 Doughty St, London WC1N 2LX",
        "media_url": None,
        "year": 1837,
    },
    {
        "name": "The Shakespeare Globe",
        "description": "Modern reconstruction of the original Globe Theatre where Shakespeare's plays were performed. Open-air theatre on the South Bank that stages Shakespeare's works using original performance practices.",
        "category": "literature",
        "latitude": 51.5081,
        "longitude": -0.0972,
        "address": "21 New Globe Walk, London SE1 9DT",
        "media_url": None,
        "year": 1997,
    },
    {
        "name": "The Harry Potter Studio Tour (Warner Bros)",
        "description": "While located just outside London in Leavesden, this attraction preserves original sets, props, and costumes from all eight Harry Potter films. J.K. Rowling wrote the books while living in London.",
        "category": "literature",
        "latitude": 51.5260,
        "longitude": -0.2670,
        "address": "Studio Tour, Warner Village, Leavesden WD25 7LH",
        "media_url": None,
        "year": 2000,
    },
    {
        "name": "Agatha Christie House",
        "description": "The former home of Agatha Christie in Wallingford where she wrote many of her famous detective novels including 'Murder on the Orient Express'. Now a museum dedicated to the Queen of Crime.",
        "category": "literature",
        "latitude": 51.5150,
        "longitude": -0.1400,
        "address": "London",
        "media_url": None,
        "year": 1920,
    },
    {
        "name": "The George Tavern",
        "description": "Historic pub near the Tower of London where Charles Dickens is said to have written parts of 'A Tale of Two Cities'. The tavern dates back to 1780 and retains much of its original character.",
        "category": "literature",
        "latitude": 51.5055,
        "longitude": -0.0720,
        "address": "98 Commercial Rd, London E1 6LP",
        "media_url": None,
        "year": 1859,
    },
    {
        "name": "Bloomsbury",
        "description": "The historic London district home to the Bloomsbury Group, including Virginia Woolf, E.M. Forster, and John Maynard Keynes. The area around Russell Square was their intellectual hub.",
        "category": "literature",
        "latitude": 51.5225,
        "longitude": -0.1248,
        "address": "Russell Square, London WC1B",
        "media_url": None,
        "year": 1905,
    },
    # TV locations
    {
        "name": "Sky Garden",
        "description": "Popular filming location for numerous TV shows including 'Sherlock' and 'Doctor Who'. This public garden on the 35th floor of 20 Fenchurch Street offers stunning views of London.",
        "category": "tv",
        "latitude": 51.5118,
        "longitude": -0.0830,
        "address": "1 Sky Garden, 20 Fenchurch St, London EC3M 8BB",
        "media_url": None,
        "year": 2014,
    },
    {
        "name": "Tate Modern",
        "description": "Contemporary art gallery housed in the former Bankside Power Station. Featured in 'Sherlock' and 'The IT Crowd'. The Turbine Hall hosts large-scale art installations.",
        "category": "tv",
        "latitude": 51.5076,
        "longitude": -0.0994,
        "address": "Bankside, London SE1 9TG",
        "media_url": None,
        "year": 2000,
    },
    {
        "name": "St Pancras Station",
        "description": "Gothic Revival railway station featured in 'The Night Manager' and 'Pride & Prejudice'. The magnificent bar and clock tower make it one of London's most photogenic locations.",
        "category": "tv",
        "latitude": 51.5321,
        "longitude": -0.1250,
        "address": "Euston Rd, London NW1 2AR",
        "media_url": None,
        "year": 2016,
    },
    {
        "name": "The British Museum",
        "description": "World-famous museum featured in 'Sherlock' and 'The Mummy' TV series. Houses the Rosetta Stone, Egyptian mummies, and the Elgin Marbles among 8 million other objects.",
        "category": "tv",
        "latitude": 51.5194,
        "longitude": -0.1270,
        "address": "Great Russell St, London WC1B 3DG",
        "media_url": None,
        "year": 2010,
    },
    {
        "name": "Tower of London",
        "description": "Historic castle featured in 'Poldark', 'Victoria', and 'The Crown'. Home to the Crown Jewels and over a thousand years of British history. The ravens are said to protect the Tower.",
        "category": "tv",
        "latitude": 51.5081,
        "longitude": -0.0759,
        "address": "St Katharine's & Wapping, London EC3N 4AB",
        "media_url": None,
        "year": 2015,
    },
    {
        "name": "Westminster Abbey",
        "description": "Gothic abbey church where British monarchs are crowned and married. Featured in 'The Crown' and 'Downton Abbey'. Burial place of poets, scientists, and royalty.",
        "category": "tv",
        "latitude": 51.4994,
        "longitude": -0.1273,
        "address": "20 Deans Yd, London SW1P 3PA",
        "media_url": None,
        "year": 2016,
    },
    # THEATRE locations
    {
        "name": "Theatre Royal, Drury Lane",
        "description": "One of London's oldest and most famous theatres, dating back to 1663. Located in the heart of the West End, it has hosted premieres of works by Shakespeare, Gilbert & Sullivan, and Andrew Lloyd Webber.",
        "category": "theatre",
        "latitude": 51.5129,
        "longitude": -0.1203,
        "address": "Catherine St, London WC2B 5JF",
        "media_url": None,
        "year": 1663,
    },
    {
        "name": "The National Theatre",
        "description": "Iconic South Bank venue known for groundbreaking productions. The distinctive brutalist building houses three stages and is free to wander, with paid tickets for performances.",
        "category": "theatre",
        "latitude": 51.5076,
        "longitude": -0.1150,
        "address": "South Bank Rd, London SE1 9PX",
        "media_url": None,
        "year": 1976,
    },
    {
        "name": "Lyceum Theatre",
        "description": "Home to 'The Lion King' musical since 1999, the longest-running show in West End history. The theatre itself dates back to 1834 and was originally designed by Charles Barry.",
        "category": "theatre",
        "latitude": 51.5110,
        "longitude": -0.1204,
        "address": "21 Wellington St, London WC2E 7RQ",
        "media_url": None,
        "year": 1999,
    },
    {
        "name": "The Old Vic",
        "description": "Historic theatre in Borough known for its commitment to classical and contemporary drama. Home to the Old Vic Theatre School, it has trained generations of British actors.",
        "category": "theatre",
        "latitude": 51.5013,
        "longitude": -0.1073,
        "address": "The Cut, London SE1 8NB",
        "media_url": None,
        "year": 1818,
    },
    {
        "name": "Prince Edward Theatre",
        "description": "West End theatre currently home to 'The Phantom of the Opera', Andrew Lloyd Webber's longest-running musical. The theatre opened in 1891 and has been a cornerstone of London's theatrical landscape.",
        "category": "theatre",
        "latitude": 51.5100,
        "longitude": -0.1280,
        "address": "Old Compton St, London W1D 4HS",
        "media_url": None,
        "year": 1986,
    },
    {
        "name": "The Royal Court Theatre",
        "description": "London's leading writers' theatre, known for premiering new British plays. Located in Sloane Square, it has a reputation for launching the careers of playwrights like Harold Pinter and Caryl Churchill.",
        "category": "theatre",
        "latitude": 51.4920,
        "longitude": -0.1560,
        "address": "50 Sloane Square, London SW1W 8DT",
        "media_url": None,
        "year": 1952,
    },
]


# Reverse mapping for CP1252 mojibake
_CP1252_MOJIBAKE_MAP = {
    0x20AC: 0x80, 0x201A: 0x82, 0x0192: 0x83, 0x201E: 0x84,
    0x2026: 0x85, 0x2020: 0x86, 0x2021: 0x87, 0x02C6: 0x88,
    0x2039: 0x89, 0x0160: 0x8A, 0x203A: 0x8B, 0x0152: 0x8C,
    0x017D: 0x8E, 0x2018: 0x91, 0x2019: 0x92, 0x201C: 0x93,
    0x201D: 0x94, 0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97,
    0x02DC: 0x98, 0x2122: 0x99, 0x0161: 0x9A, 0x0153: 0x9C,
    0x017E: 0x9E, 0x0178: 0x9F,
}


def fix_cp1252_mojibake(text):
    """Fix text corrupted by reading UTF-8 bytes as CP1252."""
    if not text:
        return text
    bytes_list = []
    has_mojibake = False
    for char in text:
        code = ord(char)
        if code in _CP1252_MOJIBAKE_MAP:
            bytes_list.append(_CP1252_MOJIBAKE_MAP[code])
            has_mojibake = True
        elif code < 256:
            bytes_list.append(code)
        else:
            return text
    if not has_mojibake:
        return text
    try:
        fixed = bytes(bytes_list).decode("utf-8")
        return fixed if fixed != text else text
    except UnicodeDecodeError:
        return text


def parse_semicolon_field(value):
    """Split a semi-colon separated field into a list of non-empty, stripped strings.

    Filters out numeric-only values (e.g., "0" from verified_productions counts)
    that should not be treated as production names. Also fixes CP1252 mojibake.
    """
    if not value or not value.strip():
        return []
    return [
        fix_cp1252_mojibake(item.strip())
        for item in value.split(";")
        if item.strip() and not item.strip().isdigit()
    ]


def seed_database():
    """Populate the database with curated London cultural locations."""
    app = create_app()

    with app.app_context():
        # Clear existing data in correct order
        LocationProduction.query.delete()
        Production.query.delete()
        Location.query.delete()
        db.session.commit()

        # Insert locations
        for loc_data in LOCATIONS_DATA:
            location = Location(**loc_data)
            db.session.add(location)
            db.session.flush()

            # If the location has top_productions or top_modelled, create Production records
            for field in ["top_modelled", "top_productions"]:
                raw = loc_data.get(field)
                if raw:
                    for item in parse_semicolon_field(raw):
                        production = Production.query.filter_by(name=item).first()
                        if not production:
                            production = Production(name=item)
                            db.session.add(production)
                            db.session.flush()
                        lp = LocationProduction(
                            location_id=location.id,
                            production_id=production.id,
                            production_source=field,
                        )
                        db.session.add(lp)

        db.session.commit()
        print(f"Successfully seeded {len(LOCATIONS_DATA)} locations into the database.")


if __name__ == "__main__":
    seed_database()

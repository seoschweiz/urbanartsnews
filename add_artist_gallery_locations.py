"""Embed verified gallery coordinates in Art Is Trash and Ashwan JPEG XMP metadata."""

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path("assets/images")
XMP_HEADER = b"http://ns.adobe.com/xap/1.0/\x00"

LOCATIONS = {
    "art-is-trash": {
        "title": "Artevistas Gallery Born",
        "address": "Carrer de la Barra de Ferro, 8, 08003 Barcelona, Spain",
        "city": "Barcelona",
        "region": "Catalonia",
        "country": "Spain",
        "country_code": "ES",
        "latitude": "41.38510",
        "longitude": "2.18058",
        "map": "https://www.google.com/maps/search/?api=1&query=41.38510%2C2.18058",
    },
    "ashwan": {
        "title": "BienCuadrado Art Gallery",
        "address": "Carrer d'Ataülf, 14, 08002 Barcelona, Spain",
        "city": "Barcelona",
        "region": "Catalonia",
        "country": "Spain",
        "country_code": "ES",
        "latitude": "41.3809952",
        "longitude": "2.1790367",
        "map": "https://www.google.com/maps/search/?api=1&query=41.3809952%2C2.1790367",
    },
}


def xmp_packet(location):
    values = {key: escape(value) for key, value in location.items()}
    latitude = gps_xmp(location["latitude"], "N", "S")
    longitude = gps_xmp(location["longitude"], "E", "W")
    return f'''<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
   xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/"
   xmlns:exif="http://ns.adobe.com/exif/1.0/"
   photoshop:City="{values['city']}"
   photoshop:State="{values['region']}"
   photoshop:Country="{values['country']}"
   Iptc4xmpCore:CountryCode="{values['country_code']}"
   Iptc4xmpCore:Location="{values['title']}"
   exif:GPSLatitude="{latitude}"
   exif:GPSLongitude="{longitude}">
   <dc:coverage><rdf:Alt><rdf:li xml:lang="x-default">{values['address']}</rdf:li></rdf:Alt></dc:coverage>
   <dc:relation><rdf:Bag><rdf:li>{values['map']}</rdf:li></rdf:Bag></dc:relation>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''.encode("utf-8")


def gps_xmp(decimal, positive, negative):
    value = float(decimal)
    hemisphere = positive if value >= 0 else negative
    value = abs(value)
    degrees = int(value)
    minutes = (value - degrees) * 60
    return f"{degrees},{minutes:.6f}{hemisphere}"


def jpeg_segments(data):
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("Not a JPEG")
    position = 2
    while position + 4 <= len(data) and data[position] == 0xFF:
        marker = data[position + 1]
        if marker in {0xDA, 0xD9}:
            break
        length = int.from_bytes(data[position + 2:position + 4], "big")
        end = position + 2 + length
        if end > len(data):
            raise ValueError("Invalid JPEG segment")
        yield position, end, marker, data[position + 4:end]
        position = end


def embed_xmp(path, location):
    data = path.read_bytes()
    packet = XMP_HEADER + xmp_packet(location)
    if len(packet) + 2 > 65535:
        raise ValueError("XMP packet is too large")
    segment = b"\xff\xe1" + (len(packet) + 2).to_bytes(2, "big") + packet
    ranges = [
        (start, end)
        for start, end, marker, payload in jpeg_segments(data)
        if marker == 0xE1 and payload.startswith(XMP_HEADER)
    ]
    for start, end in reversed(ranges):
        data = data[:start] + data[end:]
    path.write_bytes(data[:2] + segment + data[2:])


def main():
    updated = []
    for artist, location in LOCATIONS.items():
        for path in sorted((ROOT / artist).glob("*.jpg")):
            embed_xmp(path, location)
            updated.append(path)
    print(f"Gallery location metadata embedded in {len(updated)} JPEG files")


if __name__ == "__main__":
    main()

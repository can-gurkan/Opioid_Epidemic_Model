# Import requests, shutil python module.
import requests
import shutil
from math import pi, log, tan, exp, atan, log2, floor


ZOOM0_SIZE = 256


def main(marker1,marker2,apikey):
    center, zoom = get_center_zoom([float(marker1[0]),float(marker1[1]),float(marker2[0]),float(marker2[1])])
    # This is the image url.
    #image_url = "https://maps.googleapis.com/maps/api/staticmap?format=png&size=500x500&maptype=roadmap&style=feature:road|visibility:off&markers=size:tiny|40.702147,-74.015794|40.711614,-74.012318&key=AIzaSyBY5aBx-ObbPjO_RdVyJeSe2ulCGAnfehc"
    #image_url = "https://maps.googleapis.com/maps/api/staticmap?center="+str(center[0])+","+str(center[1])+"&zoom="+str(zoom)+"&format=png&size=500x500&maptype=roadmap&style=feature:road|visibility:off&markers=size:tiny|"+str(marker1[0])+","+str(marker1[1])+"|"+str(marker2[0])+","+str(marker2[1])+"&key="+str(apikey)
    image_url = "https://maps.googleapis.com/maps/api/staticmap?center="+str(center[0])+","+str(center[1])+"&zoom="+str(zoom)+"&format=png&size=500x500&maptype=roadmap&style=feature:road|visibility:off&key="+str(apikey)
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)
    # Open a local file with wb ( write binary ) permission.
    local_file = open('local_image.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp


# bbox = (left, bottom, right, top) in degrees
def get_center_zoom(bbox):
    # The region of interest in geo-coordinates in degrees
    # For example, bbox = [120.2206, 22.4827, 120.4308, 22.7578]
    (top, right, bottom, left) = bbox

    (w, h) = (600, 600)
    # The center point of the region of interest
    (lat, lon) = ((top + bottom) / 2, (left + right) / 2)
    center = (lat-0.05,lon)

    # Reduce precision of (lat, lon) to increase cache hits
    snap_to_dyadic = (lambda a, b: (lambda x, scale=(2 ** floor(log2(abs(b - a) / 4))): (round(x / scale) * scale)))
    lat = snap_to_dyadic(bottom, top)(lat)
    lon = snap_to_dyadic(left, right)(lon)
    assert ((bottom < lat < top) and (left < lon < right)), "Reference point not inside the region of interest"

    # Look for appropriate zoom level to cover the region of interest
    zoom = 16
    for zoom in range(16, 0, -1):
        # Center point in pixel coordinates at this zoom level
        (x0, y0) = g2p(lat, lon, zoom)
        # The "container" geo-region that the downloaded map would cover
        (TOP, LEFT) = p2g(x0 - w / 2, y0 - h / 2, zoom)
        (BOTTOM, RIGHT) = p2g(x0 + w / 2, y0 + h / 2, zoom)
        # Would the map cover the region of interest?
        if (LEFT <= left < right <= RIGHT):
            if (BOTTOM <= bottom < top <= TOP):
                break

    return center,zoom


# Geo-coordinate in degrees => Pixel coordinate
def g2p(lat, lon, zoom):
    return (
        # x
        ZOOM0_SIZE * (2 ** zoom) * (1 + lon / 180) / 2,
        # y
        ZOOM0_SIZE / (2 * pi) * (2 ** zoom) * (pi - log(tan(pi / 4 * (1 + lat / 90))))
    )

# Pixel coordinate => geo-coordinate in degrees
def p2g(x, y, zoom):
    return (
        # lat
        (atan(exp(pi - y / ZOOM0_SIZE * (2 * pi) / (2 ** zoom))) / pi * 4 - 1) * 90,
        # lon
        (x / ZOOM0_SIZE * 2 / (2 ** zoom) - 1) * 180,
    )


if __name__ == "__main__":

    api_key = "AIzaSyBY5aBx-ObbPjO_RdVyJeSe2ulCGAnfehc"
    m1 = [34.698987, -117.734635]
    m2 = [33.731587, -118.562865]
    #m2 = [40.702147,-74.015794]
    #m1 = [40.711614,-74.012318]
    main(m1, m2, api_key)


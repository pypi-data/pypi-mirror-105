if __name__ == "__main__":
    import sys
    import gdalinfo
    import pprint

    info = gdalinfo.info(sys.argv[1])
    pprint.pprint(info)
    wktVerbatim = info["coordinateSystem"]["wkt"]
    assert isinstance(gdalinfo.SpatialReference(wktVerbatim).exportToWkt(), str)
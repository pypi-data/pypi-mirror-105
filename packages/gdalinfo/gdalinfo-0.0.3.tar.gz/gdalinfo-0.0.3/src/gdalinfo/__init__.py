"""
A cffi binding to gdalinfo.
"""

from _gdalinfo import ffi, lib
import json

lib.GDALAllRegister()


class GDALException(Exception):
    def __init__(self):
        Exception.__init__(
            self,
            lib.CPLGetLastErrorNo(),
            ffi.string(lib.CPLGetLastErrorMsg()).decode("utf-8"),
        )


def info(path):
    """
    Return gdalinfo json for file at path.
    """
    dataset = lib.GDALOpen(str(path).encode("utf-8"), lib.GA_ReadOnly)
    if dataset == ffi.NULL:
        raise GDALException()

    try:
        with ffi.gc(
            lib.GDALInfoOptionsNew(
                [ffi.new("char[]", arg) for arg in b"-json -mdd all".split()]
                + [ffi.NULL],
                ffi.NULL,
            ),
            lib.GDALInfoOptionsFree,
        ) as options:
            info = ffi.gc(lib.GDALInfo(dataset, options), lib.VSIFree)
            if info == ffi.NULL:
                raise GDALException()
    finally:
        lib.GDALClose(dataset)

    return json.loads(ffi.string(info).decode("utf-8"))


class SpatialReference:
    def __init__(self, wkt=ffi.NULL):
        self._handle = ffi.gc(
            lib.OSRNewSpatialReference(ffi.NULL), lib.OSRDestroySpatialReference
        )
        if wkt:
            self.importFromWkt(wkt)

    def importFromWkt(self, wkt):
        err = lib.OSRImportFromWkt(
            self._handle, [ffi.new("char[]", wkt.encode("utf-8"))]
        )
        if err != 0:
            raise GDALException()

    def exportToWkt(self):
        """
        Returned WKT can be simpler than imported WKT.
        """
        rc = ffi.new("char*[1]")
        err = lib.OSRExportToWkt(self._handle, rc)
        if err != 0:
            raise GDALException()
        wkt = ffi.string(rc[0]).decode("utf-8")
        lib.VSIFree(rc[0])
        return wkt

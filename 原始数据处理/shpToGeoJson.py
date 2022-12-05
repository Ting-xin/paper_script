import ogr
import gdal
import os


def ChangeToJson(vector, output):
    print("Starting........")
    # 打开矢量图层
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
    shp_ds = ogr.Open(vector)
    shp_lyr = shp_ds.GetLayer(0)

    # 创建结果Geojson
    baseName = os.path.basename(output+'/outjson.json')
    out_driver = ogr.GetDriverByName('GeoJSON')
    out_ds = out_driver.CreateDataSource(output+'/outjson.json')
    if out_ds.GetLayer(baseName):
        out_ds.DeleteLayer(baseName)
    out_lyr = out_ds.CreateLayer(baseName, shp_lyr.GetSpatialRef())
    out_lyr.CreateFields(shp_lyr.schema)
    out_feat = ogr.Feature(out_lyr.GetLayerDefn())

    # 生成结果文件
    # for feature in shp_lyr:
    #     out_feat.SetGeometry(feature.geometry())
    #     for j in range(feature.GetFieldCount()):
    #         out_feat.SetField(j, feature.GetField(j))
    #     out_lyr.CreateFeature(out_feat)

    # 生成结果文件
    for feature in shp_lyr:
        out_feat.SetGeometry(feature.geometry())
        # for j in range(feature.GetFieldCount()):
        #     # out_feat.SetField(j, feature.GetField(j))
        #     print(j)
        print(feature.GetFieldCount())
        out_lyr.CreateFeature(out_feat)

    del out_ds
    del shp_ds
    print("Success........")


ChangeToJson(r"E:\paper\data\原始数据\历年行政区划数据\test\县.shp", r"E:\paper\data\原始数据\历年行政区划数据\output")

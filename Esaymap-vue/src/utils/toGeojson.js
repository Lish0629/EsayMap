export function toGeoJson(arcjson)   {
  let geojson;
  if (Array.isArray(arcjson.geometries)) {
    // 多个几何 -> FeatureCollection
    if (arcjson.geometries.length === 1) {
      geojson = {
        type: "Feature",
        geometry: {
          type: "Polygon",
          coordinates: arcjson.geometries[0].rings
        },
        properties: {}
      };
    } else {
      geojson = {
        type: "FeatureCollection",
        features: arcjson.geometries.map(g => ({
          type: "Feature",
          geometry: {
            type: "Polygon",
            coordinates: g.rings
          },
          properties: {}
        }))
      };
    }
  } else if (arcjson.geometry) {
    // ArcGIS 单个 Feature 格式
    geojson = {
      type: "Feature",
      geometry: {
        type: "Polygon",
        coordinates: arcjson.geometry.rings
      },
      properties: arcjson.attributes || {}
    };
  }
  return geojson;
}
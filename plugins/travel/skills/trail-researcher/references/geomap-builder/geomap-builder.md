---
name: geomap-builder
description: Research precise geographic locations and normalize remote GPX/GeoJSON sources into a lean, stateless GeoMap object with a layers array of wrappers whose geojson members are standard GeoJSON.
---

# GeoMap Builder

## Purpose

Create a reusable GeoMap object from two kinds of input:

1. Human-readable points of interest (POIs) with context and caller-supplied categories.
2. Remote GPX and/or GeoJSON URLs.

The skill must research POI coordinates carefully, download and normalize remote geographic files, and return one final JSON object whose root contains a `layers` array. GPX is an input format only. The output must never contain a GPX layer or GPX payload.

The output is intended to be directly usable by a map renderer such as Leaflet/OpenStreetMap and also easy to transform into HTML tables or dictionaries of entities.

## Input contract

Accept the following information from the executor in natural language or structured form:

- **Context**: enough geographic or itinerary context to disambiguate names.
- **POIs**: a list of requested entities. Each POI should include:
  - `name` — human-readable location name.
  - `category` — supplied by the executor, e.g. `accommodation`, `transport`, `water`, `pass`, `viewpoint`, `settlement`.
  - `routeSection` — optional grouping or stage label.
  - any extra contextual note useful for disambiguation.
- **Remote geographic sources**: zero or more URLs pointing to:
  - GPX files.
  - GeoJSON files.
- Optional instructions about layer names, ordering, or geometry simplification.

If a POI category is missing, ask for it only when the category is necessary to satisfy the request and cannot be safely derived from the executor's own input. Do not invent domain-specific semantics merely to fill a field.

## Output contract

Return **only valid JSON**. Do not wrap it in Markdown, a code fence, prose, or commentary.

The root value must be a JSON object with exactly one required top-level property, `layers`, whose value is an array of layer wrappers:

```json
{
  "layers": [
    {
      "id": "points-of-interest",
      "name": "Points of interest",
      "role": "poi",
      "geojson": {
        "type": "FeatureCollection",
        "features": []
      }
    },
    {
      "id": "official-route",
      "name": "Official route",
      "role": "route",
      "source": {
        "url": "https://example.org/route.gpx",
        "publisher": "Example authority",
        "retrievedAt": "2026-09-12",
        "originalFormat": "gpx"
      },
      "geojson": {
        "type": "FeatureCollection",
        "features": []
      }
    }
  ]
}
```

The wrapper is custom GeoMap metadata. The value of every `geojson` member must be ordinary standards-compliant GeoJSON.

Do not add request/response bookkeeping such as `requestedName`, `query`, `resolvedFrom`, `status`, `confidenceResponse`, `unresolved`, or similar fields that imply the artifact is a transcript of a resolution process. The output must describe geographic entities and datasets statelessly.

## Layer wrapper schema

A layer wrapper may contain:

- `id` — stable lowercase kebab-case identifier.
- `name` — human-readable layer name.
- `role` — short semantic role such as `poi`, `route`, `variant`, `boundary`, or another generic map-layer role.
- `source` — optional dataset-level provenance object, primarily for imported GPX/GeoJSON datasets.
- `geojson` — required standard GeoJSON object, normally a `FeatureCollection`.

Keep wrappers lean. Do not add renderer-specific style unless explicitly requested.

### Dataset-level source

Use `source` on the wrapper when the whole layer originates from one remote dataset:

```json
{
  "url": "https://example.org/route.gpx",
  "publisher": "Example authority",
  "retrievedAt": "2026-09-12",
  "originalFormat": "gpx"
}
```

Use `originalFormat` values such as `gpx` or `geojson` only as provenance metadata. The actual `geojson` payload must already be normalized to GeoJSON.

If the publisher cannot be established reliably, omit `publisher` instead of guessing.

## POI GeoJSON schema

Normally group researched POIs into a single `FeatureCollection`, unless the executor explicitly requests different layer grouping.

Each POI is a standard GeoJSON `Feature` with `Point` geometry:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [2.623, 39.7108]
  },
  "properties": {
    "name": "Valldemossa",
    "category": "settlement",
    "routeSection": "Stage 2",
    "note": "Village reference point, not a specific entrance.",
    "source": {
      "url": "https://example.org/source",
      "publisher": "Example publisher",
      "retrievedAt": "2026-09-12"
    }
  }
}
```

`properties` may contain only lean, reusable entity information. Prefer these fields:

- `name`
- `category`
- `routeSection` when supplied or clearly meaningful
- `note` only when a limitation or map interpretation matters
- `source`

Do not duplicate coordinates in `properties`.

Do not include research-process fields. Do not include empty or null fields merely for schema symmetry.

## Geographic coordinate research

For each requested POI, perform online research before producing coordinates.

### Source priority

Prefer, in roughly this order:

1. Official operator, facility, municipality, park, trail authority, transport authority, or government source.
2. Official map links or embedded geographic metadata published by the entity itself.
3. OpenStreetMap mapped feature records or services exposing OSM feature coordinates.
4. Reputable hiking, mapping, or geographic sources where official data is unavailable.
5. Other credible sources only when needed to resolve ambiguity.

Never invent coordinates.

### Entity matching

Match the requested entity using all available context:

- name and alternate names;
- municipality / region / country;
- feature type;
- nearby landmarks;
- route section or itinerary context;
- relationship to provided GPX geometry where relevant.

Distinguish carefully between:

- building vs. entrance;
- settlement vs. a specific facility;
- refuge vs. similarly named mountain or sign;
- bus stop vs. town center;
- reservoir/water body vs. access point;
- pass/locality vs. trail junction.

Use context to disambiguate, but the final artifact must contain only the resolved geographic entity. Do not preserve request wording merely as request metadata.

### Coordinate rules

- Use WGS84 decimal degrees.
- GeoJSON coordinate order is `[longitude, latitude]`.
- Preserve useful source precision up to about five decimal places, without implying equivalent positional accuracy.
- A point may represent an area/locality when that is the best valid source. State this briefly in `properties.note` when it matters.
- A mapped spring or water feature does not establish flow or potable water.
- Do not manufacture an entrance coordinate from a building centroid.

### Cross-checking

Cross-check important POIs against provided or discovered authoritative route geometry when useful, especially passes, junctions, refuges, and route-access points.

Where an independent source is available, use it to reduce ambiguity. Two websites derived from the same underlying OpenStreetMap record are not independent confirmations.

Cross-checking is a research step, not output bookkeeping. Do not add verbose verification structures to the final JSON. If the check materially changes how the point should be interpreted, summarize only that user-relevant limitation in `properties.note`.

### Unresolved locations

If a requested POI cannot be resolved to a sufficiently defensible geographic point, omit it from the output.

Never create a placeholder coordinate. Never emit an `unresolved` object, null geometry, zero coordinate, or guessed point.

## Remote GPX handling

For every GPX URL:

1. Download the file.
2. Validate that it is parseable GPX/XML and inspect its contents.
3. Convert its geographic content to GeoJSON before output.
4. Emit only the converted GeoJSON inside the layer wrapper.
5. Record the original GPX URL as wrapper-level `source.url` and set `source.originalFormat` to `gpx`.

Do not create a `type: "gpx"` output layer.

### GPX to GeoJSON conversion

Normalize GPX elements as follows:

- `<trk>` / `<trkseg>` -> GeoJSON `LineString` or `MultiLineString` as appropriate.
- `<rte>` -> GeoJSON `LineString`.
- `<wpt>` -> GeoJSON `Point`.
- `<ele>` -> preserve elevation as the third coordinate `[longitude, latitude, elevation]` where present and valid.
- meaningful `name` and `desc` -> preserve in GeoJSON feature `properties` when present.
- timestamps -> omit by default unless the executor explicitly asks to preserve temporal data.
- vendor-specific GPX extensions -> omit by default unless they contain information explicitly requested by the executor.

Preserve separate track segments rather than joining gaps that the GPX represents explicitly.

Do not simplify route geometry by default. Only simplify when the executor explicitly requests it. When simplification is requested, retain the shape closely enough for the stated visualization use and never silently modify the original source file itself.

### GPX source failures

If a remote GPX cannot be downloaded, is not actually a GPX file, or cannot be parsed reliably, omit that layer rather than fabricating geometry.

## Remote GeoJSON handling

For every GeoJSON URL:

1. Download it.
2. Parse and validate it as GeoJSON.
3. Preserve its valid geometry and meaningful feature properties.
4. Normalize the top-level result to a `FeatureCollection` when practical without altering geographic meaning.
5. Place it under the wrapper's `geojson` field.
6. Record the source URL in wrapper-level `source` with `originalFormat: "geojson"`.

Do not rewrite valid third-party feature properties merely to match POI property conventions. The POI schema applies to researched POIs created by this skill, not to arbitrary imported datasets.

If the remote GeoJSON is invalid or cannot be fetched reliably, omit the layer.

## Layer construction

Default behavior:

- Put all successfully researched POIs in one POI layer.
- Create one layer wrapper per imported GPX or GeoJSON dataset.
- Preserve input ordering of remote datasets unless the executor asks for another order.
- Use short stable `id` values derived from dataset names or their geographic role.
- Use informative `name` values suitable for a map layer control.

Do not split POIs into separate layers merely because their categories differ. Category belongs in each POI feature's `properties.category`, unless the executor explicitly requests category-specific layers.

## Research coverage

The skill should search for the complete POI list supplied by the executor and may use itinerary or route context to find the correct geographic entity.

Do not automatically add extra POIs simply because they seem useful. Add entities beyond the explicit POI list only when the executor asked for discovery or expansion.

The skill may use provided GPX geometry to validate or disambiguate POIs, but a chain of POIs must never be treated as a route substitute.

## Quality checks before returning

Before output, verify all of the following:

- The root value is a JSON object containing a `layers` array.
- Every array element is a layer wrapper.
- Every wrapper contains `id`, `name`, `role`, and `geojson`.
- Every `geojson` value is valid GeoJSON.
- No output layer contains raw GPX or uses a GPX layer type.
- All GeoJSON coordinate arrays use longitude before latitude.
- Researched POIs use `Point` geometry.
- Every researched POI has a caller-supplied or otherwise explicitly established category.
- Every researched POI has a defensible source URL.
- Imported datasets use wrapper-level provenance.
- Unresolved POIs and failed remote datasets are omitted.
- No request/response bookkeeping is present.
- No Markdown or prose surrounds the JSON object.
- The JSON can be parsed directly by `JSON.parse`.

## Example executor input

Context:

`A multi-day route through Mallorca's Serra de Tramuntana.`

POIs:

- `Valldemossa` — category: `settlement`
- `Refugi de Tossals Verds` — category: `accommodation`
- `Coll de l'Ofre` — category: `pass`
- `Font des Noguer` — category: `water`

Remote geographic sources:

- `https://example.org/official-stage-1.gpx`
- `https://example.org/official-stage-2.gpx`
- `https://example.org/protected-area.geojson`

Expected result: a raw JSON object with a `layers` array containing one researched POI layer and one normalized GeoJSON layer for each successfully downloaded remote dataset.

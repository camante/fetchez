# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- csb module
- fetchez.spatial 'region_to_wkt' method
- fetchez.core fetch_req now supports 'method' arg
- fetchez.spatial 'region_center' method
- buouy module
- gmrt module
- fetchez.spatial 'region_to_bbox' method
- waterservices module
- etopo module
- fetchez.spatial 'region_to_geojson_geom'
- chs module
- bluetopo module
	
### Changed
- In fetchez.core, allow for transparent gzip (local size is larger than remote size)

## [2.0.0] - 2026-01-24
### Added
- Initial standalone release of Fetchez.
- Decoupled from CUDEM project.
- New `fetchez.spatial` module for lightweight region parsing.
- New `fetchez.registry` for lazy module loading.
- Modernized CLI with logging support.
- FRED index now uses GeoJSON and Shapely directly (removed OGR dependency).

### Changed
- Renamed project from `fetches` to `fetchez`.
- Refactored some old cudem.fetches modules to inherit from `fetchez.core.FetchModule`.

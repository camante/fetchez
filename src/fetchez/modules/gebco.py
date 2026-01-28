#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fetchez.modules.gebco
~~~~~~~~~~~~~~~~~~~~~

Fetch General Bathymetric Chart of the Oceans (GEBCO) data.
Supports regional subsetting via WCS (default) or global download.

:copyright: (c) 2010 - 2026 Regents of the University of Colorado
:license: MIT, see LICENSE for more details.
"""

from urllib.parse import urlencode
from fetchez import core
from fetchez import cli

# WCS Endpoint (Hosted by EMODnet/BODC for GEBCO)
GEBCO_WCS_URL = 'https://www.gebco.net/data_and_products/gebco_web_services/2024/mapserv?'

# Global Download Links (Direct)
GEBCO_GLOBAL_URLS = {
    '2024': 'https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024/geotiff/',
    '2024_tid': 'https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024_tid/geotiff/',
    '2024_sub_ice': 'https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024_sub_ice_topo/geotiff/'
}

# =============================================================================
# GEBCO Module
# =============================================================================
@cli.cli_opts(
    help_text="General Bathymetric Chart of the Oceans (GEBCO)",
    layer="Dataset Layer: 'grid' (Elevation), 'tid' (Type Identifier), 'sub_ice' (Under Ice)",
    global_grid="Download the full global dataset instead of a regional subset."
)

class GEBCO(core.FetchModule):
    """Fetch GEBCO global bathymetry data.
    
    GEBCO provides a global terrain model at ~15 arc-seconds (~500m).
    
    Modes:
      Regional (Default): Uses Web Coverage Service (WCS) to download only 
        the requested bounding box.

      Global (--global-grid): Downloads the full global dataset (zipped GeoTIFF).
      
    Layers:
      - grid: Standard bathymetry/topography (Ice Surface).
      - sub_ice: Bedrock elevation (Ice removed).
      - tid: Type Identifier (Source of data per pixel).

    References:
      - https://www.gebco.net/
    """
    
    def __init__(self, layer: str = 'grid', global_grid: bool = False, **kwargs):
        super().__init__(name='gebco', **kwargs)
        self.layer = layer.lower()
        self.global_grid = global_grid

        
    def _run_wcs_subset(self):
        """Fetch a regional subset via WCS."""
        if self.region is None:
            return

        w, e, s, n = self.region
        
        coverage_map = {
            'grid': 'GEBCO_2024_Grid',
            'elevation': 'GEBCO_2024_Grid',
            'tid': 'GEBCO_2024_TID',
            'sub_ice': 'GEBCO_2024_Sub_Ice_Topo'
        }
        
        cov_id = coverage_map.get(self.layer, 'GEBCO_2024_Grid')
        
        params = {
            'SERVICE': 'WCS',
            'VERSION': '1.3.0',
            'REQUEST': 'GetCoverage',
            'COVERAGE': cov_id,
            'CRS': 'EPSG:4326',
            'BBOX': f"{s},{w},{n},{e}", # WCS 1.3.0 usually lat,lon (South, West, North, East)
            'FORMAT': 'image/tiff',
            'RESPONSE_CRS': 'EPSG:4326'
        }
        
        full_url = f"{GEBCO_WCS_URL}{urlencode(params)}"
        
        r_str = f"w{w}_e{e}_s{s}_n{n}".replace('.', 'p').replace('-', 'm')
        out_fn = f"gebco_{self.layer}_{r_str}.tif"
        
        self.add_entry_to_results(
            url=full_url,
            dst_fn=out_fn,
            data_type='geotiff',
            agency='GEBCO / BODC',
            title=f"GEBCO 2024 {self.layer.upper()}"
        )

        
    def _run_global_download(self):
        """Fetch the full global zip."""
        
        key_map = {
            'grid': '2024',
            'tid': '2024_tid',
            'sub_ice': '2024_sub_ice'
        }
        
        key = key_map.get(self.layer, '2024')
        url = GEBCO_GLOBAL_URLS[key]
        
        self.add_entry_to_results(
            url=url,
            dst_fn=f"gebco_{key}.zip",
            data_type='zip',
            agency='GEBCO / BODC',
            title=f"Global GEBCO {key} (Full)"
        )

        
    def run(self):
        """Run the GEBCO fetching logic."""
        
        if self.global_grid:
            self._run_global_download()
        else:
            self._run_wcs_subset()
            
        return self

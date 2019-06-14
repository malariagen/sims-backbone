import { Component, Input } from '@angular/core';

import { Locations } from '../typescript-angular-client/model/locations';
import { Location } from '../typescript-angular-client/model/location';

import * as L from 'leaflet';
import 'leaflet.markercluster';


@Component({
  selector: 'sims-locations-map',
  templateUrl: './locations-map.component.html',
  styleUrls: ['./locations-map.component.css']
})
export class LocationsMapComponent {

  _locations: Locations;

  // Open Street Map Definition
  LAYER_OSM = {
    id: 'openstreetmap',
    name: 'Open Street Map',
    enabled: false,
    layer: L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: 'Open Street Map'
    })
  };

  // Values to bind to Leaflet Directive
  leaflet_layersControlOptions = { position: 'bottomright' };
  leaflet_layersControl = {
    baseLayers: {
      'Open Street Map': this.LAYER_OSM.layer
    },
    overlays: {
    }
  }

  leaflet_options = {
    zoom: 5,
    maxZoom: 18,
    center: L.latLng([-4.6991, 20.8422]),
    layers: [
      this.LAYER_OSM.layer
    ]
  };

  leaflet_zoom = 5;
  // Marker cluster stuff

  markers = new Map<string, L.Layer[]>();
  map;

  polygonLayer;

  @Input()
  set polygon(geojson) {
    if (geojson && geojson.type === 'Polygon') {
      if (this.polygonLayer) {
        this.polygonLayer.clearLayers();
      }
      this.polygonLayer = L.geoJSON().addTo(this.map);
      this.polygonLayer.addData(geojson);
      if (this._locations.count === 1) {
        this.map.panTo(L.latLng([this._locations.locations[0].latitude, this._locations.locations[0].longitude]));
      }
    }
  }

  @Input()
  set zoom(zoom: number) {
    // console.log("Setting zoom:" + zoom);
    this.leaflet_zoom = zoom
    this.centerMap();
  }

  centerMap() {
    if (!this.map) {
      return;
    }
    let center = null;
    if (this._locations && this._locations.count === 1) {
      center = L.latLng([this._locations.locations[0].latitude, this._locations.locations[0].longitude]);
      // Seems to be needed as well as setView
      this.map.panTo(center);
    } else {
      center = this.map.getCenter();
    }
    // Can't use panTo
    this.map.setView(center, this.leaflet_zoom);

  }

  @Input()
  set locations(locations: Locations) {

    this._locations = locations;
    this.showLocations();
  }

  showLocations() {

    if (!this.map) {
      return;
    }

    if (this._locations) {

      Object.entries(this.leaflet_layersControl['overlays']).forEach(([key, value]) => {
        if (this.map.hasLayer(value)) {
          this.map.clearLayers(value);
        }
      });
      this.centerMap();

      const locationsArray: Array<Location> = this._locations.locations;

      locationsArray.forEach(location => {

        let layer_name = 'Unknown';
        let loc = '';

        if (location.country) {
          layer_name = location.country;
        }
        if (location.attrs) {
          location.attrs.forEach(ident => {
            if (ident.attr_type == 'partner_name') {
              loc = location.country + ' ' + ident.study_name + ' ' + ident.attr_value;

              if (location.latitude && location.longitude) {
                this.addMarker(location.location_id, ident.study_name, location.latitude, location.longitude, loc);
              }
            }
          });
        } else {
          if (location.latitude && location.longitude) {
            this.addMarker(location.location_id, location.country, location.latitude, location.longitude, layer_name);
          }
        }
      });

      this.markers.forEach((value: L.Layer[], key: string) => {
        const mcg = L.markerClusterGroup();
        mcg.clearLayers();
        mcg.addLayers(value);
        this.leaflet_layersControl['overlays'][key] = mcg;
        // So that the layer is visible by default
        if (this.map) {
          mcg.addTo(this.map);
        }

      });

    }
  }

  onMapReady(map: L.Map) {
    this.map = map;
    this.showLocations();
  }

  addMarker(locationId, country, lat, lng, marker_title) {
    const marker = L.marker(
      [lat, lng],
      {
        title: marker_title,
        icon: L.icon({
          iconSize: [25 * 0.5, 41 * 0.5],
          iconAnchor: [13 * 0.5, 0],
          iconUrl: 'assets/marker-icon.png',
          shadowUrl: 'assets/marker-shadow.png'
        })
      }
    ).bindPopup('<a href="location/' + locationId + '">' + marker_title + '</a>');

    if (!this.markers.has(country)) {
      this.markers.set(country, []);
    }

    this.markers.get(country).push(marker);

  }

  disableLayers() {

    Object.entries(this.leaflet_layersControl['overlays']).forEach(([key, value]) => {
      if (this.map.hasLayer(value)) {
        this.map.removeLayer(value);
      }
    });
  }

  enableLayers() {
    Object.entries(this.leaflet_layersControl['overlays']).forEach(([key, value]) => {
      if (!this.map.hasLayer(value)) {
        this.map.addLayer(value);
      }
    });
  }

}

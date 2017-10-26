import { Component, Input } from '@angular/core';

import { Locations } from '../typescript-angular2-client/model/Locations';
import { Location } from '../typescript-angular2-client/model/Location';

import * as L from 'leaflet';
import 'leaflet.markercluster';


@Component({
  selector: 'app-locations-map',
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

  leaflet_zoom: number = 5;
  // Marker cluster stuff

  markers = new Map<string, L.Layer[]>();
  groups = new Map<string, L.MarkerClusterGroup>();
  map;

  polygonLayer;

  @Input()
  set polygon(geojson) {
    if (geojson && geojson.type == 'Polygon') {
      this.polygonLayer = L.geoJSON().addTo(this.map);
      this.polygonLayer.clearLayers();
      this.polygonLayer.addData(geojson);
      if (this._locations.count == 1) {
        this.map.panTo(L.latLng([this._locations.locations[0].latitude, this._locations.locations[0].longitude]));
      }
    }
  }

  @Input()
  set zoom(zoom: number) {
    console.log("Setting zoom:" + zoom);
    this.leaflet_zoom = zoom
    this.centerMap();
  }

  centerMap() {
    if (!this.map) {
      return;
    }
    let center = null;
    if (this._locations && this._locations.count == 1) {
      center = L.latLng([this._locations.locations[0].latitude, this._locations.locations[0].longitude]);
    } else {
      center = this.map.getCenter();
    }
    //Can't use panTo
    this.map.setView(center, this.leaflet_zoom);
  }

  @Input()
  set locations(locations: Locations) {

    console.log("locations-map set locations");
    this._locations = locations;

    if (this._locations) {
      let locationsArray: Array<Location> = this._locations.locations;

      this.centerMap();
      locationsArray.forEach(location => {

        let layer_name: string = 'Unknown';
        let loc: string = '';

        if (location.country) {
          layer_name = location.country;
        }
        if (location.identifiers) {
          location.identifiers.forEach(ident => {
            loc = location.country + " " + ident.study_name + ' ' + ident.identifier_value;

            if (location.latitude && location.longitude) {
              this.addMarker(ident.study_name, location.latitude, location.longitude, loc);
            }
          });
        } else {
          if (location.latitude && location.longitude) {
            this.addMarker(location.country, location.latitude, location.longitude, layer_name);
          }
        }

      });

      this.markers.forEach((value: L.Layer[], key: string) => {
        let mcg = L.markerClusterGroup();
        mcg.clearLayers();
        mcg.addLayers(value);
        this.leaflet_layersControl['overlays'][key] = mcg;
        //So that the layer is visible by default
        mcg.addTo(this.map);

      });


    }
  }

  onMapReady(map: L.Map) {
    this.map = map;
  }

  addMarker(country, lat, lng, marker_title) {
    let marker = L.marker(
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
    ).bindPopup('<a href="location/' + lat + '/' + lng + '">' + marker_title + '</a>');

    if (!this.markers.has(country)) {
      this.markers.set(country, []);
    }

    this.markers.get(country).push(marker);

  }
}

import { Component, NgZone, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';

import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Location } from '../typescript-angular-client/model/location';
import { Country } from '../typescript-angular-client/model/country';
import { Locations } from '../typescript-angular-client/model/locations';
import { LocationService } from '../typescript-angular-client/api/location.service';
import { MetadataService } from '../typescript-angular-client/api/metadata.service';

import { } from 'googlemaps';
import { MapsAPILoader } from '@agm/core';
import { LatLngLiteral } from '@agm/core';

@Component({
  selector: 'app-location-edit',
  providers: [LocationService, MetadataService, HttpClient],
  templateUrl: './location-edit.component.html',
  styleUrls: ['./location-edit.component.css']
})
export class LocationEditComponent implements OnInit {

  calc2Cols = '2 2 calc(10em + 10px);';
  /** 10px is the missing margin of the missing box */
  calc3Cols = '3 3 calc(15em + 20px)';
  /** 20px is the missing margin of the two missing boxes */

  latitude: string;
  longitude: string;

  location: Location;
  locations;

  polygon;

  public locationForm: FormGroup;
  public osmForm: FormGroup;
  public googleForm: FormGroup;
  public gPolygon: Array<LatLngLiteral> = [];
  public locationEvents: string = '/location/events';

  zoom: number = 10;
  accuracy: string;

  constructor(protected httpClient: HttpClient, private route: ActivatedRoute, private locationService: LocationService, private metadataService: MetadataService, private _fb: FormBuilder, private mapsAPILoader: MapsAPILoader, private ngZone: NgZone
  ) { }

  getPrecisionFromZoom() {
    let ret = 'country';

    if (this.zoom > 6) {
      ret = 'region';
    }
    if (this.zoom > 9) {
      ret = 'city';
    }
    if (this.zoom > 15) {
      ret = 'building';
    }
    return ret;
  }

  setPrecisionFromZoom() {
    if (this.locationForm) {
      this.locationForm.controls['accuracy'].setValue(this.getPrecisionFromZoom());
    }
  }


  setZoomFromPrecision() {
    this.zoom = 4;
    if (this.location && this.location.accuracy) {
      if (this.location.accuracy == 'country') {
        this.zoom = 4;
      }
      if (this.location.accuracy == 'region') {
        this.zoom = 7;
      }
      if (this.location.accuracy == 'city') {
        this.zoom = 11;
      }
      if (this.location.accuracy == 'building') {
        this.zoom = 16;
      }
    }
  }

  setCountry(country: string) {
    this.metadataService.getCountryMetadata(country.toUpperCase()).subscribe((countryData) => {
      this.locationForm.controls['country'].setValue(countryData.alpha3);
    });
  }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.latitude = pmap.get('latitude');
      this.longitude = pmap.get('longitude');
    });

    this.locationService.downloadGPSLocation(this.latitude, this.longitude).subscribe(
      (location) => {
        console.log("Downloaded location via GPS");
        let locs = <Locations>{
          count: 0,
          locations: []
        };
        this.location = location;
        this.setZoomFromPrecision();
        this.accuracy = this.getPrecisionFromZoom();
        locs.count = 1;
        locs.locations = [location];
        this.locations = locs;

        this.locationForm = this._fb.group(
          {
            location_id: [this.location.location_id, [Validators.required]],
            latitude: [this.location.latitude, [Validators.required]],
            longitude: [this.location.longitude, [Validators.required]],
            curated_name: [this.location.curated_name, [Validators.required]],
            curation_method: [this.location.curation_method, [Validators.required]],
            notes: [this.location.notes, []],
            country: [this.location.country, [Validators.required, Validators.minLength(3)]],
            accuracy: [this.location.accuracy, [Validators.required]],
            identifiers: this._fb.array([]),
          }
        );
        const formIdents = <FormArray>this.locationForm.controls['identifiers'];

        if (this.location.identifiers) {
          this.location.identifiers.forEach(ident => {
            let identControl = new FormGroup({
              identifier_type: new FormControl(ident.identifier_type, Validators.required),
              identifier_value: new FormControl(ident.identifier_value, Validators.required),
              study_name: new FormControl(ident.study_name, Validators.required),
            });
            formIdents.push(identControl);
          });
        }
        //console.log(this.locationForm);
        //console.log(this.locations);


      },
      (err) => console.error(err),
      () => { console.log("Downloaded locations") }
    );

  }

  public onSubmit({ value, valid }: { value: Location, valid: boolean }): void {

    console.log("Submitting:" + JSON.stringify(value));
    //Should be solved by the nullable property but isn't
    if (!value.notes) {
      value.notes = '';
    }
    this.locationService.updateLocation(value.location_id, value).subscribe((result) => {
      //console.log(result);
    },
      (err) => {
        console.log(err); alert('Failed to save');
      });
  }

  public onSubmitFetchOSM({ value, valid }: { value: Location, valid: boolean }): void {
    this.fetchOSM(value);
  }

  public fetchOSM(location): void {

    this.ngZone.run(() => {
      this.getOSM().subscribe((resp) => {
        //console.log("OSM response:");
        //console.log(resp);
        this.osmForm = this._fb.group(
          {
            'display_name': [resp.display_name],
            'country_code': ['']
          }
        );
        if (resp.address && resp.address.country_code) {
          this.osmForm.controls['country_code'].setValue(resp.address.country_code);
        }
        if (resp.geojson) {
          this.polygon = resp.geojson;
        }
      },
        err => {
          console.log("Request to OSM failed");
          alert('OSM request failed please try again later');
        });
    });
  }

  public getOSM() {

    let headers = new HttpHeaders();

    headers.set('Content-Type', 'application/json');
    headers.set('User-Agent', 'wrighting test app');


    let path = 'http://nominatim.openstreetmap.org/reverse?format=json&polygon_geojson=1&lat=' + this.location.latitude + '&lon=' + this.location.longitude + '&zoom=' + this.zoom;
    return this.httpClient.post<any>(path, null, {
      headers: headers
    });

  }

  public useOSM({ value, valid }: { value: any, valid: boolean }): void {
    console.log(value);
    this.locationForm.controls['curated_name'].setValue(value.display_name);
    this.locationForm.controls['curation_method'].setValue('osm');
    this.setPrecisionFromZoom();
    this.setCountry(value.country_code);
  }

  public onSubmitFetchGoogleMaps({ value, valid }: { value: Location, valid: boolean }): void {
    this.fetchGoogleMaps(value);
  }

  private setGooglePolygon(geometry): void {

    if (!geometry.bounds) {
      return;
    }

    this.gPolygon = [];
    let point = {
      lat: geometry.bounds.getNorthEast().lat(),
      lng: geometry.bounds.getSouthWest().lng()
    };
    this.gPolygon.push(point);
    this.gPolygon.push(geometry.bounds.getNorthEast());
    point = {
      lat: geometry.bounds.getSouthWest().lat(),
      lng: geometry.bounds.getNorthEast().lng()
    };
    this.gPolygon.push(point);
    this.gPolygon.push(geometry.bounds.getSouthWest());
    //console.log(geometry);
  }

  public fetchGoogleMaps(location): void {

    this.mapsAPILoader.load().then(() => {
      this.ngZone.run(() => {
        let geocoder = new google.maps.Geocoder();
        let latlng = new google.maps.LatLng(this.location.latitude, this.location.longitude);
        let request = {
          location: latlng
        };
        geocoder.geocode(request, (results, status) => {
          //console.log('Google geocoded');
          //console.log(results);

          this.googleForm = this._fb.group(
            {
              'display_name': [''],
              'country_code': ['']
            }
          );
          let country_code = false;
          let display_name = '';
          results.forEach(result => {
            result.address_components.forEach(addr_component => {
              addr_component.types.forEach(type => {
                //console.log(this.zoom + ":" + display_name + ":" + type + ":" + result.formatted_address);
                if (this.zoom < 10 && type == 'administrative_area_level_1') {
                  display_name = result.formatted_address;
                  this.setGooglePolygon(result.geometry);
                } else
                  if (this.zoom < 15 && (type == 'administrative_area_level_2' || type == 'sublocality')) {
                    display_name = result.formatted_address;
                    this.setGooglePolygon(result.geometry);
                  } else
                    if (this.zoom > 16 && (type == 'locality' || type == 'sublocality')) {
                      display_name = result.formatted_address;
                      this.setGooglePolygon(result.geometry);
                    } else
                      if (this.zoom > 16 && type == 'sublocality') {
                        display_name = result.formatted_address;
                        this.setGooglePolygon(result.geometry);
                      } else
                        if (type == 'country' && !country_code) {
                          country_code = true;
                          this.googleForm.controls['country_code'].setValue(addr_component.short_name);
                          //console.log(addr_component.long_name);
                        }

              });
            });
          });
          this.googleForm.controls['display_name'].setValue(display_name);

        });
      });
    });
  }

  public useGoogle({ value, valid }: { value: any, valid: boolean }): void {
    console.log(value);
    this.locationForm.controls['curated_name'].setValue(value.display_name);
    this.locationForm.controls['curation_method'].setValue('google');
    this.setPrecisionFromZoom();
    this.setCountry(value.country_code);
  }

  public incrementZoom(): void {
    this.zoom += 1;
    this.fetchOSM(this.location);
    this.fetchGoogleMaps(this.location);
    this.accuracy = this.getPrecisionFromZoom();
  }
  public decrementZoom(): void {
    this.zoom -= 1;
    this.fetchOSM(this.location);
    this.fetchGoogleMaps(this.location);
    this.accuracy = this.getPrecisionFromZoom();
  }
}

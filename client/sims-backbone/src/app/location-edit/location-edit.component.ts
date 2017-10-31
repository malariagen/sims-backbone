import { Component, NgZone, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';

import { Http, Headers, URLSearchParams } from '@angular/http';
import { RequestMethod, RequestOptions, RequestOptionsArgs } from '@angular/http';
import { Response, ResponseContentType } from '@angular/http';

import { Location } from '../typescript-angular2-client/model/Location';
import { Country } from '../typescript-angular2-client/model/Country';
import { Locations } from '../typescript-angular2-client/model/Locations';
import { LocationApi } from '../typescript-angular2-client/api/LocationApi';
import { MetadataApi } from '../typescript-angular2-client/api/MetadataApi';

import { } from 'googlemaps';
import { MapsAPILoader } from '@agm/core';

@Component({
  selector: 'app-location-edit',
  providers: [LocationApi, MetadataApi],
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

  public locationEvents: string = '/location/events';
  public studyEvents: string = '/study/events';

  zoom: number = 10;
  precision: string;

  constructor(private route: ActivatedRoute, private locationApi: LocationApi, private metadataApi: MetadataApi, private _fb: FormBuilder, protected http: Http, private mapsAPILoader: MapsAPILoader, private ngZone: NgZone
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
      this.locationForm.controls['precision'].setValue(this.getPrecisionFromZoom());
    }
  }


  setZoomFromPrecision() {
    this.zoom = 4;
    if (this.location && this.location.precision) {
      if (this.location.precision == 'country') {
        this.zoom = 4;
      }
      if (this.location.precision == 'region') {
        this.zoom = 7;
      }
      if (this.location.precision == 'city') {
        this.zoom = 11;
      }
      if (this.location.precision == 'building') {
        this.zoom = 16;
      }
    }
  }

  setCountry(country: string) {
    this.metadataApi.getCountryMetadata(country.toUpperCase()).subscribe((countryData) => {
      this.locationForm.controls['country'].setValue(countryData.alpha3);
    });
  }

  ngOnInit() {
    this.latitude = this.route.snapshot.params['latitude'];
    this.longitude = this.route.snapshot.params['longitude'];

    this.locationApi.downloadGPSLocation(this.latitude, this.longitude).subscribe(
      (location) => {
        console.log("Downloaded location via GPS");
        let locs = {
          count: 0,
          locations: []
        };
        this.location = location;
        this.setZoomFromPrecision();
        this.precision = this.getPrecisionFromZoom();
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
            precision: [this.location.precision, [Validators.required]],
            identifiers: this._fb.array([]),
          }
        );
        const formIdents = <FormArray>this.locationForm.controls['identifiers'];

        this.location.identifiers.forEach(ident => {
          let identControl = new FormGroup({
            identifier_type: new FormControl(ident.identifier_type, Validators.required),
            identifier_value: new FormControl(ident.identifier_value, Validators.required),
            study_name: new FormControl(ident.study_name, Validators.required),
          });
          formIdents.push(identControl);
        });

        console.log(this.locationForm);
        console.log(this.locations);


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
    this.locationApi.updateLocation(value.location_id, value).subscribe((result) => {
      console.log(result);
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
        console.log("OSM response:");
        console.log(resp);
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

    let headers = new Headers();
    headers.set('Content-Type', 'application/json');
    headers.set('User-Agent', 'wrighting test app');
    let requestOptions: RequestOptionsArgs = new RequestOptions({
      method: RequestMethod.Post,
      headers: headers,
      body: null

    });


    let path = 'http://nominatim.openstreetmap.org/reverse?format=json&polygon_geojson=1&lat=' + this.location.latitude + '&lon=' + this.location.longitude + '&zoom=' + this.zoom;
    return this.http.request(path, requestOptions).map((response: Response) => {
      if (response.status === 204) {
        return undefined;
      } else if (response.status === 503) {
        console.log("Request to OSM failed");
        return undefined;
      } else {
        return response.json() || {};
      }
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

    this.mapsAPILoader.load().then(() => {
      this.ngZone.run(() => {
        let geocoder = new google.maps.Geocoder();
        let latlng = new google.maps.LatLng(this.location.latitude, this.location.longitude);
        let request = {
          latLng: latlng
        };
        geocoder.geocode(request, (results, status) => {
          console.log('Google geocoded');
          console.log(results);

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
                if (type == 'administrative_area_level_1') {
                  console.log(result.formatted_address);
                  display_name = result.formatted_address;
                } else
                  if (type == 'administrative_area_level_2' && display_name == '') {
                    display_name = result.formatted_address;
                  } else
                    if (type == 'locality' && display_name == '') {
                      display_name = result.formatted_address;
                    } else
                      if (type == 'sublocality' && display_name == '') {
                        display_name = result.formatted_address;
                      } else
                        if (type == 'country' && !country_code) {
                          country_code = true;
                          this.googleForm.controls['country_code'].setValue(addr_component.short_name);
                          console.log(addr_component.long_name);
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
    this.precision = this.getPrecisionFromZoom();
  }
  public decrementZoom(): void {
    this.zoom -= 1;
    this.fetchOSM(this.location);
    this.precision = this.getPrecisionFromZoom();
  }
}

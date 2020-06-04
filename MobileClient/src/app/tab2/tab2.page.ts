import { Component, OnInit } from '@angular/core';
//import { Geolocation} from '@capacitor/core';

import { Geolocation } from '@ionic-native/geolocation/ngx';
import { IdentificationService } from '../services/identification.service';
import { SynchronizationService } from '../services/synchronization.service';

import { GeoLocationPoint } from '../services/synchronization.service'

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page implements OnInit {

  latitude: number;
  longitude: number;
  lastUpdate: number;
  currentIdentity: number;

  constructor(private geolocation: Geolocation, 
    private identificationService: IdentificationService, 
    private synchronizationService: SynchronizationService) {
  }

  ngOnInit(): void {
    let watch = this.geolocation.watchPosition();
    watch.subscribe((data) => {
        this.latitude = data.coords.latitude;
        this.longitude = data.coords.longitude;
        this.lastUpdate = data.timestamp;
        if (this.currentIdentity) {
          const point = {
            latitude: this.latitude, 
            longitude: this.longitude, 
            timestamp: this.lastUpdate, identifier: 
            this.currentIdentity
          } as GeoLocationPoint;
          this.synchronizationService.postSingleGeoLocation(point);
        }
      },
      (err) => {
        console.log(err);
      }
    );

    this.identificationService.getIdentity().subscribe((data) => {
        this.currentIdentity = data;
    });
  }

  // async getLocation() {
  //   const position = await Geolocation.getCurrentPosition();
  //   this.latitude = position.coords.latitude;
  //   this.longitude = position.coords.longitude;
  // }

}

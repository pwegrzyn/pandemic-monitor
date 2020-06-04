import { Injectable } from '@angular/core';

import { HTTP } from '@ionic-native/http/ngx';


export type methods = 'get' | 'post' | 'put' | 'patch' | 'head' | 'delete' | 'options' | 'upload' | 'download';
export type serializers = 'json' | 'urlencoded' | 'utf8' | 'multipart';

@Injectable({
  providedIn: 'root'
})
export class SynchronizationService {

  locationSyncServerAddr: string;
  
  constructor(private http: HTTP) {
    // TODO: Somehow inject the addr string dynamically based on Docker context
    this.locationSyncServerAddr = "http://192.168.1.187:5042/location";
  }

  public postSingleGeoLocation(point: GeoLocationPoint) {
    const options = {
      method: "post" as methods,
      data: {
        "latitude": point.latitude, 
        "longitude": point.longitude, 
        "timestamp": point.timestamp, 
        "identifier": point.identifier
      },
      headers: { "x-user-identifier": point.identifier.toString() },
      serializer: "json" as serializers
    };

    this.http.sendRequest(this.locationSyncServerAddr, options)
      .then(data => {
        console.log(data.status);
        console.log(data.data); // data received by server
        console.log(data.headers);
      })
      .catch(error => {
        console.log(error.status);
        console.log(error.error); // error message as string
        console.log(error.headers);
      });
  }

}


export interface GeoLocationPoint {
  latitude: number;
  longitude: number;
  timestamp: number;
  identifier: number;
}

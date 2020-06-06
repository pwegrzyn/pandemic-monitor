import { Injectable } from '@angular/core';

import { HTTP } from '@ionic-native/http/ngx';
import { Observable, from } from 'rxjs';
import { IdentificationService } from './identification.service';

export type methods = 'get' | 'post' | 'put' | 'patch' | 'head' | 'delete' | 'options' | 'upload' | 'download';
export type serializers = 'json' | 'urlencoded' | 'utf8' | 'multipart';


@Injectable({
  providedIn: 'root'
})
export class FetchingService {

  statusURI: string;
  identity: number;

  constructor(private http: HTTP, private identificationService: IdentificationService) {
    // TODO: Somehow inject the addr string dynamically based on Docker context
    this.statusURI = "http://192.168.1.187:5048/usersByUUID/";
    this.identificationService.getIdentity().subscribe(data => {
      this.identity = data;
    });
  }

  public getStatus(): Observable<string> {
    const options = {
      method: "get" as methods,
      data: {},
      headers: { "x-user-identifier": this.identity + "" },
      serializer: "json" as serializers
    };

    return from(
      this.http.sendRequest(this.statusURI + this.identity, options)
      .then(data => {
        console.log(data.data)
        return JSON.parse(data.data)["status"]
      })
    );

  }

}

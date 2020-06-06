import { Injectable } from '@angular/core';
import {Http, Headers} from '@angular/http';
import { User } from "../models/user";

@Injectable({
  providedIn: 'root'
})
export class UserManagementService {
  private BASE_URL: string = 'http://localhost:5049/normal_users';
  constructor(private http: Http) {}

  getUserInfo(token: string, userId: string): Promise<any> {
    let headers: Headers = new Headers({
      'Content-Type': 'application/json',
      'Authorization': token
    });
    let url: string = `${this.BASE_URL}/${userId}`;
    return this.http.get(url, {headers: headers}).toPromise();
  }

  updateUserStatus(token: string, userId: string, newStatus: string): Promise<any> {
    let headers: Headers = new Headers({
      'Content-Type': 'application/json',
      'Authorization': token
    });
    let url: string = `{${this.BASE_URL}/${userId}`;
    return this.http.post(url, {"status": newStatus}, {headers: headers}).toPromise();
  }
}

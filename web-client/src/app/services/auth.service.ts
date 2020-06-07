import { Injectable } from '@angular/core';
import {Http, Headers} from '@angular/http';
import { User } from "../models/user";
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private BASE_URL: string = 'http://localhost:5049/auth';
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  constructor(private http: Http, private router: Router) {}

  login(user: User): Promise<any> {
    let url: string = `${this.BASE_URL}/login`;
    return this.http.post(url, user, {headers: this.headers}).toPromise();
  }

  register(user: User): Promise<any> {
    let url: string = `${this.BASE_URL}/register`;
    return this.http.post(url, user, {headers: this.headers}).toPromise();
  }

  logout() {
    if (localStorage.getItem("token") != null) {
      localStorage.removeItem("token");
    }
    this.router.navigateByUrl('/login')
  }
}

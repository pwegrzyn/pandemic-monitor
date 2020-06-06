import { Component } from '@angular/core';
import {AuthService} from "../../services/auth.service";
import { User} from "../../models/user";
import {Router} from "@angular/router";

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  user: User = new User();
  constructor(private auth: AuthService, private router: Router) { }

  onLogin() {
    console.log("onLogin")
    this.auth.login(this.user)
      .then((response) => {
        console.log(response.json());
        if (response.json().status == "success") {
          localStorage.setItem('token', response.json().auth_token)
          this.router.navigateByUrl('/users')
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }

  onGotoRegister() {
    this.router.navigateByUrl('/register')
  }
}

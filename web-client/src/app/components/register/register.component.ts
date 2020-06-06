import { Component } from '@angular/core';
import { User } from "../../models/user";
import { AuthService } from "../../services/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {

  user: User = new User();
  constructor(private auth: AuthService, private router: Router) { }

  onRegister(): void {
    this.auth.register(this.user)
      .then((user) => {
        console.log(user.json())
      })
      .catch((err) => {
        console.log("catch");
        console.log(err);
      });
  }

  onGotoLogin() {
    this.router.navigateByUrl('/login')
  }
}

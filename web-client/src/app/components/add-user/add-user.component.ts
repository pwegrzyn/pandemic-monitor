import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {NormalUser} from "../../models/normal-user";
import {UserManagementService} from "../../services/user-management.service";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-add-user',
  templateUrl: './add-user.component.html',
  styleUrls: ['./add-user.component.scss']
})
export class AddUserComponent implements OnInit {

  constructor(private router: Router, private userService: UserManagementService, private auth: AuthService) { }
  normalUser: NormalUser;

  ngOnInit() {
    console.log("add user component init")
    this.normalUser = new NormalUser()
  }

  onCancel() {
    this.router.navigateByUrl('/users')
  }

  onAddUser() {
    this.userService.addNormalUser(localStorage.getItem("token"), this.normalUser).toPromise()
      .then((user) => {
        console.log(user.json())
        this.router.navigateByUrl('/users/' + user.json()["user_api_id"])
      })
      .catch((err) => {
        console.log("catch");
        console.log(err);
        if (err.status == 401) {
          this.auth.logout()
        } else {
          this.router.navigateByUrl('/users')
        }
      });
  }
}

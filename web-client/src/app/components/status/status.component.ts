import { Component, OnInit } from '@angular/core';
import { UserManagementService } from "../../services/user-management.service";
import {ActivatedRoute, Router} from "@angular/router";
import {User} from "../../models/user";
import {AuthService} from "../../services/auth.service";

export const COVID_STATUS_LIST: string[] = [
  "healthy",
  "covid-positive",
  "covid-negative"
]

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit {
  constructor(
    private userService: UserManagementService,
    private route: ActivatedRoute,
    private router: Router,
    private auth: AuthService) { }

  userId: any;
  userName: string;
  userSurname: string;
  userStatus: string;


  ngOnInit() {
    this.userId = this.route.snapshot.paramMap.get("userId")
    this.userService.getUserInfo(localStorage.getItem("token"), this.userId)
      .then((response) => {
        console.log("got response")
        console.log(response)
        if (response.json().status == "success") {
          this.userName = response.json().name;
          this.userSurname = response.json().surname;
          this.userStatus = response.json().user_status;
        } else {
          this.router.navigateByUrl('/users')
        }
      })
      .catch((err) => {
        console.log("error")
        console.log(err)
        console.log(err.status)
        if (err.status == 404) {
          console.log("navigating to createUser")
          this.router.navigateByUrl('/users/create')
        } else if (err.status == 401) {
          this.auth.logout()
        } else {
            this.router.navigateByUrl('/users')
        }
      });
  }

  onChangeStatus(newStatus: string) {
    this.userService.updateUserStatus(localStorage.getItem("token"), this.userId, newStatus)
      .then((response) => {
        this.userStatus = newStatus
      })
      .catch((err) => {
        console.log(err)
        if (err.status == 401) {
          this.auth.logout()
        } else {
          this.router.navigateByUrl('/users')
        }
      })
  }

  onBack() {
    this.router.navigateByUrl('/users')
  }
}

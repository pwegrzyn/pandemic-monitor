import { Component, OnInit } from '@angular/core';
import { UserManagementService } from "../../services/user-management.service";
import {ActivatedRoute, Router} from "@angular/router";
import {User} from "../../models/user";

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
  constructor(private userService: UserManagementService, private route: ActivatedRoute, private router: Router) { }

  availableStatuses = COVID_STATUS_LIST;

  userId: any;
  userEmail: string;
  userStatus: string;


  ngOnInit() {
    this.userId = this.route.snapshot.paramMap.get("userId")
    this.userService.getUserInfo(localStorage.getItem("token"), this.userId)
      .then((response) => {
        console.log("got response")
        console.log(response)
        // if (response.json().status == "success") {
        //   this.userEmail = response.json().email;
        //   this.userStatus = response.json().userStatus;
        // }
      })
      .catch((err) => {
        console.log("error")
        console.log(err)
        this.router.navigateByUrl('/users')
      });
  }

}

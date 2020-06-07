import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AuthService} from "../../services/auth.service";
import {UserManagementService} from "../../services/user-management.service";

@Component({
  selector: 'app-find-user',
  templateUrl: './find-user.component.html',
  styleUrls: ['./find-user.component.scss']
})
export class FindUserComponent implements OnInit {
  userId: string;

  constructor(private router: Router, private auth: AuthService) { }

  ngOnInit() {
    console.log("init")
  }

  onFindUser(userId: string) {
    this.router.navigateByUrl('/users/' + userId)
  }

  onLogout() {
    this.auth.logout()
  }

  onAddUser() {
    this.router.navigateByUrl('/users/create')
  }
}

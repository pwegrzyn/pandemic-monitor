import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-find-user',
  templateUrl: './find-user.component.html',
  styleUrls: ['./find-user.component.scss']
})
export class FindUserComponent implements OnInit {
  userId: string;

  constructor(private router: Router) { }

  ngOnInit() {
  }

  onFindUser(userId: string) {
    this.router.navigateByUrl('/users/' + userId)
  }
}

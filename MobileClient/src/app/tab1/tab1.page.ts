import { Component, OnInit } from '@angular/core';

import { IdentificationService } from "../services/identification.service";
import { FetchingService } from '../services/fetching.service';


@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page implements OnInit {

  currentIdentityNumber: number;
  currentStatus: string;

  constructor(private identificationService: IdentificationService, private fetchingService: FetchingService) {
    this.currentStatus = "unknown";
  }

  ngOnInit(): void {
    this.identificationService.getIdentity().subscribe((val) => {
      this.currentIdentityNumber = val;
    });
  }

  updateStatusClicked() {
    this.fetchingService.getStatus().subscribe((val) => {
      this.currentStatus = val;
    });
  }

}

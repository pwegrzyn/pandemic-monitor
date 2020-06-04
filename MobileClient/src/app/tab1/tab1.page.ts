import { Component, OnInit } from '@angular/core';

import { IdentificationService } from "../services/identification.service";


@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page implements OnInit {

  currentIdentityNumber: number;

  constructor(private identificationService: IdentificationService) {
    
  }

  ngOnInit(): void {
    this.identificationService.getIdentity().subscribe((val) => {
      this.currentIdentityNumber = val;
    });
  }

}

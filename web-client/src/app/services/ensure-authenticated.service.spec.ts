import { TestBed } from '@angular/core/testing';

import { EnsureAuthenticatedService } from './ensure-authenticated.service';

describe('EnsureAuthenticatedService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: EnsureAuthenticatedService = TestBed.get(EnsureAuthenticatedService);
    expect(service).toBeTruthy();
  });
});

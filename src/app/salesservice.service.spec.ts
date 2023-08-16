import { TestBed } from '@angular/core/testing';

import { SalesserviceService } from './salesservice.service';

describe('SalesserviceService', () => {
  let service: SalesserviceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SalesserviceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

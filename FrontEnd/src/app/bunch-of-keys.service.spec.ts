import { TestBed } from '@angular/core/testing';

import { BunchOfKeysService } from './bunch-of-keys.service';

describe('BunchOfKeysService', () => {
  let service: BunchOfKeysService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BunchOfKeysService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

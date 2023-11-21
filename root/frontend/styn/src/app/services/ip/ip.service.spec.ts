import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { IpService } from './ip.service';

describe('IpService', () => {
  let service: IpService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [IpService],
    });
    service = TestBed.inject(IpService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalespredictComponent } from './salespredict.component';

describe('SalespredictComponent', () => {
  let component: SalespredictComponent;
  let fixture: ComponentFixture<SalespredictComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SalespredictComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SalespredictComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

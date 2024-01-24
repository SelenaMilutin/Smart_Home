import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnePiComponent } from './one-pi.component';

describe('OnePiComponent', () => {
  let component: OnePiComponent;
  let fixture: ComponentFixture<OnePiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OnePiComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OnePiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

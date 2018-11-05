import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RangeSelectionComponent } from './range-selection.component';

describe('RangeSelectionComponent', () => {
  let component: RangeSelectionComponent;
  let fixture: ComponentFixture<RangeSelectionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RangeSelectionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RangeSelectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PopupPickerComponent } from './popup-picker.component';

describe('PopupPickerComponent', () => {
  let component: PopupPickerComponent;
  let fixture: ComponentFixture<PopupPickerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PopupPickerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PopupPickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

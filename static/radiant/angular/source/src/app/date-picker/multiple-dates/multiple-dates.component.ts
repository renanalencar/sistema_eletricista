import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-multiple-dates',
  templateUrl: './multiple-dates.component.html',
  styleUrls: ['./multiple-dates.component.scss']
})
export class MultipleDatesComponent implements OnInit {
  displayMonths = 2;
  constructor() { }

  ngOnInit() {
  }
}

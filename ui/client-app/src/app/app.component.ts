import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subject, Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent implements OnInit {
  literals = {
    Title: 'Order Management',
  };
  showHeader: boolean = true;
  displayLoader: boolean;
  baseRouterOutletHeight: number = 500;
  baseRouterOutletFixedHeight: number = 85;
  windowSizeChanged = new Subject<Event>();
  get title() {
    return this.literals.Title;
  }
  async ngOnInit() {
    this.displayLoader = false;
  }
  // onResize(e: Event): void {
  //   this.windowSizeChanged.next(e);
  // }
}

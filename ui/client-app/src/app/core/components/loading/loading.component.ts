import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-loading',
  templateUrl: './loading.component.html',
  styleUrls: ['./loading.component.less']
})
export class LoadingComponent {
  constructor() { }
  displayLoader: boolean;
  @Input()
  visible: boolean;
}
